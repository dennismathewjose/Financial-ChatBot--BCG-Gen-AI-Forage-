import json
import os
import requests
from dotenv import load_dotenv
from embedding.pinecone_client import init_pinecone

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def get_embeddings(text):
    """Call Ollama's embedding API for nomic-embed-text"""
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    response.raise_for_status()
    return response.json()["embedding"]

def embed_and_push_chunks(json_path):
    index = init_pinecone()

    with open(json_path, "r") as f:
        chunks = json.load(f)

    for chunk in chunks:
        embedding = get_embeddings(chunk["content"])
        ticker_namespace = chunk.get("ticker", "default").upper()

        index.upsert(
            vectors=[{
                "id": chunk["chunk_id"],
                "values": embedding,
                "metadata": {
                    "section": chunk["section"],
                    "subsection": chunk["subsection"],
                    "content": chunk["content"],
                    "ticker": chunk["ticker"],
                    "filing_type": chunk["filing_type"],
                    "filing_date": chunk["filing_date"],
                    "tags": chunk["tags"],
                    "has_table": chunk["has_table"]
                }
            }],
            namespace=ticker_namespace
        )

        print(f"Upserted: {chunk['chunk_id']} → Namespace: {ticker_namespace}")

if __name__ == "__main__":
    embed_and_push_chunks("data/chunks/sample_chunks.json")
