import os
import requests
from dotenv import load_dotenv
from embedding.pinecone_client import init_pinecone

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def embed_query(query: str):
    """Generate embedding for user query using Ollama + nomic-embed-text"""
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": query
        }
    )
    response.raise_for_status()
    return response.json()["embedding"]

def retrieve_relevant_chunks(query: str, top_k=5, namespace=""):
    """
    Query Pinecone to retrieve the top-k most relevant chunks for a given query.

    Args:
        query (str): User query
        top_k (int): Number of top matches to retrieve
        namespace (str): Company ticker (e.g., AAPL, MSFT, AMZN) used for multi-filing isolation

    Returns:
        List[Dict]: Matched chunk metadata and content
    """
    index = init_pinecone()
    query_embedding = embed_query(query)

    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace or ""  # fallback to global space
    )

    results = []
    for match in result["matches"]:
        metadata = match["metadata"]
        results.append({
            "score": match["score"],
            "content": metadata.get("content") or "N/A",
            "section": metadata.get("section"),
            "subsection": metadata.get("subsection"),
            "tags": metadata.get("tags"),
            "chunk_id": match["id"],
            "ticker": metadata.get("ticker"),
            "filing_type": metadata.get("filing_type"),
            "filing_date": metadata.get("filing_date"),
            "has_table": metadata.get("has_table", False)
        })

    return results

if __name__ == "__main__":
    # Local testing
    query = "What are the risks related to international operations?"
    chunks = retrieve_relevant_chunks(query, top_k=3, namespace="AMZN")

    if not chunks:
        print("No relevant chunks found.")
    else:
        for i, chunk in enumerate(chunks, 1):
            print(f"\nChunk {i} (Score: {chunk['score']:.4f})")
            print(f"Section: {chunk['section']} - {chunk.get('subsection', 'N/A')}")
            print(f"Tags: {chunk.get('tags', [])}")
            print(f"Content Snippet: {chunk.get('content', '')[:300]}...")
