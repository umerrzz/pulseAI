import feedparser
import re
from datetime import datetime

FEEDS = [
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://venturebeat.com/feed/",
    "https://techcrunch.com/feed/",
]

def clean_html(raw: str) -> str:
    clean = re.sub(r'<[^>]+>', '', raw)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:500]

def scrape_articles(topic: str, max_per_feed: int = 8) -> list[dict]:
    articles = []
    for feed_url in FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:max_per_feed]:
                title = clean_html(entry.get("title", ""))
                summary = clean_html(entry.get("summary", ""))
                link = entry.get("link", "")
                published = entry.get("published", str(datetime.now()))
                if topic.lower() in title.lower() or topic.lower() in summary.lower():
                    articles.append({
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "published": published,
                        "source": feed_url
                    })
        except Exception as e:
            print(f"Error scraping {feed_url}: {e}")
            continue
    print(f"Scraped {len(articles)} articles about '{topic}'")
    return articles

if __name__ == "__main__":
    results = scrape_articles("AI")
    for r in results:
        print(f"\n Title: {r['title']}")
        print(f" Source: {r['source']}")
        print(f" Summary: {r['summary'][:150]}")
