import json
from tqdm import tqdm
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraper.scraper import download_filings
from embedding.cleaner import clean_text

def get_embedding(text: str, model: str = "nomic-embed-text"):
    return [0.0] * 384

def simple_chunk(text, chunk_size=700):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i+chunk_size])

def process_company(ticker, form_types=["10-K"], after_date="2022-01-01"):
    for form in form_types:
        print(f"→ Downloading {form} filings for {ticker}")
        files = download_filings(ticker, form, after=after_date)
        print(f"✔️ Found {len(files)} files for {ticker}")

        for file_path in files:
            print(f"📄 Reading: {file_path}")
            year = file_path.split("/")[-2].split("-")[1][:4]

            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            print(f"🧼 Raw length: {len(raw_text)}")

            cleaned = clean_text(raw_text)
            print(f"✅ Cleaned length: {len(cleaned)}")

            for i, chunk in enumerate(simple_chunk(cleaned)):
                print(f"🔹 Chunk {i} - {len(chunk)} words")
                embedding = get_embedding(chunk)
                yield {
                    "text": chunk,
                    "embedding": embedding,
                    "metadata": {
                        "ticker": ticker,
                        "year": year,
                        "form_type": form,
                        "chunk_id": i
                    }
                }

if __name__ == "__main__":
    os.makedirs("preloaded_embeddings", exist_ok=True)
    companies = ["AAPL", "MSFT", "TSLA"]

    for ticker in companies:
        output_path = f"preloaded_embeddings/{ticker}_embeddings.jsonl"
        print(f"\nStarting {ticker}")
        count = 0
        with open(output_path, "w", encoding="utf-8") as f:
            for item in tqdm(process_company(ticker), desc=f"Processing {ticker}"):
                f.write(json.dumps(item) + "\n")
                count += 1
        print(f"✅Done: {ticker} → {count} chunks written to {output_path}")
