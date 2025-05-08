import re
from bs4 import BeautifulSoup

def clean_text(raw_text: str) -> str:
    """
    Cleans raw SEC HTML or text by removing tags and normalizing whitespace.
    """
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    text = re.sub(r'Page \d+ of \d+', '', text)  # Remove page numbers
    text = text.lower()
    return text.strip()
