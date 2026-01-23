from openai import OpenAI
from config import BATCH_COMPLETION_WINDOW

client = OpenAI()

file = client.files.create(
    file=open("output/batch_input.jsonl", "rb"),
    purpose="batch"
)

print("Uploaded file ID:", file.id)

batch = client.batches.create(
    input_file_id=file.id,
    endpoint="/v1/responses",
    completion_window=BATCH_COMPLETION_WINDOW
)

print(batch)

print("Batch submitted")
print("Batch ID:", batch.id)