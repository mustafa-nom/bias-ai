import requests

#fetch the news articles
def fetch_requests(topic):
    BASE_URL = "https://newsapi.org/v2/"
    url = BASE_URL + "everything"
    params = {
        "q": topic,
        "language": "en",
        "pageSize": 15,
        "sortBy": "relevancy",
        "apiKey": NEWSAPI_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data