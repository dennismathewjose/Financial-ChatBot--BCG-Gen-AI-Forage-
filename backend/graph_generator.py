# backend/graph_generator.py
import pandas as pd
import plotly.express as px

# Load the metrics CSV once (can be called in app.py init or inside a function)
METRICS_CSV_PATH = "data/metrics/xbrl_financial_metrics.csv"

def load_metrics():
    df = pd.read_csv(METRICS_CSV_PATH)
    return df

def plot_metric_trend(df, ticker, metric_name):
    df_filtered = df[(df["ticker"] == ticker) & (df["metric"] == metric_name)]
    df_filtered = df_filtered.sort_values(by="fiscal_year")

    # Plot
    fig = px.line(
        df_filtered,
        x="fiscal_year",
        y="value",
        markers=True,
        title=f"{metric_name} trend for {ticker}"
    )
    return fig

def plot_metric_comparison(df, metric_name):
    df_filtered = df[df["metric"] == metric_name]
    df_filtered = df_filtered.sort_values(by=["ticker", "fiscal_year"])

    fig = px.line(
        df_filtered,
        x="fiscal_year",
        y="value",
        color="ticker",
        markers=True,
        title=f"{metric_name} comparison across companies"
    )
    return fig
