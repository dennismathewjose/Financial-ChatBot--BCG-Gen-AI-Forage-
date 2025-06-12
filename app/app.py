import streamlit as st
import traceback
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.retriever import retrieve_relevant_chunks
from backend.summarizer import summarize_text, summarize_with_fallback, clean_summary_output
from backend.graph_generator import load_metrics, plot_metric_trend, plot_metric_comparison

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
# Load metrics CSV once
metrics_df = load_metrics()

#Visualization Section

# Let user pick metric to visualize
metric_options = metrics_df["metric"].unique().tolist()
selected_metric = st.selectbox("Select a metric:", metric_options)

# Create two columns side by side
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Company Trend")
    fig1 = plot_metric_trend(metrics_df, selected_ticker, selected_metric)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Cross-Company Comparison")
    fig2 = plot_metric_comparison(metrics_df, selected_metric)
    st.plotly_chart(fig2, use_container_width=True)