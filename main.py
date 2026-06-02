import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from scraper import scrape_articles
from embedder import store_articles
from newsletter import generate_newsletter

load_dotenv()

app = FastAPI(
    title="PulseAI",
    description="Autonomous AI News Intelligence Agent",
    version="1.0.0"
)

class NewsRequest(BaseModel):
    topic: str = "AI"
    max_per_feed: int = 8

class NewsResponse(BaseModel):
    topic: str
    total_scraped: int
    unique_articles: int
    duplicates_removed: int
    newsletter: str

@app.get("/")
def root():
    return {
        "name": "PulseAI",
        "status": "running",
        "description": "Autonomous AI News Intelligence Agent"
    }

@app.post("/generate", response_model=NewsResponse)
def generate(request: NewsRequest):
    articles = scrape_articles(request.topic, request.max_per_feed)
    unique = store_articles(articles)
    newsletter = generate_newsletter(unique, request.topic)
    return NewsResponse(
        topic=request.topic,
        total_scraped=len(articles),
        unique_articles=len(unique),
        duplicates_removed=len(articles) - len(unique),
        newsletter=newsletter
    )

@app.get("/health")
def health():
    return {"status": "healthy"}
