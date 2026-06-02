import os
import hashlib
from google import genai
from google.genai import types
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = os.getenv("PINECONE_INDEX", "pulseai-news")

def init_pinecone(clear: bool = False):
    existing = [i.name for i in pc.list_indexes()]
    if INDEX_NAME in existing and clear:
        pc.delete_index(INDEX_NAME)
        existing = []
    if INDEX_NAME not in existing:
        pc.create_index(
            name=INDEX_NAME,
            dimension=3072,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"Created Pinecone index: {INDEX_NAME}")
    else:
        print(f"Index '{INDEX_NAME}' already exists")
    return pc.Index(INDEX_NAME)

def get_embedding(text: str) -> list[float]:
    result = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    return result.embeddings[0].values

def is_duplicate(index, embedding: list[float], threshold: float = 0.90) -> bool:
    results = index.query(vector=embedding, top_k=1, include_values=False)
    if results["matches"] and results["matches"][0]["score"] >= threshold:
        print(f"  Duplicate detected (score: {results['matches'][0]['score']:.2f}) — skipping")
        return True
    return False

def store_articles(articles: list[dict]) -> list[dict]:
    index = init_pinecone(clear=True)
    unique_articles = []
    for article in articles:
        text = f"{article['title']} {article['summary']}"
        embedding = get_embedding(text)
        if not is_duplicate(index, embedding):
            article_id = hashlib.md5(article["link"].encode()).hexdigest()
            index.upsert(vectors=[{
                "id": article_id,
                "values": embedding,
                "metadata": {
                    "title": article["title"],
                    "source": article["source"],
                    "link": article["link"]
                }
            }])
            unique_articles.append(article)
            print(f"  Stored: {article['title'][:60]}")
    print(f"\nResult: {len(unique_articles)} unique articles out of {len(articles)} total")
    return unique_articles

if __name__ == "__main__":
    from scraper import scrape_articles
    articles = scrape_articles("AI")
    unique = store_articles(articles)
