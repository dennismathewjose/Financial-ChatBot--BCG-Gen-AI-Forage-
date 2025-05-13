# backend/fallback_scraper.py
from bs4 import BeautifulSoup
from pathlib import Path

def fallback_scrape_and_extract(ticker: str, filing_type: str, filing_date: str, query: str) -> str:
    """
    Extract fallback content by scanning raw HTML for query-relevant paragraphs.
    """
    safe_path = f"data/raw/{ticker.lower()}_{filing_type.lower()}_{filing_date}.html"

    if not Path(safe_path).exists():
        print("Fallback raw HTML not found.")
        return ""

    with open(safe_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        all_text = soup.get_text(separator="\n")

    paragraphs = [p.strip() for p in all_text.split("\n") if len(p.strip()) > 100]
    for para in paragraphs:
        if query.lower() in para.lower():
            return para

    return ""
