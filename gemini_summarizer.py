import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

#summarize the text and give source bias score
def ai_summarize(article_text):
    try:
        response = model.generate_content(
            f"Summarize this article in 3-4 sentences and determine the source's bias to its respective political standing: {article_text}"
            )
        summarized_text = response.text
        return summarized_text
    except Exception as e:
        return f'Gemini summarization got an error, {e}'
