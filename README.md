# Bias News Inference Summarizer

This tool uses the CLI to:
1. Fetch news articles via a get request from [NewsAPI](https://newsapi.org/)
2. Extract full article text via the webscraper from ['newspaper3k'](https://pypi.org/project/newspaper3k/)
3. Summarize everything w/ [Google Gemini]('google-generativeai')

Installing the correct packages include:
`pip install requests newspaper3k python-dotenv google-generativeai lxml_html_clean`
in an optional virtual env. that can be created with the following: 
```
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
```

Tool configuration:
To run the app, you must put the following in a `.env` file:
```
NEWSAPI_KEY=your_newsapi_key_here 
GEMINI_API_KEY=your_gemini_api_key_here
```
Note: verify its ignored in the .gitignore file

To run the script, call the following: 
```python src/main.py```
