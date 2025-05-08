# scraper/scraper.py

import os
from sec_edgar_downloader import Downloader

def download_filings(ticker: str, form_type: str, after: str = "2021-01-01"):
    """
    Downloads filings from SEC EDGAR and returns list of downloaded file paths.
    """
    dl = Downloader(
        company_name="BCG GenAI Forage Financial Chatbot",
        email_address="dennismjose26@yahoo.com"
    )
    dl.get(form_type, ticker, after=after)

    folder = f"sec-edgar-filings/{ticker}/{form_type}"
    if not os.path.exists(folder):
        raise FileNotFoundError("No filings downloaded.")

    # Get latest filing paths
    filing_dirs = sorted(os.listdir(folder), reverse=True)
    files = []
    for d in filing_dirs:
        path = os.path.join(folder, d, "full-submission.txt")
        if os.path.exists(path):
            files.append(path)

    return files
