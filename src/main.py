"""Main execution module for the news bias analysis project."""

import requests
from collections import Counter

# Import from local modules
from api_setup import api_keys
from article_utils import extract_full_text, load_allsides_data, find_allsides_metadata
from analysis import summarize_with_gemini_http, analyze_bias_with_together_ai
from visualization import print_bias_summary

def fetch_news_articles(topic, max_articles=25):
    """Fetch news articles on a specific topic."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "language": "en",
        "pageSize": max_articles,
        "sortBy": "relevancy",
        "apiKey": api_keys['newsapi']
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("articles", [])
        else:
            print(f"Failed to fetch news. Status: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def main():
    """Main execution function."""
    print("--News Bias Analysis Tool--")
    print("--------------------------")
    
    # Get user input for news topic
    topic = input("Enter a news topic to search: ")
    
    # Load AllSides data for bias ratings
    print("Loading media bias data...")
    allsides_df = load_allsides_data()
    
    # Fetch news articles
    print(f"Fetching articles about '{topic}'...")
    articles = fetch_news_articles(topic)
    
    if not articles:
        print("No articles found.")
        return
    
    # Process and analyze articles
    seen_sources = set()
    leaning_tally = []
    count = 0
    
    print(f"\nFound {len(articles)} articles. Analyzing up to 6 unique sources:")
    
    for idx, article in enumerate(articles, 1):
        source_name = article["source"]["name"]
        
        # Skip duplicate sources
        if source_name in seen_sources:
            continue
        
        seen_sources.add(source_name)
        count += 1
        
        # Get bias metadata
        metadata = find_allsides_metadata(source_name, allsides_df)
        
        print(f"\n{count}. {article['title']}")
        print(f"    Source: {source_name}")
        print(f"    Bias Rating: {metadata['rating']} (Confidence: {metadata['confidence']}, Agreement: {metadata['perc_agree']})")
        print(f"    Outlet Type: {metadata['type']}")
        if metadata['allsides_url']:
            print(f"    AllSides Profile: {metadata['allsides_url']}")
        print(f"    URL: {article['url']}")
        
        # Extract and analyze article content
        full_text = extract_full_text(article['url'])
        if full_text:
            print("    Summarizing article...")
            summary = summarize_with_gemini_http(full_text)
            print(f"\n Gemini Summary:\n{summary}")
            
            print("    Analyzing bias...")
            analysis = analyze_bias_with_together_ai(summary, topic, source_name, metadata)
            print(f"\n Mistral Bias Analysis:\n{analysis}")
            
            # Track the stated leaning
            for line in analysis.splitlines():
                if "🧭" in line and ":" in line:
                    leaning = line.split(":")[-1].strip().lower()
                    leaning_tally.append(leaning)
                    break
        else:
            print("Summary skipped due to scraping issue.")
        
        # Limit to 6 articles from unique sources
        if count >= 6:
            break
    
    # Show final summary
    print_bias_summary(leaning_tally)
    
    # Optional: Visualize the results
    # Uncomment the following line if you've implemented visualization.py
    # plot_bias_distribution(leaning_tally)

if __name__ == "__main__":
    main()