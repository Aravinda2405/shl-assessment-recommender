import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

INDEX_PATH = "data/vectors/shl_index.faiss"
META_PATH = "data/vectors/shl_metadata.json"

print("Loading FAISS index and metadata...")

index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")


def recommend_assessments(query, top_k=10):
    query_embedding = model.encode([query]).astype("float32")

    # retrieve more for better balance
    distances, indices = index.search(query_embedding, 20)

    candidates = [metadata[i] for i in indices[0]]

    # Separate by test type
    technical = [c for c in candidates if "K" in c["test_type"]]
    behavioral = [c for c in candidates if "P" in c["test_type"]]

    final_results = []

    # balance: mix both if possible
    final_results.extend(technical[:5])
    final_results.extend(behavioral[:5])

    # fallback if not enough
    if len(final_results) < top_k:
        for c in candidates:
            if c not in final_results:
                final_results.append(c)
            if len(final_results) == top_k:
                break

    return final_results
