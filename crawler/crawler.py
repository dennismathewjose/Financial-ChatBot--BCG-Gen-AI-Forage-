import asyncio
from crawl4ai import AsyncWebCrawler
from pathlib import Path
import nest_asyncio

# Add all companies and their filing URLs here
filings = [
    {
        "ticker": "AAPL",
        "filing_type": "10-K",
        "filing_date": "2023-09-30",
        "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"
    },
    {
        "ticker": "MSFT",
        "filing_type": "10-K",
        "filing_date": "2023-06-30",
        "url": "https://www.sec.gov/Archives/edgar/data/789019/000095017024087843/msft-20240630.htm"
    },
    {
        "ticker": "AMZN",
        "filing_type": "10-K",
        "filing_date": "2023-12-31",
        "url": "https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm"
    }
]

async def crawl_and_save():
    async with AsyncWebCrawler() as crawler:
        for filing in filings:
            ticker = filing["ticker"]
            ftype = filing["filing_type"]
            fdate = filing["filing_date"]
            url = filing["url"]

            save_path = f"data/raw/{ticker.lower()}_{ftype.lower()}_{fdate}.html"
            print(f"\nCrawling {ticker} {ftype} ({fdate})...")

            result = await crawler.arun(url=url)
            if result and result.success:
                Path("data/raw").mkdir(parents=True, exist_ok=True)
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(result.html)
                print(f"Saved to {save_path}")
            else:
                print(f"Failed to crawl {ticker}: {result.error_message if result else 'Unknown error'}")

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(crawl_and_save())
