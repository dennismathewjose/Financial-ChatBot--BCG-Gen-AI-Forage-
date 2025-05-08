import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from embedding.cleaner import clean_text
from embedding.preload_pipeline import simple_chunk

def test_clean_text_removes_html():
    raw = "<html><body><p>Page 1 of 20</p>This is financial data</body></html>"
    cleaned = clean_text(raw)
    assert "<" not in cleaned
    assert "Page" not in cleaned
    assert "financial data" in cleaned

def test_chunking_works():
    sample = "This is a test sentence. " * 100  # ~600 words
    chunks = list(simple_chunk(sample, chunk_size=100))
    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)
