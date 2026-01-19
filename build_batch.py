import json
import pandas as pd
from config import MODEL, SCENARIOS, MEASURES_FILE, OUTPUT_DIR

with open("prompts/system_context.txt", "r", encoding="utf-8") as f:
    SYSTEM_CONTEXT = f.read()

measures = pd.read_csv(MEASURES_FILE)

requests = []

for _, row in measures.iterrows():
    for scenario in SCENARIOS:
        prompt = f"""
Considera il contesto fornito (scenari, aree di studio, relazione area–scenario).

MISURA:
"{row.measure_text}"

AREA: {row.area}
SCENARIO: {scenario}
TEMA: {row.topic}

1) La misura è compatibile con questo scenario?
   Rispondi esclusivamente con "yes" o "no" e fornisci una breve motivazione
   (circa 100 parole).

2) Per questo scenario, quali criticità potrebbero emergere nell’applicazione
   della misura e che andrebbero verificate?
   (circa 100 parole).

Fornisci l’output esclusivamente in formato JSON con i seguenti campi:
area, scenario, topic, measure_text, compatibility, motivation, critical_issues.
"""

        requests.append({
            "custom_id": f"{row.area}_{row.topic}_{scenario}",
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

with open(output_path, "w", encoding="utf-8") as f:
    for r in requests:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"Batch input written to {output_path}")