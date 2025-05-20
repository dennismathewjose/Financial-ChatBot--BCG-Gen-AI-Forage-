import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

RAW_DIR = Path("data/raw")
CHUNK_DIR = Path("data/chunks")
CHUNK_SAVE_PATH = CHUNK_DIR / "sample_chunks.json"

def extract_clean_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for tag in soup(["script", "style", "footer", "nav"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines

def split_into_sections(lines):
    section_indices = [(i, line.strip()) for i, line in enumerate(lines) if re.match(r"^(ITEM|Item)\s+\d{1,2}[A]?\.?", line.strip())]
    section_chunks = []
    for idx in range(len(section_indices) - 1):
        start_idx, section_title = section_indices[idx]
        end_idx, _ = section_indices[idx + 1]
        section_lines = lines[start_idx + 1:end_idx]
        section_chunks.append((section_title, section_lines))
    return section_chunks

def basic_subchunk_split(lines):
    sub_chunks = []
    current_sub = []
    current_title = "General"
    for line in lines:
        if len(line.split()) < 15 and line.istitle():
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
    if "1A" in section.upper(): tags.extend(["risk", "forward-looking"])
    if "7A" in section.upper(): tags.extend(["financials", "market risk"])
    if "7" in section.upper(): tags.append("MD&A")
    if any(x in subsection.lower() for x in ["liquidity", "capital"]): tags.append("liquidity")
    if "balance sheet" in subsection.lower(): tags.append("balance sheet")
    if "operations" in subsection.lower(): tags.append("operations")
    return tags or ["financial"]

def sanitize_chunk_id(section, subsection, count, ticker):
    base = f"{ticker.lower()}_{section.lower().replace(' ', '_').replace('.', '')}-{subsection.lower().replace(' ', '_')}-{count}"
    return re.sub(r'[^a-zA-Z0-9_\-]', '', base)

def parse_filename(file_path):
    # Expect filename like: aapl_10-k_2023-09-30.html
    name = file_path.stem
    parts = name.split("_")
    return parts[0].upper(), parts[1].upper(), parts[2]

def extract_chunks(section_data, ticker, filing_type, filing_date):
    all_chunks = []
    for section_title, lines in section_data:
        sub_chunks = basic_subchunk_split(lines)
        for i, (sub_title, text) in enumerate(sub_chunks):
            if len(text) < 200:
                continue
            chunk = {
                "chunk_id": sanitize_chunk_id(section_title, sub_title, i + 1, ticker),
                "section": section_title,
                "subsection": sub_title,
                "content": text,
                "tags": infer_tags(section_title, sub_title),
                "ticker": ticker,
                "filing_type": filing_type,
                "filing_date": filing_date,
                "has_table": "table" in text.lower()
            }
            all_chunks.append(chunk)
    return all_chunks

def process_all_filings():
    all_chunks = []
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)

    for file in RAW_DIR.glob("*.html"):
        print(f"\nProcessing {file.name}")
        try:
            ticker, filing_type, filing_date = parse_filename(file)
            lines = extract_clean_text(file)
            sections = split_into_sections(lines)
            chunks = extract_chunks(sections, ticker, filing_type, filing_date)
            all_chunks.extend(chunks)
            print(f"Extracted {len(chunks)} chunks from {file.name}")
        except Exception as e:
            print(f"Failed to process {file.name}: {e}")

    with open(CHUNK_SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)
    print(f"\nTotal extracted chunks: {len(all_chunks)}")
    print(f"Saved to {CHUNK_SAVE_PATH}")

if __name__ == "__main__":
    print("🔍 Extracting from all filings...")
    process_all_filings()
