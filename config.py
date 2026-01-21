MODEL = "gpt-4.1-mini"

SCENARIOS = [
    "Slow Pace",
    "Nature@Work",
    "Blue Development"
]

BATCH_COMPLETION_WINDOW = "24h"

CONTEXT_FILES = {
    "scenari": "data/scenari.csv",
    "aree": "data/aree_di_studio.csv",
    "area_scenario": "data/AreaXscenario.csv"
}

MEASURES_FILE = "data/misure.csv"

OUTPUT_DIR = "output"