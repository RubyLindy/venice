import pandas as pd
from config import CONTEXT_FILES

def df_to_text(df, title):
    return f"\n### {title}\n" + df.to_csv(index=False)

def build_context():
    parts = []

    for title, path in CONTEXT_FILES.items():
        df = pd.read_csv(path)
        parts.append(df_to_text(df, title.upper()))

    return "\n".join(parts)

if __name__ == "__main__":
    context = build_context()
    with open("prompts/system_context.txt", "w", encoding="utf-8") as f:
        f.write(context)

    print("System context written to prompts/system_context.txt")