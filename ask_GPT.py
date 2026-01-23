import json
import pandas as pd
from config import MODEL, SCENARIOS, MEASURES_FILE, OUTPUT_DIR
import re
import hashlib
from openai import OpenAI
import time
import os

# Initialize client
client = OpenAI()

# Read system context
with open("prompts/system_context.txt", "r", encoding="utf-8") as f:
    SYSTEM_CONTEXT = f.read()

# Read measures CSV
measures = pd.read_csv(MEASURES_FILE)

# Load cache if it exists
cache_file = f"{OUTPUT_DIR}/prompt_cache.json"
if os.path.exists(cache_file):
    print(f"The cache {cache_file} exists." )
    with open(cache_file, "r", encoding="utf-8") as f:
        prompt_cache = json.load(f)
else:
    prompt_cache = {}

print(f"Prompt cache: {prompt_cache}")
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

        # Generate unique short ID
        raw_id = f"{row['area']}|{row['tema']}|{row['scenario']}|{test_scenario}"
        short_id = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()[:16]
        custom_id = short_id

        # Use prompt hash as cache key
        prompt_hash = hashlib.sha1(prompt.encode("utf-8")).hexdigest()

        if prompt_hash in prompt_cache:
            output_text = prompt_cache[prompt_hash]
            log_msg = "[CACHE HIT]"
        else:
            resp = client.responses.create(
                model=MODEL,
                input=[{"role": "system", "content": SYSTEM_CONTEXT},
                    {"role": "user", "content": prompt}]
            )
            output_text = resp.output_text
            prompt_cache[prompt_hash] = output_text
            log_msg = "[API CALL]"

        print(f"{log_msg} {custom_id}")

        responses.append({
            "custom_id": custom_id,
            "response": output_text
        })

# Save all responses
output_file = f"{OUTPUT_DIR}/responses.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(responses, f, ensure_ascii=False, indent=2)

# Save updated cache
with open(cache_file, "w", encoding="utf-8") as f:
    json.dump(prompt_cache, f, ensure_ascii=False, indent=2)

print(f"All done! Responses saved to {output_file}")