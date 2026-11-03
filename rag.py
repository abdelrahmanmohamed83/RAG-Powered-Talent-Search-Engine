import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


# ============================================================
# Load saved RAG data
# ============================================================

with open("resume_chunks.pkl", "rb") as f:
    documents = pickle.load(f)

embeddings = np.load("resume_embeddings.npy")

index = faiss.read_index("resume_index.faiss")


# ============================================================
# Embedding model
# ============================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


print(f"Loaded {len(documents)} chunks")
print(f"Embeddings: {embeddings.shape}")
print(f"FAISS vectors: {index.ntotal}")


# ============================================================
# Build candidate resume lookup
# ============================================================

candidate_chunks = {}

for doc in documents:

    candidate_id = doc["candidate_id"]

    if candidate_id not in candidate_chunks:
        candidate_chunks[candidate_id] = []

    candidate_chunks[candidate_id].append(
        doc["text"]
    )


def get_candidate_resume(candidate_id):

    if candidate_id not in candidate_chunks:
        return None

    return "\n\n".join(
        candidate_chunks[candidate_id]
    )


# ============================================================
# Search candidates
# ============================================================

def search_candidates(
    query,
    top_n=5,
    chunk_k=30
):

    # Embed recruiter query
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    # Search FAISS
    scores, indices = index.search(
        query_embedding.astype("float32"),
        chunk_k
    )

    candidate_scores = {}

    # Convert chunk results → candidate results
    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx < 0:
            continue

        doc = documents[idx]

        candidate_id = doc["candidate_id"]

        if (
            candidate_id not in candidate_scores
            or score > candidate_scores[candidate_id]
        ):
            candidate_scores[candidate_id] = float(score)

    # Rank candidates
    ranked_candidates = sorted(
        candidate_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Return requested number
    results = []

    for candidate_id, score in ranked_candidates[:top_n]:

        resume = get_candidate_resume(
            candidate_id
        )

        results.append({
            "candidate_id": candidate_id,
            "score": score,
            "resume": resume
        })

    return results