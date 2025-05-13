import asyncio
from crawl4ai import AsyncWebCrawler
from pathlib import Path
import nest_asyncio # Import nest_asyncio

URL = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"
SAVE_PATH = "data/raw/aapl_10k_2023.html"

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=URL)
        if result and result.success:
            Path("data/raw").mkdir(parents=True, exist_ok=True)
            with open(SAVE_PATH, "w", encoding="utf-8") as f:
                f.write(result.html)
            print(f"Saved HTML to {SAVE_PATH}")
        else:
            print(f"Failed to crawl the page: {result.error_message if result else 'Unknown error'}")

# Instead of asyncio.run, use the following to execute the coroutine within the existing event loop:
if __name__ == "__main__":
    nest_asyncio.apply() # Apply nest_asyncio to allow nested event loops
    asyncio.get_event_loop().run_until_complete(main()) # Use the existing event loop