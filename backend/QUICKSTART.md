# Phase 2 Quick Start Guide

## ✅ What's Ready

### 1. **Recommendation Engine** — All 4 Modules
- ✅ `embedder.py` — Generate embeddings (326 articles embedded)
- ✅ `faiss_store.py` — Vector search (326 vectors, dim=384)
- ✅ `user_profile.py` — User interest modeling (6 categories)
- ✅ `recommender.py` — Ranking algorithm

### 2. **API Endpoints Running**
- ✅ `GET /health` → Returns `{"status": "ok", "faiss_vectors": 326}`
- ✅ `GET /interests` → Returns 6 interest categories
- ✅ `POST /feed` → Returns ranked articles

### 3. **FAISS Index**
- ✅ Built: 326 vectors
- ✅ Dimension: 384
- ✅ Search speed: ~5-10ms

### 4. **Tested with Multiple Interests**
- ✅ stocks
- ✅ startup
- ✅ macro
- ✅ corporate
- ✅ crypto
- ✅ real_estate
- ✅ combined (stocks + macro)

---

## 🚀 Start the API

```bash
cd backend
PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The API will automatically:
1. Embed any pending articles
2. Build FAISS index
3. Start serving on http://localhost:8000

---

## 🧪 Test Examples

### Health Check
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

### List Interests
```bash
curl http://localhost:8000/interests | python3 -m json.tool
```

### Get Personalized Feed
```bash
# Stocks
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests": ["stocks"], "top_k": 5}'

# Startup
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests": ["startup"], "top_k": 5}'

# Multiple interests
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests": ["stocks", "macro"], "top_k": 5}'
```

---

## 📊 Response Format

```json
{
  "id": "article_mongodb_id",
  "title": "Article Title",
  "description": "Article summary",
  "source": "News Source",
  "published_at": "2026-03-18T10:29:36Z",
  "category": "stocks",
  "url": "https://...",
  "relevance_score": 0.5369
}
```

Articles are ranked by `relevance_score` (highest = most relevant).

---

## 🔑 Key Features

### Interest-Based Ranking
User interests are converted to embeddings using INTEREST_SEEDS:
- stocks: "NSE BSE stock market equity mutual funds SIP SEBI"
- startup: "startup funding venture capital Series A founder unicorn"
- macro: "GDP inflation RBI monetary policy interest rate economy"
- corporate: "company earnings merger acquisition quarterly results"
- crypto: "cryptocurrency Bitcoin blockchain DeFi Web3 regulation"
- real_estate: "real estate property housing market RERA home loan"

### Reading History Integration
User query vector = 70% interests + 30% reading history (weighted average)
- Set `read_article_ids` parameter to personalize further
- Most recent reads have more influence

### Filtering
- Automatically excludes already-read articles
- Set `read_article_ids` to get fresh recommendations

---

## 📁 Documentation

- `PHASE2_DELIVERABLES.md` — Full deliverables checklist
- `PHASE2_TEST_REPORT.md` — Comprehensive test results
- `test_api.sh` — Test suite script
- `verify_phase2_simple.py` — Python verification script

---

## ✨ What Changed

**Preserved:**
- Data pipeline workflow
- MongoDB schema
- API structure

**Added:**
- Sentence Transformer embeddings
- FAISS vector index
- User profiling system
- Recommendation ranking

**No Breaking Changes** ✅

---

## 🎯 Next Phase

Phase 3 — AI News Navigator (RAG):
- Chunk articles
- Implement vector retrieval
- Integrate LLM (Ollama + Llama3)
- Create interactive briefing system
