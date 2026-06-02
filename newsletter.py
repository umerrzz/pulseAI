import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_newsletter(articles: list[dict], topic: str) -> str:
    articles_text = ""
    for i, article in enumerate(articles[:15], 1):
        articles_text += f"""
Article {i}:
Title: {article['title']}
Summary: {article['summary']}
Source: {article['source']}
Link: {article['link']}
---"""

    prompt = f"""
You are an expert tech journalist writing a premium AI industry newsletter.

Here are today's unique, deduplicated news articles about "{topic}":

{articles_text if articles_text else "No articles found. Use your own knowledge about recent " + topic + " developments."}

Write a professional newsletter with exactly this structure:

1. SUBJECT LINE
A compelling email subject line (max 10 words)

2. OPENING (2-3 sentences)
A punchy executive summary of today's biggest story

3. TOP 3 TRENDS
For each trend:
- Trend name (bold)
- 2-3 sentence analysis connecting multiple articles
- Why it matters for the industry

4. STORY OF THE DAY
Pick the single most important story, explain it in depth (4-5 sentences)

5. QUICK HITS
5 bullet points of other notable news, one sentence each with source

6. CLOSING THOUGHT
One sharp, memorable insight (2-3 sentences)

Write in a confident, intelligent tone like a senior analyst.
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    from scraper import scrape_articles
    from embedder import store_articles
    print("Scraping articles...")
    articles = scrape_articles("AI")
    print("Deduplicating with Pinecone...")
    unique_articles = store_articles(articles)
    print("Generating newsletter with Gemini...\n")
    newsletter = generate_newsletter(unique_articles, "AI")
    print("=" * 60)
    print(newsletter)
    print("=" * 60)
