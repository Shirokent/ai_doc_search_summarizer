from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
import os

from .utils import save_upload_file, embed_and_store, semantic_search, summarize_text

app = FastAPI(title="AI Document Search & Summarizer")

UPLOAD_DIR = "uploaded_files"
VECTOR_STORE = "vector_store.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    filepath = await save_upload_file(file, UPLOAD_DIR)
    embed_and_store(filepath, VECTOR_STORE)
    return {"status": "success", "filename": file.filename}

@app.get("/search/")
async def search_docs(query: str, top_k: int = 3):
    results = semantic_search(query, VECTOR_STORE, top_k=top_k)
    return {"query": query, "results": results}

@app.get("/summarize/")
async def summarize(query: str):
    results = semantic_search(query, VECTOR_STORE, top_k=1)
    if not results:
        return JSONResponse(content={"error": "No results found"}, status_code=404)
    text = results[0]["content"]
    summary = summarize_text(text)
    return {"query": query, "summary": summary}
