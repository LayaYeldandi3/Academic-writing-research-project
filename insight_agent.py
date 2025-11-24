import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# Load OpenRouter API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Config
# UPDATED MODEL: Switching to a different, reliable free model to bypass the DeepSeek 404 error.
MODEL_NAME = "mistralai/mistral-7b-instruct:free"
MAX_RETRIES = 5 # number of retries on 429
RETRY_DELAY = 10  # seconds to wait between retries

def ask_openrouter(prompt):
    """
    Makes a request to the OpenRouter API with retry logic and robust error handling.
    Always returns a string (either the LLM response or an error message).
    """
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        if response.status_code == 200:
            try:
                # Extract content from the standard OpenRouter response structure
                return response.json()["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                # If extraction fails, log the issue and return a specific error string
                print(f"❌ API Error: Successful status code (200), but could not parse response JSON. Full response: {response.text}")
                return "[[API_ERROR: 200 - Could not parse response]]"
        
        elif response.status_code == 429:
            print(f"⚠ Rate limited. Retry {attempt}/{MAX_RETRIES} after {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
        
        else:
            # Handle all other errors (like 404 from DeepSeek) by returning an error string
            try:
                error_message = response.json().get('error', {}).get('message', 'Unknown Error')
            except requests.exceptions.JSONDecodeError:
                error_message = response.text
                
            print(f"❌ API Error {response.status_code}: {error_message}")
            return f"[[API_ERROR: {response.status_code} - {error_message}]]"
            
    # If all retries fail, return a final error string
    print("❌ Max retries exceeded. Skipping this prompt.")
    return "[[API_ERROR: Max retries exceeded]]"

def generate_insights(file_path):
    df = pd.read_csv(file_path)
    insights = []

    for i, summary in enumerate(df.get('summary', []), start=1):
        if isinstance(summary, str) and summary.strip():
            # Prompt the model to provide structure for better parsing/readability
            prompt = f"Based on this literature summary, format your output with clear headings:\n\nSummary:\n{summary}\n\n1. Key Insights (3 points)\n2. Research Hypothesis (1 point)"
            print(f"📝 Processing row {i}/{len(df)}...")
            result = ask_openrouter(prompt)
            insights.append(result if result else "")
        else:
            # If summary is empty/invalid, append an empty string
            insights.append("")

    df['insights_hypotheses'] = insights
    output_file = file_path.replace(".csv", "_insights.csv")
    df.to_csv(output_file, index=False)
    print(f"✅ Insights generated and saved to {output_file}")

if __name__ == "_main_":
    file_path = input("Enter summarized CSV file path: ")
    generate_insights(file_path)