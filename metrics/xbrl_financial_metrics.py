# metrics/xbrl_financial_metrics.py

import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# Constants
COMPANIES = {
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "AMZN": "0001018724"
}

METRICS = {
    "Revenues": "Total Revenue",
    "NetIncomeLoss": "Net Income",
    "CashAndCashEquivalentsAtCarryingValue": "Cash Flow",
    "Assets": "Total Assets",
    "Liabilities": "Total Liabilities"
}

SEC_API_URL = "https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{metric}.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Financial Chatbot by Dennis)"
}

# Output path
METRIC_DIR = Path("data/metrics")
METRIC_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV = METRIC_DIR / "xbrl_financial_metrics.csv"

def fetch_and_save_metrics():
    all_data = []

    for ticker, cik in COMPANIES.items():
        for metric_tag, label in METRICS.items():
            url = SEC_API_URL.format(cik=cik, metric=metric_tag)
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("units", {}).get("USD", []):
                    if item.get("form") == "10-K" and item.get("fy"):
                        all_data.append({
                            "ticker": ticker,
                            "fiscal_year": item.get("fy"),
                            "filed_date": item.get("filed"),
                            "metric": label,
                            "value": item.get("val")
                        })

    df = pd.DataFrame(all_data)
    df = df[df["fiscal_year"].between(datetime.now().year - 3, datetime.now().year - 1)]
    df_sorted = df.sort_values(by=["ticker", "fiscal_year", "filed_date"], ascending=[True, True, False])
    df_deduped = df_sorted.drop_duplicates(subset=["ticker", "fiscal_year", "metric"], keep="first")

    df_deduped.to_csv(OUTPUT_CSV, index=False)
    print(f"XBRL metrics saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    fetch_and_save_metrics()
