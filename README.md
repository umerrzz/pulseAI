# PulseAI — Autonomous AI News Intelligence Agent

An end-to-end AI pipeline that scrapes news, deduplicates using vector similarity, and generates a professional newsletter using Gemini 2.5.

## Architecture
- **Scraper** — fetches articles from 5 RSS feeds
- **Pinecone RAG** — embeds articles using Gemini embeddings, deduplicates using cosine similarity
- **Gemini 2.5** — trend analysis and newsletter generation
- **FastAPI** — production REST API with auto-generated docs

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your API keys
python -m uvicorn main:app --reload
```

## API
- `GET /` — status
- `POST /generate` — generate newsletter for any topic
- `GET /health` — health check
- `GET /docs` — interactive API documentation
