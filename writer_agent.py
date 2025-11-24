import pandas as pd
from insight_agent import ask_openrouter

def generate_related_work(file_path, output_file="related_work.md"):
    df = pd.read_csv(file_path)
    all_insights = "\n\n".join(df['insights_hypotheses'].dropna().tolist())
    prompt = f"Using the following research insights, write a 300-word 'Related Work' section for an academic paper:\n\n{all_insights}"
    related_work = ask_openrouter(prompt)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(related_work)
    print(f"✅ Related Work section saved to {output_file}")

if __name__ == "_main_":
    file_path = input("Enter insights CSV file path: ")
    generate_related_work(file_path)