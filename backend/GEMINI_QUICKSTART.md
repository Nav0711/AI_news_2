# Phase 3 Gemini Refactor — Quick Setup Guide

**Time to complete:** ~5 minutes

---

## Step 1: Get Gemini API Key (2 minutes)

1. Open browser: https://aistudio.google.com/app/apikey
2. Sign in with Google (your personal account)
3. Click **"Create API Key"** button
4. Select **"Create API key in new project"**
5. Copy the API key (looks like: `AIzaSyC...`)
6. Keep it safe!

**Free Tier Benefits:**
- 1500 requests/day
- 1M token context window per request
- Sufficient for hackathons and development

---

## Step 2: Add API Key to .env (1 minute)

Open `backend/.env` and add:

```bash
GEMINI_API_KEY=AIzaSyC...your_actual_key_here...
```

**Example:**
```bash
# backend/.env
GEMINI_API_KEY=AIzaSyBrfXvfvWxT_oN0x16_5nZ9mJ_example
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=newsdb
```

---

## Step 3: Install Dependencies (1 minute)

```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend

/opt/homebrew/bin/python3.11 -m pip install google-generativeai==0.5.4
```

---

## Step 4: Start API Server (1 minute)

```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend

PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## Step 5: Test API (in new terminal)

### Health Check
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

**Expected Response:**
```json
{
  "status": "ok",
  "faiss_articles": 326,
  "gemini": true,
  "model": "gemini-1.5-flash"
}
```

### Simple Question (Non-Streaming)
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the latest news on AI startups in India?",
    "stream": false
  }' | python3 -m json.tool
```

**Expected Response:**
```json
{
  "question": "What is the latest news on AI startups in India?",
  "answer": "Based on recent articles:\n\n**Key Highlights:**\n- Indian AI startups raised...",
  "articles_used": 45,
  "model": "gemini-1.5-flash"
}
```

### Streaming Question
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Impact of RBI decisions on markets",
    "stream": true
  }'
```

**Expected Response:** Real-time streaming text
```
Based on recent articles:

Key Highlights:
- RBI raised repo rate by...
- Banks showed mixed response...
...
```

### Category-Filtered Question
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "SEBI regulatory updates",
    "stream": false,
    "category_filter": "stocks"
  }' | python3 -m json.tool
```

---

## What's Different from Ollama Version?

### Before (Ollama):
- ❌ Needed to run `ollama serve` in separate terminal
- ❌ Downloaded 4.7GB Llama3 model
- ❌ Startup took 90+ seconds
- ❌ Complex chunking pipeline
- ❌ Multiple FAISS indices

### After (Gemini):
- ✅ No extra servers needed
- ✅ Instant startup (<2 seconds)
- ✅ Simple API call
- ✅ Better responses
- ✅ Easier to scale

---

## Troubleshooting

### Error: "GEMINI_API_KEY not set"
- Check `.env` has the key
- Restart FastAPI server (Ctrl+C, then start again)

### Error: "ModuleNotFoundError: google"
- Run: `/opt/homebrew/bin/python3.11 -m pip install google-generativeai==0.5.4`

### Error: "429 Too Many Requests"
- You've exceeded free tier limit (1500 req/day)
- Wait 24 hours or upgrade

### Error: "No Response"
- Check internet connection (API requires network)
- Check GEMINI_API_KEY is valid

---

## Expected Response Format

### /briefing (non-streaming)
```json
{
  "question": "...",
  "answer": "string with AI response",
  "articles_used": 42,
  "model": "gemini-1.5-flash"
}
```

### /ask (follow-up)
```json
{
  "question": "...",
  "answer": "string with continuation",
  "articles_used": 38,
  "model": "gemini-1.5-flash"
}
```

### /health
```json
{
  "status": "ok",
  "faiss_articles": 326,
  "gemini": true,
  "model": "gemini-1.5-flash"
}
```

---

## All Available Endpoints (Now Working!)

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/feed` | POST | Phase 2: Personalized news | ✅ unchanged |
| `/interests` | GET | Phase 2: List categories | ✅ unchanged |
| `/health` | GET | API health check | ✅ updated for Gemini |
| `/briefing` | POST | Phase 3: AI briefings | ✅ NEW (Gemini) |
| `/ask` | POST | Phase 3: Follow-ups | ✅ NEW (Gemini) |

---

## Optional: Test Phase 2 Still Works

```bash
# Get interest categories
curl http://localhost:8000/interests | python3 -m json.tool

# Get personalized feed
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["stocks", "startup"],
    "read_article_ids": [],
    "top_k": 10
  }' | python3 -m json.tool
```

---

## 🎉 You're Done!

Your NewsET API now runs on Google Gemini 1.5 Flash!

**Next Steps:**
- Build frontend (React/Vue)
- Connect UI to endpoints
- Add user authentication
- Deploy to cloud

---

**Questions?**
- Check Gemini docs: https://ai.google.dev/
- API key management: https://aistudio.google.com/app/apikey
- FastAPI docs: http://localhost:8000/docs (interactive!)
