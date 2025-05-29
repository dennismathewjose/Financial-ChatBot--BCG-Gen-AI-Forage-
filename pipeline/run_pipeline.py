import subprocess
import concurrent.futures

def run_step(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {command}")

def run_pipeline():
    print("Starting full ingestion pipeline...")

    # Step 1: Crawl
    run_step("python crawler/crawler.py")

    # Step 2: Run chunking and xbrl in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(run_step, "python crawler/chunk_formatter.py"),
            executor.submit(run_step, "python metrics/xbrl_financial_metrics.py")
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")
                raise

    # Step 3: Embedding
    run_step("python -m embedding.embedder")

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
