import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.summarizer import is_valid_content, clean_summary_output
from backend.retriever import retrieve_relevant_chunks

def test_is_valid_content():
    assert is_valid_content("Apple had a total revenue of $394 billion.") is True
    assert is_valid_content("   ") is False
    assert is_valid_content("n/a") is False
    assert is_valid_content("N/A") is False

def test_clean_summary_output_formatting():
    raw = "Apple earned 394billionin2023 and paid 5.2millionininterest."
    cleaned = clean_summary_output(raw)
    assert "394 billion" in cleaned or "394billion" in cleaned  # depending on LLM output
    assert "5.2 million" in cleaned

def test_retrieve_chunks_returns_data():
    chunks = retrieve_relevant_chunks("What are the risks for Apple?", top_k=1)
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert "section" in chunks[0]
