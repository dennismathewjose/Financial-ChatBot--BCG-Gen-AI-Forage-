# SEC Financial Chatbot

A full-stack AI-powered chatbot to query and summarize financial data from SEC 10-K filings, using Ollama for embeddings, Groq LLaMA-3 for summarization, and Pinecone for semantic search.

---

## Features Implemented

### Core Capabilities
- **Natural language question answering** on financial filings
- **Semantic chunking** of SEC 10-K HTML files using section and subsection boundaries
- **Embedding-based retrieval** with `nomic-embed-text` via Ollama
- **RAG-based summarization** using `llama3-8b-8192` via Groq API
- **Fallback mechanism** if chunk content is missing or invalid
- **Streamlit web UI** for interactive Q&A
- **Auto-cleanup of summary formatting**, especially around financial figures

---

## Tech Stack

| Component         | Tool/Library                              |
|------------------|--------------------------------------------|
| Embeddings       | [Ollama](https://ollama.com) (`nomic-embed-text`) |
| Vector DB        | [Pinecone](https://www.pinecone.io/)       |
| LLM Summarizer   | [Groq](https://console.groq.com/) (`llama3-8b-8192`) |
| Web UI           | [Streamlit](https://streamlit.io/)         |
| SEC Crawler      | [Crawl4AI](https://github.com/unclecode/crawl4ai) |
| Data Processing  | BeautifulSoup, Regex, NLTK                 |
| Testing & CI     | Pytest + GitHub Actions                    |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/financial-chatbot.git
cd financial-chatbot
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set up Environment Variables
Create a .env file in the root directory and add the following:
```bash
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=financial-chatbot
OLLAMA_BASE_URL=http://localhost:11434
GROQ_API_KEY=your_groq_api_key
```
---
## How to run the pipeline

### 1. Start ollama locally
```bash
ollama run nomic-embed-text
```

### 2. Crawl and download the SEC 10-K HTML
```bash
python crawler/crawler.py
```

### 3. Format and chunk the HTML
```bash
python crawler/chunk_formatter.py
```

### 4. Embed and upload to pinecone
```bash
python -m embedding.embedder
```

### 5. Launch the streamlit chatbot
```bash
streamlit run app/app.py
```
---

## Example queries

1. What are Apple’s international market risks?
2. Summarize Apple’s liquidity and cash flow position.
3. What is the total revenue in 2023?
4. Give me the capital expenditures in the last year.
---
## Known Limitations
- Summarization may occasionally misinterpret table structure
- Some fallback extractions may produce repeated values
- Groq API key must be valid and have usage access

---
## Upcomng features
- Financial metric visualization from structured summaries
- Support for multi-filing and year-to-year comparisons
- Advanced query filtering and topic-level summaries
- Export reports as PDF/CSV
