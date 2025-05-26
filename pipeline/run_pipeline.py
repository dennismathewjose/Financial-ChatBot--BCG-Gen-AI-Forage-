# pipeline/run_pipeline.py
import subprocess

def run_step(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {command}")

if __name__ == "__main__":
    print("Starting full ingestion pipeline...")

    run_step("python crawler/crawler.py")
    run_step("python crawler/chunk_formatter.py")
    run_step("python -m embedding.embedder")  # safer with -m for relative imports

    print("Pipeline complete.")
