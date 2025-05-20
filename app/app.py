import streamlit as st
import traceback
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.retriever import retrieve_relevant_chunks
from backend.summarizer import summarize_text, summarize_with_fallback, clean_summary_output

st.set_page_config(page_title="SEC Financial Chatbot", layout="wide")
st.title("SEC Financial Chatbot")
st.write("Ask questions about SEC 10-K filings. Powered by Ollama + Groq.")

# Step 1: Company Selector
company_map = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN"
}

selected_company = st.selectbox("Select a company:", list(company_map.keys()))
selected_ticker = company_map[selected_company]

query = st.text_input("Enter your financial question:")

if query:
    with st.spinner("Retrieving relevant chunks..."):
        chunks = retrieve_relevant_chunks(query, top_k=3, namespace=selected_ticker)

    if not chunks:
        st.warning("No relevant information found.")
    else:
        SHOW_CONTEXT = False
        if SHOW_CONTEXT:
            with st.expander("Retrieved Context"):
                for i, chunk in enumerate(chunks):
                    st.markdown(f"**Chunk {i+1}: {chunk['section']} - {chunk['subsection']}**")
                    st.code(chunk['content'][:1000] + "...")

        # Use top-1 chunk
        selected_chunk = chunks[0]

        with st.spinner("Generating summary with LLaMA..."):
            try:
                if selected_chunk["content"] != "N/A":
                    summary = summarize_text(selected_chunk["content"], query=query)
                else:
                    # Pass the ticker for fallback logic
                    summary = summarize_with_fallback(query=query, namespace=selected_ticker)

                summary = clean_summary_output(summary)
                st.subheader("Summary")
                st.markdown(summary)

            except Exception as e:
                st.error("Failed to summarize due to API error.")
                st.code(traceback.format_exc())
