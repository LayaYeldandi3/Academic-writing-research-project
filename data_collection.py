# data_collection.py
import os
import re
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

def collect_papers_semanticscholar(query, limit=20):
    """
    Fetch papers from Semantic Scholar API using API key and save as CSV.
    """
    safe_query = re.sub(r"[^\w\-]", "_", query)
    csv_file = f"{safe_query}_papers.csv"

    # Semantic Scholar API URL
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,abstract,authors,year,venue,url,externalIds"

    headers = {
        "x-api-key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ API request failed. Status code: {response.status_code}")
            print("Response:", response.text)
            return

        data = response.json().get("data", [])
        if not data:
            print("⚠️ No papers found for this query.")
            return

        papers = []
        for paper in data:
            authors = ", ".join([a["name"] for a in paper.get("authors", [])])
            papers.append({
                "title": paper.get("title", ""),
                "authors": authors,
                "abstract": paper.get("abstract", ""),
                "year": paper.get("year", ""),
                "venue": paper.get("venue", ""),
                "doi": paper.get("externalIds", {}).get("DOI", ""),
                "url": paper.get("url", "")
            })

        df = pd.DataFrame(papers)
        df.to_csv(csv_file, index=False, encoding="utf-8")
        print(f"✅ CSV saved as {csv_file}")

    except Exception as e:
        print(f"❌ Error fetching papers: {e}")

def collect_papers(query, limit=20):
    """
    Wrapper function for compatibility with previous workflow.
    """
    collect_papers_semanticscholar(query, limit)
