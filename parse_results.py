import json

INPUT_FILE = "output/batch_output.jsonl"
OUTPUT_FILE = "output/final_results.jsonl"

results = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        record = json.loads(line)
        content = record["response"]["output_text"]
        results.append(json.loads(content))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for r in results:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("Final results written to", OUTPUT_FILE)