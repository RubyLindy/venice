import json
import pandas as pd
from config import MODEL, SCENARIOS, MEASURES_FILE, OUTPUT_DIR
import re
import hashlib

with open("prompts/system_context.txt", "r", encoding="utf-8") as f:
    SYSTEM_CONTEXT = f.read()

measures = pd.read_csv(MEASURES_FILE)

requests = []

for _, row in measures.iterrows():
    for test_scenario in SCENARIOS:
        prompt = f"""
Considera il contesto fornito (scenari, aree di studio, relazione area–scenario).

MISURA:
"{row['misura']}"

AREA: {row['area']}
SCENARIO: {row['scenario']}
TEMA: {row['tema']}

MOTIVAZIONE (contesto aggiuntivo):
"{row['motivazione']}"

1) La misura è compatibile con questo scenario?
   Rispondi esclusivamente con "yes" o "no" e fornisci una breve motivazione
   (circa 100 parole).

2) Per questo scenario, quali criticità potrebbero emergere nell’applicazione
   della misura e che andrebbero verificate?
   (circa 100 parole).

Fornisci l’output esclusivamente in formato JSON con i seguenti campi:
area, scenario, topic, measure_text, compatibility, motivation, critical_issues.
"""
        
        raw_id = f"{row['area']}|{row['tema']}|{row['scenario']}|{test_scenario}"
        short_id = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()[:16]

        custom_id = short_id

        requests.append({
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/responses",
            "body": {
                "model": MODEL,
                "input": [
                    {"role": "system", "content": SYSTEM_CONTEXT},
                    {"role": "user", "content": prompt}
                ]
            }
        })

output_path = f"{OUTPUT_DIR}/batch_input.jsonl"

print("Number of batch requests:", len(requests))

if len(requests) == 0:
    raise RuntimeError("No batch requests generated — CSV parsing logic is wrong.")

with open(output_path, "w", encoding="utf-8") as f:
    for r in requests:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"Batch input written to {output_path}")