"""Functions for article summarization and bias analysis."""

import requests
import json
from api_setup import api_keys, together_client

def summarize_with_gemini_http(article_text):
    """Summarize article text using the Gemini API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_keys['gemini']}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Summarize the following news article in 12-15 sentences with a neutral and factual tone:\n\n{article_text}"
                    }
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Gemini API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"

def analyze_bias_with_together_ai(summary, topic, source, metadata):
    """Analyze political bias in article summary using Together AI."""
    prompt = f"""
You are a political media analyst.

Analyze the article summary below and classify its political leaning:
- Left-leaning
- Center
- Right-leaning
- Balanced

Also explain:
- What framing or tone signals this leaning?
- Does it align with the AllSides rating?

Topic: {topic}
Source: {source}
AllSides Rating: {metadata['rating']}
Confidence: {metadata['confidence']}, Agreement: {metadata['perc_agree']}

Summary:
{summary}

Respond in at least 15 sentences and include the leaning label at the top like this: " Political Leaning: [Left/Right/Center/Balanced]"
"""
    response = together_client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.5,
        top_p=0.9
    )
    return response.choices[0].message.content.strip()