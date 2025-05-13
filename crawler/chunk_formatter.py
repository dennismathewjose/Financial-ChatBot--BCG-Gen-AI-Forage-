import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

RAW_HTML_PATH = "data/raw/aapl_10k_2023.html"
CHUNK_SAVE_PATH = "data/chunks/sample_chunks.json"

TICKER = "AAPL"
FILING_TYPE = "10-K"
FILING_DATE = "2023-09-30"

def extract_clean_text():
    with open(RAW_HTML_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for tag in soup(["script", "style", "footer", "nav"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    print("\nSection Headers Found:")
    for line in lines:
        if re.match(r"^(ITEM|Item)\s+\d{1,2}[A]?\.", line):
            print(" -", line)

    return lines


def split_into_sections(lines):
    section_indices = []
    for i, line in enumerate(lines):
        if re.match(r"^(ITEM|Item)\s+\d{1,2}[A]?\.?", line.strip()):
            section_indices.append((i, line.strip()))

    section_chunks = []
    for idx in range(len(section_indices) - 1):
        start_idx, section_title = section_indices[idx]
        end_idx, _ = section_indices[idx + 1]
        section_lines = lines[start_idx + 1:end_idx]
        section_chunks.append((section_title, section_lines))

    return section_chunks


def basic_subchunk_split(section_title, lines):
    text = "\n".join(lines)
    sub_chunks = []
    current_sub = []
    current_title = "General"

    for line in lines:
        if len(line.split()) < 15 and line.istitle():
            # Treat as subsection title if it's short and title-cased
            if current_sub:
                sub_chunks.append((current_title, "\n".join(current_sub)))
                current_sub = []
            current_title = line.strip()
        else:
            current_sub.append(line)

    if current_sub:
        sub_chunks.append((current_title, "\n".join(current_sub)))

    return sub_chunks


def infer_tags(section, subsection):
    tags = []
    if "1A" in section.upper():
        tags.extend(["risk", "forward-looking"])
    if "7A" in section.upper():
        tags.extend(["financials", "market risk"])
    if "7" in section.upper():
        tags.append("MD&A")
    if any(x in subsection.lower() for x in ["liquidity", "capital"]):
        tags.append("liquidity")
    if "balance sheet" in subsection.lower():
        tags.append("balance sheet")
    if "operations" in subsection.lower():
        tags.append("operations")
    return tags or ["financial"]


def sanitize_chunk_id(section, subsection, count):
    base = f"{section.lower().replace(' ', '_').replace('.', '')}-{subsection.lower().replace(' ', '_')}-{count}"
    safe_id = re.sub(r'[^a-zA-Z0-9_\-]', '', base)
    return safe_id


def extract_chunks(section_data):
    all_chunks = []
    for idx, (section_title, lines) in enumerate(section_data):
        sub_chunks = basic_subchunk_split(section_title, lines)
        for i, (sub_title, text) in enumerate(sub_chunks):
            if len(text) < 200:
                continue

            chunk = {
                "chunk_id": sanitize_chunk_id(section_title, sub_title, i + 1),
                "section": section_title,
                "subsection": sub_title,
                "content": text,
                "tags": infer_tags(section_title, sub_title),
                "ticker": TICKER,
                "filing_type": FILING_TYPE,
                "filing_date": FILING_DATE,
                "has_table": "table" in text.lower()  # naive flag for now
            }
            all_chunks.append(chunk)
    return all_chunks


def save_chunks(chunks):
    Path("data/chunks").mkdir(parents=True, exist_ok=True)
    with open(CHUNK_SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
    print(f"\nExtracted {len(chunks)} chunks and saved to {CHUNK_SAVE_PATH}")


if __name__ == "__main__":
    print("Extracting text from HTML...")
    lines = extract_clean_text()

    print("Chunking sections and subsections...")
    sections = split_into_sections(lines)
    chunks = extract_chunks(sections)

    save_chunks(chunks)
