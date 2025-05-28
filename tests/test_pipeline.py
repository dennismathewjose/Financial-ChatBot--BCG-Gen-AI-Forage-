import sys
import os
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.summarizer import is_valid_content, clean_summary_output
from backend.retriever import retrieve_relevant_chunks

# ----------------------------
# Tests for summarizer logic
# ----------------------------

def test_is_valid_content():
    assert is_valid_content("Apple had a total revenue of $394 billion.")
    assert not is_valid_content("   ")
    assert not is_valid_content("n/a")
    assert not is_valid_content("N/A")

def test_clean_summary_output_formatting():
    raw = "Apple earned 394billionin2023 and paid 5.2millionininterest."
    cleaned = clean_summary_output(raw)
    assert "394 billion" in cleaned or "394billion" in cleaned
    assert "5.2 million" in cleaned

# --------------------------------------
# Tests for retriever (mocked behavior)
# --------------------------------------

@patch("backend.retriever.init_pinecone")
@patch("backend.retriever.embed_query")
def test_retrieve_chunks_returns_data(mock_embed_query, mock_init_pinecone):
    # Setup mock return values
    mock_embed_query.return_value = [0.1] * 768
    mock_index = mock_init_pinecone.return_value
    mock_index.query.return_value = {
        "matches": [
            {
                "score": 0.95,
                "id": "chunk-1",
                "metadata": {
                    "content": "Risk factors include global market uncertainty.",
                    "section": "Item 1A",
                    "subsection": "Risk Factors",
                    "tags": ["risk"],
                    "ticker": "AAPL",
                    "filing_type": "10-K",
                    "filing_date": "2023-09-30",
                    "has_table": False
                }
            }
        ]
    }

    # Run actual test
    chunks = retrieve_relevant_chunks("What are the risks for Apple?", top_k=1)

    assert isinstance(chunks, list)
    assert len(chunks) == 1
    assert chunks[0]["section"] == "Item 1A"
    assert "Risk" in chunks[0]["subsection"]

