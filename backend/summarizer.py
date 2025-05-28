import os
import requests
from dotenv import load_dotenv
from backend.retriever import retrieve_relevant_chunks
from backend.fallback_scraper import fallback_scrape_and_extract
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def is_valid_content(content: str) -> bool:
    if not isinstance(content, str):
        return False
    stripped = content.strip().lower()
    return bool(stripped and stripped != "n/a")


def summarize_text(text: str, query: str = "") -> str:
    """Summarize text using Groq LLM."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You are a financial assistant AI. Summarize the following SEC filing content in detail and"
        "in clear and concise points. If a query is provided, make the summary query-focused."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Query: {query}\n\nContent:\n{text}"}
    ]

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.4
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def summarize_with_fallback(query: str, top_k=5) -> str:
    """Try summarization from retrieved chunks; fallback to raw HTML if needed."""
    chunks = retrieve_relevant_chunks(query, top_k=top_k)

    for chunk in chunks:
        content = chunk.get("content", "").strip()

        if is_valid_content(content):
            return summarize_text(content, query)
        else:
            print(f"Fallback triggered for chunk ID: {chunk['chunk_id']}")
            fallback = fallback_scrape_and_extract(
                ticker=chunk["ticker"],
                filing_type=chunk["filing_type"],
                filing_date=chunk["filing_date"],
                query=query
            )
            if is_valid_content(fallback):
                return summarize_text(fallback, query)

    return "Sorry, no relevant content could be found to summarize."


def clean_summary_output(summary: str) -> str:
    import re

    # Remove stray markdown italics or bolds around units
    summary = re.sub(r"[*_](million|billion)[*_]", r"\1", summary, flags=re.IGNORECASE)

    # Fix number + unit merging like "103.9billion" -> "103.9 billion"
    summary = re.sub(r"(\d)(million|billion)", r"\1 \2", summary, flags=re.IGNORECASE)

    # Add spacing before markdown tags if missing
    summary = re.sub(r"(\w)([_*])", r"\1 \2", summary)
    summary = re.sub(r"([_*])(\w)", r"\1 \2", summary)

    # Remove any repeated markdown chars
    summary = re.sub(r"[*_]{2,}", "*", summary)

    # Remove markdown if rendering issues persist
    # summary = re.sub(r"[_*]", "", summary)

    return summary


if __name__ == "__main__":
    test_query = "Provide details about Apple's total net sales"
    print("Fetching summary...")
    print(summarize_with_fallback(test_query))
