"""Utilities for article extraction and metadata."""

import pandas as pd
from newspaper import Article

def extract_full_text(url):
    """Extract the full text content from a news article URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except Exception as e:
        print(f"❌ Failed to extract article text: {e}")
        return None

def load_allsides_data():
    """Load and prepare AllSides media bias dataset."""
    url = "https://raw.githubusercontent.com/favstats/AllSideR/master/data/allsides_data.csv"
    df = pd.read_csv(url)
    df["news_source_clean"] = df["news_source"].str.lower().str.strip()
    df["screen_name_clean"] = df["screen_name"].fillna("").str.lower().str.strip()
    return df

def find_allsides_metadata(source_name, allsides_df):
    """Find bias metadata for a news source from AllSides dataset."""
    name = source_name.lower().strip()
    match = allsides_df[
        (allsides_df["news_source_clean"].str.contains(name, na=False)) |
        (allsides_df["screen_name_clean"].str.contains(name, na=False))
    ]
    if not match.empty:
        row = match.iloc[0]
        return {
            "rating": row.get("rating", "Unknown"),
            "confidence": row.get("confidence_level", "Unknown"),
            "perc_agree": f"{round(row.get('perc_agree', 0.0) * 100, 1)}%" if pd.notna(row.get("perc_agree")) else "Unknown",
            "type": row.get("type", "Unknown"),
            "allsides_url": row.get("url", None)
        }
    return {
        "rating": "Unknown",
        "confidence": "Unknown",
        "perc_agree": "Unknown",
        "type": "Unknown",
        "allsides_url": None
    }