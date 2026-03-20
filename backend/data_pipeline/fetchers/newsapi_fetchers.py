# data-pipeline/fetchers/newsapi_fetcher.py
import os
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from data_pipeline.cleaners.text_cleaner import clean_article_text, is_too_short
from data_pipeline.models.article import create_article_doc
from data_pipeline.utils.db import get_db

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

# Topic buckets mapped to search queries.
# These cover the 4 target user segments from the PRD.
TOPIC_QUERIES = {
    "stocks":    "NSE OR BSE OR SEBI OR stock market OR mutual funds",
    "startup":   "startup funding OR Series A OR venture capital India",
    "macro":     "RBI monetary policy OR GDP India OR inflation rate",
    "corporate": "earnings results OR merger acquisition India",
    "crypto":    "cryptocurrency Bitcoin India regulation",
}

def fetch_articles_for_topic(topic: str, query: str, days_back: int = 1) -> list[dict]:
    """
    Fetch articles for a single topic from NewsAPI.
    Returns a list of raw (uncleaned) article dicts.
    """
    from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    params = {
        "q": query,
        "from": from_date,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,   # NewsAPI max per request
        "apiKey": NEWS_API_KEY,
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "ok":
            print(f"  ✗ NewsAPI error for '{topic}': {data.get('message')}")
            return []

        articles = data.get("articles", [])
        print(f"  ✓ Fetched {len(articles)} raw articles for topic: {topic}")
        return articles

    except requests.RequestException as e:
        print(f"  ✗ Network error fetching '{topic}': {e}")
        return []

def process_and_store(raw_articles: list[dict], category: str) -> int:
    """
    Clean each article and upsert into MongoDB.
    Returns count of newly inserted articles.
    """
    db = get_db()
    collection = db["articles"]
    inserted = 0

    for raw in raw_articles:
        # Build cleaned content from description + content fields
        # NewsAPI's 'content' field is truncated to ~200 chars on free tier
        raw_text = (raw.get("content") or "") + " " + (raw.get("description") or "")
        cleaned = clean_article_text(raw_text)

        # Skip stubs
        if is_too_short(cleaned):
            continue

        doc = create_article_doc(
            url=raw.get("url", ""),
            title=raw.get("title", ""),
            description=raw.get("description", ""),
            content=cleaned,
            source_name=raw.get("source", {}).get("name", "Unknown"),
            published_at=raw.get("publishedAt", ""),
            category=category,
        )

        # Upsert on url_hash — safe to re-run without duplicates
        result = collection.update_one(
            {"url_hash": doc["url_hash"]},
            {"$setOnInsert": doc},
            upsert=True
        )
        if result.upserted_id:
            inserted += 1

    return inserted

def run_full_pipeline(days_back: int = 1):
    """
    Fetch all topic buckets, clean, and store.
    Called by the scheduler every 30 minutes.
    """
    print(f"\n[{datetime.utcnow().isoformat()}] Starting news fetch pipeline...")
    total = 0

    for topic, query in TOPIC_QUERIES.items():
        raw = fetch_articles_for_topic(topic, query, days_back=days_back)
        count = process_and_store(raw, category=topic)
        total += count
        time.sleep(1)  # Respect NewsAPI rate limits

    db = get_db()
    grand_total = db["articles"].count_documents({})
    print(f"\n✓ Pipeline complete. +{total} new articles. Total in DB: {grand_total}")
    return total