import pandas as pd
import plotly.express as px

def load_metrics(path="data/metrics/xbrl_financial_metrics.csv"):
    df = pd.read_csv(path)
    return df

def plot_metric_trend(df, company_ticker, metric_name):
    plot_df = df[(df["ticker"] == company_ticker) & (df["metric"] == metric_name)]
    plot_df = plot_df.groupby(["fiscal_year"])["value"].mean().reset_index()
    fig = px.line(
        plot_df, 
        x="fiscal_year", y="value", markers=True,
        title=f"{metric_name} Trend for {company_ticker}",
        labels={"value": metric_name, "fiscal_year": "Fiscal Year"}
    )
    return fig

def plot_metric_comparison(df, metric_name, chart_type='bar'):
    plot_df = df[df["metric"] == metric_name].groupby(["ticker", "fiscal_year"])["value"].mean().reset_index()

    if chart_type == "line":
        fig = px.line(
            plot_df, 
            x="fiscal_year", y="value", color="ticker", markers=True,
            title=f"{metric_name} Comparison",
            labels={"value": metric_name, "fiscal_year": "Fiscal Year"}
        )
    elif chart_type == "bar":
        fig = px.bar(
            plot_df, 
            x="fiscal_year", y="value", color="ticker", barmode="group",
            title=f"{metric_name} Comparison",
            labels={"value": metric_name, "fiscal_year": "Fiscal Year"}
        )
    elif chart_type == "pie":
        latest_year = plot_df["fiscal_year"].max()
        pie_df = plot_df[plot_df["fiscal_year"] == latest_year]
        fig = px.pie(
            pie_df, names="ticker", values="value",
            title=f"{metric_name} ({latest_year}) - Cross-Company"
        )
    else:
        # Default to bar chart
        fig = px.bar(
            plot_df, 
            x="fiscal_year", y="value", color="ticker", barmode="group",
            title=f"{metric_name} Comparison",
            labels={"value": metric_name, "fiscal_year": "Fiscal Year"}
        )
    
    return fig
