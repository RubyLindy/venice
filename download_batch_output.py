import time
import json
from openai import OpenAI

client = OpenAI()

BATCH_ID = "batch_6973674bb43c8190ba52af2243a3c5b7"
POLL_INTERVAL = 10

def wait_for_batch(batch_id):
    while True:
        batch = client.batches.retrieve(batch_id)
        status = batch.status
        print(f"Batch status: {status}, completed={batch.request_counts.completed}, failed={batch.request_counts.failed}")
        
        if status in ["completed", "failed", "cancelled", "expired"]:
            return batch
        time.sleep(POLL_INTERVAL)

def download_batch_output(batch):
    if batch.output_file_id:
        output_file = client.files.retrieve(batch.output_file_id)
        output_content = client.files.download(output_file.id)
        with open("batch_output.jsonl", "wb") as f:
            f.write(output_content)
        print("Batch output downloaded to batch_output.jsonl")
    elif batch.error_file_id:
        error_file = client.files.retrieve(batch.error_file_id)
        error_content = client.files.download(error_file.id)
        with open("batch_errors.jsonl", "wb") as f:
            f.write(error_content)
        print("Batch errors downloaded to batch_errors.jsonl")
    else:
        print("No output or error file found for this batch.")

if __name__ == "__main__":
    print("Waiting for batch to complete...")
    batch = wait_for_batch(BATCH_ID)
    download_batch_output(batch)