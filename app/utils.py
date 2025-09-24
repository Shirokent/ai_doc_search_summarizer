import os
import json
import hashlib
from typing import List
from fastapi import UploadFile
import shutil

# Simple sentence embeddings using bag of words (placeholder)
def embed_text(text: str) -> List[float]:
    # Very naive embedding: use hash of words as numbers
    return [float(int(hashlib.sha256(word.encode()).hexdigest(), 16) % 1000) for word in text.split()[:50]]

async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    os.makedirs(destination, exist_ok=True)
    file_path = os.path.join(destination, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def embed_and_store(filepath: str, store_file: str):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    embedding = embed_text(content)
    record = {
        "filename": os.path.basename(filepath),
        "content": content,
        "embedding": embedding
    }

    if os.path.exists(store_file):
        with open(store_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)
    with open(store_file, "w", encoding="utf-8") as f:
        json.dump(data, f)

def semantic_search(query: str, store_file: str, top_k: int = 3):
    if not os.path.exists(store_file):
        return []

    with open(store_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    query_emb = embed_text(query)

    def cosine_similarity(v1, v2):
        dot = sum(a*b for a,b in zip(v1, v2))
        norm1 = sum(a*a for a in v1) ** 0.5
        norm2 = sum(a*a for a in v2) ** 0.5
        return dot / (norm1 * norm2 + 1e-9)

    scored = []
    for d in data:
        sim = cosine_similarity(query_emb, d["embedding"])
        scored.append({"filename": d["filename"], "content": d["content"], "score": sim})

    scored = sorted(scored, key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

def summarize_text(text: str) -> str:
    # Naive summarization: first 3 sentences
    sentences = text.split(".")
    return ".".join(sentences[:3]) + "..."
