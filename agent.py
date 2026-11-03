import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from rag import (
    search_candidates,
    get_candidate_resume
)

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


# ============================================================
# Conversation memory
# ============================================================

conversation_history = []

current_candidates = {}


# ============================================================
# Save latest search
# ============================================================

def save_search_results(results):

    global current_candidates

    current_candidates = {}

    for rank, candidate in enumerate(results, start=1):

        current_candidates[rank] = candidate["candidate_id"]


# ============================================================
# Get candidate from current search
# ============================================================

def get_candidate_by_rank(rank):

    if rank not in current_candidates:

        return {
            "error": (
                f"Candidate {rank} does not exist "
                "in the current search results."
            )
        }

    candidate_id = current_candidates[rank]

    resume = get_candidate_resume(candidate_id)

    return {
        "candidate_id": candidate_id,
        "resume": resume
    }


# ============================================================
# Tool 1: Search
# ============================================================

search_tool = types.FunctionDeclaration(

    name="search_candidates",

    description="""
    Search the resume database for candidates matching
    the recruiter's requirements.

    Use this when the recruiter asks to:
    - find candidates
    - search candidates
    - recommend candidates
    - rank candidates
    - find the strongest candidates

    The recruiter can request ANY number of candidates.
    """,

    parameters={

        "type": "OBJECT",

        "properties": {

            "query": {
                "type": "STRING",
                "description": (
                    "The recruiter's requirements."
                )
            },

            "top_n": {
                "type": "INTEGER",
                "description": (
                    "Number of candidates requested. "
                    "Use the exact number requested. "
                    "Default to 5 if no number is specified."
                )
            }
        },

        "required": ["query"]
    }
)


# ============================================================
# Tool 2: Get candidate
# ============================================================

candidate_tool = types.FunctionDeclaration(

    name="get_candidate",

    description="""
    Retrieve the complete resume of a candidate
    from the most recent search results.

    Use this for questions such as:
    - Tell me more about candidate 1
    - What are candidate 2's skills?
    - Does he have leadership experience?
    - Where does she work?
    """,

    parameters={

        "type": "OBJECT",

        "properties": {

            "rank": {
                "type": "INTEGER",
                "description": (
                    "Candidate rank from the most recent search."
                )
            }
        },

        "required": ["rank"]
    }
)


# ============================================================
# Tool 3: Compare
# ============================================================

compare_tool = types.FunctionDeclaration(

    name="compare_candidates",

    description="""
    Compare two candidates from the most recent search.

    Use this when the recruiter asks:
    - Compare candidate 1 and candidate 3
    - Who is stronger, candidate 2 or candidate 5?
    """,

    parameters={

        "type": "OBJECT",

        "properties": {

            "candidate_a": {
                "type": "INTEGER",
                "description": "First candidate rank."
            },

            "candidate_b": {
                "type": "INTEGER",
                "description": "Second candidate rank."
            }
        },

        "required": [
            "candidate_a",
            "candidate_b"
        ]
    }
)


# ============================================================
# Tools
# ============================================================

agent_tools = types.Tool(

    function_declarations=[
        search_tool,
        candidate_tool,
        compare_tool
    ]
)


# ============================================================
# Agent configuration
# ============================================================

agent_config = types.GenerateContentConfig(

    temperature=0.2,

    tools=[
        agent_tools
    ],

    system_instruction="""
You are an AI recruitment assistant connected to a
resume database.

Your job is to help recruiters search and evaluate candidates.

IMPORTANT RULES:

1. When the recruiter asks to find or search for candidates,
   ALWAYS use search_candidates.

2. The recruiter can request any number of candidates:
   1, 3, 5, 10, 20, etc.

3. Always respect the requested number.

4. If no number is specified, return 5 candidates.

5. Candidate numbers refer to rankings from the
   MOST RECENT search.

6. If the recruiter asks about a candidate from the
   current results, use get_candidate.

7. Understand conversational references.

   Example:

   Recruiter:
   Find me 5 deep learning candidates.

   Recruiter:
   Tell me more about candidate 1.

   Recruiter:
   Does he have leadership experience?

   The phrase "he" refers to candidate 1.

8. Use compare_candidates when comparing candidates.

9. Base your answers ONLY on resume information.

10. Never invent experience, skills, education,
    leadership, certifications, or qualifications.

11. If something is not explicitly mentioned,
    clearly say that it is not explicitly mentioned.

12. Similarity scores are retrieval signals only.
    They are NOT proof of a skill.

13. Give recruiter-friendly answers.

14. When returning search results, clearly identify:
    - Rank
    - Candidate ID
    - Candidate name when available
    - Relevant experience
    - Why they match

15. Do not unnecessarily expose raw resume text
    unless the recruiter asks for detailed information.
"""
)


# ============================================================
# Execute tools
# ============================================================

def execute_tool(tool_name, args):

    # -----------------------------------------
    # Search
    # -----------------------------------------

    if tool_name == "search_candidates":

        query = args["query"]

        top_n = args.get(
            "top_n",
            5
        )

        results = search_candidates(
            query=query,
            top_n=top_n,
            chunk_k=30
        )

        save_search_results(results)

        return results


    # -----------------------------------------
    # Get candidate
    # -----------------------------------------

    elif tool_name == "get_candidate":

        rank = args["rank"]

        return get_candidate_by_rank(rank)


    # -----------------------------------------
    # Compare candidates
    # -----------------------------------------

    elif tool_name == "compare_candidates":

        rank_a = args["candidate_a"]
        rank_b = args["candidate_b"]

        candidate_a = get_candidate_by_rank(
            rank_a
        )

        candidate_b = get_candidate_by_rank(
            rank_b
        )

        return {
            "candidate_a": candidate_a,
            "candidate_b": candidate_b
        }


    return {
        "error": f"Unknown tool: {tool_name}"
    }


# ============================================================
# Main recruiter agent
# ============================================================

def recruiter_agent(user_message):

    conversation_history.append({

        "role": "user",

        "parts": [
            {
                "text": user_message
            }
        ]
    })


    while True:

        response = client.models.generate_content(

            model="gemini-3.5-flash",

            contents=conversation_history,

            config=agent_config
        )


        # -----------------------------------------
        # Check for tool calls
        # -----------------------------------------

        function_calls = []

        for part in response.candidates[0].content.parts:

            if part.function_call:

                function_calls.append(
                    part.function_call
                )


        # -----------------------------------------
        # Final response
        # -----------------------------------------

        if not function_calls:

            conversation_history.append({

                "role": "model",

                "parts": response.candidates[0].content.parts
            })

            return response.text


        # -----------------------------------------
        # Save Gemini tool request
        # -----------------------------------------

        conversation_history.append({

            "role": "model",

            "parts": response.candidates[0].content.parts
        })


        tool_parts = []


        # -----------------------------------------
        # Execute tools
        # -----------------------------------------

        for function_call in function_calls:

            tool_name = function_call.name

            args = dict(
                function_call.args
            )

            print(
                f"Tool: {tool_name}"
            )

            print(
                f"Arguments: {args}"
            )


            result = execute_tool(
                tool_name,
                args
            )


            print(
                f"Tool result type: {type(result)}"
            )


            tool_parts.append({

                "function_response": {

                    "name": tool_name,

                    "response": {
                        "result": result
                    }
                }
            })


        # -----------------------------------------
        # Give tool results back to Gemini
        # -----------------------------------------

        conversation_history.append({

            "role": "user",

            "parts": tool_parts
        })