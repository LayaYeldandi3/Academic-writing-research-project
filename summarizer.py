# from transformers import pipeline
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor
# summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
# def summarize_text(text):
#     text = text[:2000]  # Truncate to avoid excessive time on long abstracts
#     return summarizer(text, max_length=50, min_length=50, do_sample=False)[0]['summary_text']

# def summarize_csv(file_path):
#     df = pd.read_csv(file_path)
#     if 'abstract' not in df.columns:
#         raise ValueError("CSV does not have an 'abstract' column")
    
#     abstracts = df['abstract'].fillna("").tolist()

#     # Parallelize summarization across CPU cores
#     with ThreadPoolExecutor() as executor:
#         summaries = list(executor.map(summarize_text, abstracts))

#     df['summary'] = summaries
#     output_path = file_path.replace(".csv", "_summarized.csv")
#     df.to_csv(output_path, index=False)
#     print(f"✅ Summaries saved to {output_path}")

# if __name__ == "__main__":
#     file_path = input("Enter CSV file path: ")
#     summarize_csv(file_path)
# summarizer.py

from transformers import pipeline
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# ✅ Use a lighter model for faster processing
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    """
    Summarize a single abstract safely.
    """
    if not isinstance(text, str) or text.strip() == "":
        return "⚠ No abstract available for summarization."
    
    # Truncate long text to avoid long processing times
    text = text[:2000]  
    try:
        summary = summarizer(text, max_length=60, min_length=50, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        return f"⚠ Error summarizing: {e}"

def summarize_csv(file_path):
    """
    Summarize abstracts from a CSV and save a new CSV with summaries.
    """
    df = pd.read_csv(file_path)
    
    if 'abstract' not in df.columns:
        raise ValueError("CSV does not have an 'abstract' column")
    
    abstracts = df['abstract'].fillna("").tolist()

    # ✅ Parallelize summarization across CPU cores
    with ThreadPoolExecutor() as executor:
        summaries = list(executor.map(summarize_text, abstracts))

    df['summary'] = summaries
    output_path = file_path.replace(".csv", "_summarized.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Summaries saved to {output_path}")
