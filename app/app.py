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

metrics_df = load_metrics()
metric_options = metrics_df["metric"].unique().tolist()

# Section header
st.subheader("Financial Metrics Visualization")

# Selection box with "All" option
selected_metric = st.selectbox("Select a metric (leave empty to show all):", ["All"] + metric_options)

# Helper function to choose chart type
def choose_chart_type(metric_name):
    if "Revenue" in metric_name:
        return "line"
    elif "Income" in metric_name:
        return "line"
    elif "Cash Flow" in metric_name:
        return "bar"
    elif "Assets" in metric_name:
        return "bar"
    elif "Liabilities" in metric_name:
        return "pie"
    else:
        return "bar"

if selected_metric == "All":
    st.write("Showing all available metrics across companies...")
    
    # Displaying 2 charts per row
    metrics_to_plot = metric_options
    num_cols = 2
    rows = (len(metrics_to_plot) + num_cols - 1) // num_cols
    
    for row in range(rows):
        cols = st.columns(num_cols)
        for i in range(num_cols):
            idx = row * num_cols + i
            if idx >= len(metrics_to_plot):
                break
            metric_name = metrics_to_plot[idx]
            chart_type = choose_chart_type(metric_name)
            
            with cols[i]:
                st.markdown(f"#### {metric_name}")
                
                # Cross-company comparison for simplicity
                fig = plot_metric_comparison(metrics_df, metric_name, chart_type=chart_type)
                st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown(f"### Showing '{selected_metric}' for {selected_company}")
    
    # (company trend + cross-company Analysis)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Company Trend")
        fig1 = plot_metric_trend(metrics_df, selected_ticker, selected_metric)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("#### Cross-Company Comparison")
        fig2 = plot_metric_comparison(metrics_df, selected_metric)
        st.plotly_chart(fig2, use_container_width=True)
