import requests
import os
from newspaper import Article
import google.generativeai as genai
from dotenv import load_dotenv
from fetch_articles.py import fetch_requests
from extract_text.py import extract_text

#loading env vars
load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY") #news api https://newsapi.org/ --> get api key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

BASE_URL = "https://newsapi.org/v2/"
url = BASE_URL + "everything"

topic = input("Enter a news topic to search: ")

data = fetch_requests(topic)
article_text = extract_text(url)



