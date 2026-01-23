from openai import OpenAI
import os

print("DOWNLOAD SCRIPT STARTED")

BATCH_ID = "batch_697350963c748190b9387267ba2cb739"
OUTPUT_DIR = "output"
OUTPUT_FILE = f"{OUTPUT_DIR}/batch_output.jsonl"

client = OpenAI()

os.makedirs(OUTPUT_DIR, exist_ok=True)

batch = client.batches.retrieve(BATCH_ID)

print("STATUS:", batch.status)
print("ERROR FILE ID:", batch.error_file_id)
print("OUTPUT FILE ID:", batch.output_file_id)
print("REQUEST COUNTS:", batch.request_counts)

print("Batch status:", batch.status)

if batch.status == "failed":
    print("Error file id:", batch.error_file_id)

if batch.status == "failed" and batch.error_file_id:
    error_bytes = client.files.content(batch.error_file_id)
    print(error_bytes.decode("utf-8"))

if not batch.output_file_id:
    raise RuntimeError("Batch completed but no output_file_id found.")

content = client.files.content(batch.output_file_id)

with open(OUTPUT_FILE, "wb") as f:
    f.write(content)

print(f"Batch output downloaded to {OUTPUT_FILE}")