import requests
from collections import Counter

from api_setup import api_keys
from article_utils import extract_full_text, load_allsides_data, find_allsides_metadata
from analysis import summarize_with_gemini_http, analyze_bias_with_together_ai
from db_utils import save_article, fetch_all_articles, init_db

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
    print("BiasAI Analysis Tool")
    print("--------------------------")

    init_db()

    while True:
        print("\nOptions:")
        print("1. Analyze new topic")
        print("2. Browse saved articles")
        print("q. End program")
        choice = input("Your choice: ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break

        elif choice == '2':
            print("\n--- Saved Articles ---\n")
            saved = fetch_all_articles()
            if not saved:
                print("No saved articles found.")
            else:
                for row in saved:
                    print(f"[{row[0]}] {row[1]} ({row[2]}) - {row[5].capitalize()} leaning")
                    print(f"Date: {row[8]}")
                    print(f"URL: {row[3]}")
                    print(f"Summary: {row[4][:300]}...\n")

        elif choice == '1':
            print("\nGive a topic, we will give the source, summarize it, take its political stance and evidence of it.")
            topic = input("Enter a news topic to search: ")

            print("Loading media bias data...")
            allsides_df = load_allsides_data()

            print(f"Fetching articles about '{topic}'...")
            articles = fetch_news_articles(topic)

            if not articles:
                print("No articles found.")
                continue

            seen_sources = set()
            leaning_tally = []
            count = 0

            print(f"\nFound {len(articles)} articles. Analyzing up to 6 unique sources:")

            for idx, article in enumerate(articles, 1):
                source_name = article["source"]["name"]

                if source_name in seen_sources:
                    continue
                seen_sources.add(source_name)
                count += 1

                metadata = find_allsides_metadata(source_name, allsides_df)

                print(f"\n{count}. {article['title']}")
                print(f"Source: {source_name}")
                print(f"Bias Rating: {metadata['rating']} (Confidence: {metadata['confidence']}, Agreement: {metadata['perc_agree']})")
                print(f"Outlet Type: {metadata['type']}")
                if metadata['allsides_url']:
                    print(f"    AllSides Profile: {metadata['allsides_url']}")
                print(f"    URL: {article['url']}")

                full_text = extract_full_text(article['url'])
                if full_text:
                    print("Summarizing...")
                    summary = summarize_with_gemini_http(full_text)
                    print(f"\n Gemini Summary:\n{summary}")

                    print("Analyzing bias...")
                    analysis = analyze_bias_with_together_ai(summary, topic, source_name, metadata)
                    print(f"\n Mistral Bias Analysis:\n{analysis}")

                    leaning = "unknown"
                    for line in analysis.splitlines():
                        if "Political Leaning:" in line:
                            leaning = line.split(":")[-1].strip().lower()
                            leaning_tally.append(leaning)
                            break
                
                    save_article(
                        title=article['title'],
                        source=source_name,
                        url=article['url'],
                        summary=summary,
                        leaning=leaning,
                        topic=topic,
                        explanation=analysis
                    )
                else:
                    print("Summary skipped due to scraping issue.")
                
                #curr source amount allowed
                if count >= 6:
                    break

        else:
            print("invalid; choose 1, 2, or q.")



if __name__ == "__main__":
    main()