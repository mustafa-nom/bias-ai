# Bias News Inference Summarizer
**BiasAI** is a Python command-line tool that helps users evaluate the political bias and sentiment of news articles. It fetches real-time articles on a given topic, summarizes them using Google's Gemini AI, and assesses political leaning with TogetherAI (Mistral model), cross-referenced with the AllSides media bias dataset.

## Features & Tools
- **News fetching** using [NewsAPI](https://newsapi.org/) based on user-provided topics  
- **Article summarization** via [Google Gemini](https://ai.google.dev/)  
- **Political bias detection** using [TogetherAI (Mistral)](https://www.together.ai/)  
- **Bias context and rating** cross-referenced with the [AllSides Dataset](https://github.com/favstats/AllSideR)  
- **Web scraping** to extract full article content via [`newspaper3k`](https://pypi.org/project/newspaper3k/)  
- **Caching system** using local JSON to reduce redundant API calls  
- **Persistent storage** of analyzed articles and results in a local SQLite database

## Installation
Installing the correct packages include:
`pip install requests newspaper3k python-dotenv google-generativeai lxml_html_clean`
in an optional virtual environment that can be created with the following: 
```
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
```
## Configuration
To run the app, you must put the following in a `.env` file:
```
NEWSAPI_KEY=your_newsapi_key_here 
GEMINI_API_KEY=your_gemini_api_key_here
TOGETHER_API_KEY=together_api_key_here
```
Note: verify its ignored in the .gitignore file

To run the script, call the following: 
```python src/main.py```
