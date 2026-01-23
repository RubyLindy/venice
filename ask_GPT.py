import json
import pandas as pd
from config import MODEL, SCENARIOS, MEASURES_FILE, OUTPUT_DIR
import hashlib
from openai import OpenAI
import os
import time

# Initialize client
client = OpenAI()

with open("prompts/system_context.txt", "r", encoding="utf-8") as f:
    SYSTEM_CONTEXT = f.read()

measures = pd.read_csv(MEASURES_FILE)

# Store responses
responses = []

for _, row in measures.iterrows():
    for test_scenario in SCENARIOS:
        # Build prompt
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
        custom_id = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()[:16]

        prompt_hash = hashlib.sha1(prompt.encode("utf-8")).hexdigest()

        print(f"[API CALL] {prompt_hash}")
        resp = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": SYSTEM_CONTEXT},
                {"role": "user", "content": prompt}
            ]
        )
        output_text = resp.output_text
        time.sleep(0.5)  # optional delay

        # Save the response
        responses.append({
            "custom_id": custom_id,
            "response": output_text
        })

# Save responses
output_file = f"{OUTPUT_DIR}/responses.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(responses, f, ensure_ascii=False, indent=2)

print(f"All done! Responses saved to {output_file}")