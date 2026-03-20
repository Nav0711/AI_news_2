# AI News Data Pipeline

Complete documentation for the news data pipeline that fetches, cleans, and stores articles in MongoDB.

## Overview

The data pipeline automatically fetches news articles from NewsAPI across multiple financial and tech topics, cleans the content, and stores them in MongoDB for downstream processing.

### Architecture

```
NewsAPI → Fetch → Clean → Deduplicate → MongoDB
         (5 topics)   (HTML/Boilerplate)  (url_hash)
```

## Setup

### Prerequisites
- Python 3.14+ 
- MongoDB Atlas account  
- NewsAPI key
- Virtual environment (included)

### Installation

1. **Environment Variables** - Update `.env` in backend directory:
   ```bash
   NEWS_API_KEY=your_newsapi_key
   MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/?appName=Ai-news
   MONGO_DB_NAME=newset
   ```

2. **Dependencies** - Already installed in virtual environment:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt  # (optional - already done)
   ```

## Running the Pipeline

### Option 1: Scheduler (Production)
Runs in blocking mode with automatic 30-minute intervals:
```bash
cd backend
source venv/bin/activate
python3 -m data_pipeline.scheduler
```

**What it does:**
- Initial seed fetch: 7 days of articles
- Recurring fetch: Every 30 minutes (1 day back)
- Auto-creates MongoDB indexes
- Graceful shutdown on Ctrl+C

### Option 2: One-time Fetch (Development/Testing)
```bash
cd backend
source venv/bin/activate
python3 -c "from data_pipeline.fetchers.newsapi_fetchers import run_full_pipeline; run_full_pipeline(days_back=7)"
```

### Option 3: Shell Script
```bash
./backend/run_pipeline.sh
```

## Features

### Topics Covered
The pipeline fetches articles for 5 financial/tech topic buckets:

| Topic | Query |
|-------|-------|
| **Stocks** | NSE, BSE, SEBI, stock market, mutual funds |
| **Startups** | startup funding, Series A, venture capital India |
| **Macro** | RBI monetary policy, GDP India, inflation |
| **Corporate** | earnings results, M&A, India |
| **Crypto** | cryptocurrency, Bitcoin, India regulation |

### Data Cleaning Pipeline
1. **HTML Removal** - Strip HTML/XML tags using BeautifulSoup
2. **Boilerplate Removal** - Remove noise (Reuters, AP, newsletter signups, etc.)
3. **Whitespace Normalization** - Collapse multiple spaces/newlines
4. **Length Filtering** - Skip articles < 50 words (stubs/paywall content)

### Deduplication
- Uses `url_hash` as unique key for upsert operations
- Safe to re-run without creating duplicates
- Automatically tracks `fetched_at` timestamp

## Database Schema

### articles Collection
```json
{
  "_id": ObjectId,
  "url": "https://...",
  "url_hash": 1234567890,
  "title": "Article Title",
  "description": "Summary",
  "content": "Full cleaned body text",
  "source": "Reuters",
  "published_at": "2026-03-18T12:00:00Z",
  "category": "stocks",
  "language": "en",
  "fetched_at": "2026-03-18T19:46:12Z",
  "is_cleaned": true,
  "word_count": 450,
  
  // Phase 2: Embeddings (filled later)
  "embedding": null,
  "embedding_model": null,
  
  // Phase 3: RAG (filled later)
  "chunks": []
}
```

### Indexes
Automatically created on first run:
- `url_hash` - Fast deduplication
- `category` - Query by topic
- `published_at` - Sort by date
- `category + published_at` - Combined queries (e.g., "latest crypto news")

## File Structure

```
backend/
├── data_pipeline/
│   ├── scheduler.py              # Main scheduler (runs every 30 min)
│   ├── fetchers/
│   │   └── newsapi_fetchers.py   # NewsAPI integration
│   ├── cleaners/
│   │   └── text_cleaner.py       # HTML/boilerplate removal
│   ├── models/
│   │   └── article.py            # Document schema
│   └── utils/
│       └── db.py                 # MongoDB client + indexes
├── requirements.txt              # Python dependencies
├── .env                          # Configuration (not in git)
└── run_pipeline.sh              # Convenience script
```

## Configuration

### Fetch Interval
Edit [scheduler.py](data_pipeline/scheduler.py) line ~24:
```python
scheduler.add_job(
    func=lambda: run_full_pipeline(days_back=1),
    trigger="interval",
    minutes=30,  # ← Change this to adjust interval
    ...
)
```

### Topic Queries
Modify [newsapi_fetchers.py](data_pipeline/fetchers/newsapi_fetchers.py) `TOPIC_QUERIES` dict to change search terms.

### Min Word Count
Edit [text_cleaner.py](data_pipeline/cleaners/text_cleaner.py) line ~49:
```python
def is_too_short(text: str, min_words: int = 50):  # ← Adjust threshold
```

## Monitoring & Debugging

### Test MongoDB Connection
```bash
cd backend && source venv/bin/activate
python3 -c "from data_pipeline.utils.db import ping; ping()"
```

### Manual Index Creation
```bash
python3 -c "from data_pipeline.utils.db import setup_indexes; setup_indexes()"
```

### Sample Query (Mongo Shell)
```javascript
// Find latest 10 articles about stocks
db.articles.find({category: "stocks"})
  .sort({published_at: -1})
  .limit(10)

// Count articles by category
db.articles.aggregate([
  {$group: {_id: "$category", count: {$sum: 1}}}
])
```

### Check Logs
The scheduler prints real-time logs to stdout:
- `✓ Fetched X raw articles` - Success
- `✗ Network error fetching 'topic'` - API/network issue
- `✓ Pipeline complete. +X new articles` - Summary

## Troubleshooting

### Connection Errors
**Error:** `OperationFailure: bad auth : authentication failed`
- Check `MONGO_URI` in `.env` file
- Verify username/password don't have special characters (if so, URL-encode them)
- Verify IP whitelist in MongoDB Atlas

**Error:** `ModuleNotFoundError: No module named 'data_pipeline'`
- Ensure you're in the `backend/` directory
- Run: `source venv/bin/activate` first

### API Errors
**Error:** `NewsAPI error for 'stocks': Your API key is invalid`
- Check `NEWS_API_KEY` in `.env`
- Visit https://newsapi.org to verify

### Performance Issues
**Slow fetches (> 30 minutes per cycle):**
- Check network connectivity
- Verify MongoDB connection pooling settings in [db.py](data_pipeline/utils/db.py)
- NewsAPI has rate limits (100 requests/day on free tier)

## Next Steps

### Phase 2: Embeddings
- Generate embeddings for cleaned articles  
- Populate `embedding` and `embedding_model` fields
- Store in vector database (optional)

### Phase 3: RAG Pipeline  
- Chunk articles by token count
- Populate `chunks` array for retrieval

### Phase 4: API Server
- Create REST API to query cleaned articles
- Add search/filtering endpoints
- Implement user authentication

## API Keys & Secrets

⚠️ **Never commit `.env` to git!**

- `NEWS_API_KEY` - Get from https://newsapi.org (free tier = 100/day)
- `MONGO_URI` - Get from MongoDB Atlas (connection string)

## Performance

**Typical Run Metrics (1-day lookback):**
- Fetch time: 5-10 seconds (5 topics × 20s timeout)
- Clean & dedupe: 1-3 seconds (100 articles)
- Database insert: 2-5 seconds  
- **Total**: ~15 seconds per cycle

**Memory usage:** ~50-100 MB (Python + MongoDB driver)

## Support

- Check scheduler output for detailed error messages
- Review [newsapi_fetchers.py](data_pipeline/fetchers/newsapi_fetchers.py) for fetch logic
- Visit [NewsAPI Docs](https://newsapi.org/docs) for query syntax
