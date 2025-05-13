
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

query = st.text_input("Enter your financial question:")

if query:
    with st.spinner("Retrieving relevant chunks..."):
        chunks = retrieve_relevant_chunks(query, top_k=3)

    if not chunks:
        st.warning("No relevant information found.")
    else:
        SHOW_CONTEXT = False
        if SHOW_CONTEXT:
            with st.expander("Retrieved Context"):
                for i, chunk in enumerate(chunks):
                    st.markdown(f"**Chunk {i+1}: {chunk['section']} - {chunk['subsection']}**")
                    st.code(chunk['content'][:1000] + "...")

        # Select first chunk (top-1) for direct summarization
        selected_chunk = chunks[0]  # always use top-1

        with st.spinner("Generating summary with LLaMA..."):
            try:
                if selected_chunk["content"] != "N/A":
                    # Standard summarization
                    summary = summarize_text(selected_chunk["content"], query=query)
                else:
                    # Fallback to alternative chunks
                    summary = summarize_with_fallback(query)

                summary = clean_summary_output(summary)
                st.subheader("Summary")
                st.markdown(summary)

            except Exception as e:
                st.error("Failed to summarize due to API error.")
                st.code(traceback.format_exc())
