# 🎯 RAG-Powered Talent Search Engine & AI Recruiter

An intelligent, conversational recruitment platform powered by **Retrieval-Augmented Generation (RAG)** and **Google Gemini (`gemini-2.5-flash`)**. This system enables recruiters and hiring managers to search, evaluate, and compare candidates from a resume vector database using natural language queries.

---

## 🌟 Key Features

- **Semantic Talent Retrieval (RAG):**
  - High-dimensional semantic search using `sentence-transformers/all-MiniLM-L6-v2`.
  - Fast vector similarity search with **FAISS** (Facebook AI Similarity Search).
  - Chunk-to-candidate aggregation to evaluate full resume context.

- **Autonomous Agentic Recruiter:**
  - Built with the official **Google GenAI SDK** and `gemini-2.5-flash`.
  - Autonomous function/tool calling architecture:
    - `search_candidates`: Translates recruiter requirements into semantic queries and retrieves top matches.
    - `get_candidate`: Pulls complete resume details for specific ranked candidates.
    - `compare_candidates`: Conducts side-by-side comparative analysis between candidates.

- **Context-Aware Conversational Memory:**
  - Maintains multi-turn context (e.g., handles co-references like *"Tell me more about candidate 2"*, *"Does he have leadership experience?"*).
  - Adheres strictly to facts in resumes to avoid hallucinating skills or qualifications.

- **Modern Interactive Web UI:**
  - Built with **Streamlit** featuring a sleek dark-themed recruiter dashboard.
  - Interactive chat interface with real-time model thinking and tool execution visibility.

---

## 🏗️ Architecture

```
Recruiter (Natural Language)
          │
          ▼
   Streamlit Web UI (app.py)
          │
          ▼
   Gemini Recruiter Agent (agent.py)
          │
    ┌─────┴─────────────────────────┐
    ▼                               ▼
Tool Calling                  Conversation Memory
(search / inspect / compare)
    │
    ▼
RAG Pipeline (rag.py)
    │
    ├── SentenceTransformer ("all-MiniLM-L6-v2")
    └── FAISS Vector Database (resume_index.faiss)
```

---

## 📁 Repository Structure

```
.
├── app.py                   # Streamlit web application & UI
├── agent.py                 # Gemini-powered recruiter agent with tool calling
├── rag.py                   # Vector search & candidate retrieval pipeline
├── RAG_Talent_Search.ipynb  # End-to-end data processing, chunking & indexing notebook
├── resume_chunks.pkl        # Pre-processed resume text chunks and candidate metadata
├── resume_embeddings.npy    # Pre-computed normalized dense embeddings
├── resume_index.faiss       # FAISS index for fast nearest-neighbor retrieval
├── requirements.txt         # Project Python dependencies
├── .env.example             # Example environment variable template
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/abdelrahmanmohamed83/RAG-Powered-Talent-Search-Engine.git
cd RAG-Powered-Talent-Search-Engine
```

### 2. Create and Activate a Virtual Environment

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory (you can copy `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your Google Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

> **Note:** You can obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### 5. Run the Application

Launch the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## 💬 Example Queries & Interaction

Here are some prompts you can test in the interactive recruiter chat:

1. **Candidate Discovery:**
   > *"Find me 5 candidates with experience in Computer Vision, PyTorch, and deploying deep learning models."*

2. **Deep-Dive Profile Analysis:**
   > *"Tell me more about candidate 1. What notable projects and work experience do they have?"*

3. **Follow-up Questions with Coreference:**
   > *"Do they have any leadership or mentoring experience?"*

4. **Comparative Assessment:**
   > *"Compare candidate 1 and candidate 3. Who is better suited for an MLOps engineering role?"*

---

## 🛠️ Tech Stack

- **LLM & Agent:** Google Gemini (`gemini-2.5-flash`), `google-genai` SDK
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Vector Search:** `faiss-cpu`
- **Application Framework:** `streamlit`
- **Data & Computation:** `numpy`, `pickle`

---

## 📄 License

This project is licensed under the MIT License - feel free to use and modify for your own projects.
