from newspaper import Article

def extract_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except Exception as e:
        print(f"failed to extract article text: {e}")
        return None