import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

INPUT_PATH = "data/processed/shl_catalog_clean.json"
VECTOR_INDEX_PATH = "data/vectors/shl_index.faiss"
META_PATH = "data/vectors/shl_metadata.json"

print("Step 5 started: Loading cleaned catalog...")

# Load cleaned data
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total assessments found: {len(data)}")

# Prepare text for embeddings
texts = []
metadata = []

for item in data:
    combined_text = (
        item["name"] + ". "
        + item["description"] + ". "
        + "Test type: " + " ".join(item["test_type"])
    )
    texts.append(combined_text)
    metadata.append(item)

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

embeddings = np.array(embeddings).astype("float32")

print("Creating FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, VECTOR_INDEX_PATH)

with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("Step 5 completed: FAISS index and metadata saved successfully")
