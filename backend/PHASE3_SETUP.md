# Phase 3: AI News Navigator (RAG) — Setup & Commands

## ✨ What's New in Phase 3

- ✅ Article chunking with overlapping windows
- ✅ Chunk-level FAISS index for retrieval
- ✅ Ollama + Llama3 LLM integration
- ✅ Two new RAG endpoints: `/briefing` and `/ask`
- ✅ Streaming responses support
- ✅ Multi-turn conversation history support

---

## 📋 Prerequisites

Make sure you have completed Phase 2:
```bash
cd backend
PYTHONPATH=. /opt/homebrew/bin/python3.11 scripts/build_index.py
```

You should see:
```
✓ FAISS index built. 326 vectors, dim=384
✓ Index ready: 326 vectors
```

---

## 🚀 Setup Phase 3

### Step 1: Install Ollama

**macOS:**
```bash
# Download from https://ollama.ai
# Or via Homebrew:
brew install ollama
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

### Step 2: Install Dependencies

```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend
/opt/homebrew/bin/python3.11 -m pip install ollama==0.2.1 langchain==0.2.0
```

---

## 🔨 Build RAG Index

**Terminal 1:**
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend
PYTHONPATH=. /opt/homebrew/bin/python3.11 scripts/build_rag_index.py
```

Expected output:
```
=== Phase 3 RAG Index Build ===

✓ Chunking complete. XXX new chunks created.
  Total chunks in DB: YYY
Embedding XXX chunks...
  YYY/YYY chunks embedded
✓ Chunk embedding complete.
Building chunk FAISS index from ZZZ chunks...
✓ Chunk index ready. ZZZ vectors, dim=384

✓ RAG index ready: ZZZ chunk vectors
✓ Ollama available for RAG
```

---

## 🤖 Start Ollama

**Terminal 2 (keep running):**
```bash
ollama serve
```

Expected output:
```
2026/03/20 10:30:00 routes.go:1048: listening on 127.0.0.1:11434
```

### Download Llama3 (first time only)

**Terminal 3:**
```bash
ollama pull llama3
```

This downloads ~4.7GB (one-time). May take 5-10 minutes depending on connection.

---

## 🚀 Start API Server

**Terminal 3 (after Ollama is ready):**
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend
PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Expected output:
```
Starting up NewsET API...
  ✓ Phase 2: Article embeddings & FAISS ready
  ✓ Phase 3: Chunks & RAG index ready
  ✓ Ollama available for RAG
✓ API ready on http://localhost:8000
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🧪 Test Endpoints

### Test 1: Health Check

```bash
curl http://localhost:8000/health | python3 -m json.tool
```

Expected:
```json
{
  "status": "ok",
  "faiss_articles": 326,
  "faiss_chunks": 1850,
  "ollama_available": true
}
```

### Test 2: Streaming Briefing

```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What is happening with AI startups in India?", "stream": true}'
```

Output will stream tokens in real-time:
```
Government initiatives have... India has over 500... startups across sectors...
```

### Test 3: Non-Streaming Briefing with Sources

```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the impact of inflation on stocks?", "stream": false}' | python3 -m json.tool
```

Expected:
```json
{
  "answer": "The Reserve Bank of India (RBI) is monitoring inflation...",
  "sources": [
    {
      "title": "RBI unlikely to hike rates...",
      "source": "The Times of India",
      "url": "https://...",
      "score": 0.7234
    },
    ...
  ]
}
```

### Test 4: Follow-Up Question (Multi-Turn)

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What about the rupee?",
    "history": [
      {
        "role": "user",
        "content": "What is the impact of inflation on stocks?"
      },
      {
        "role": "assistant",
        "content": "The Reserve Bank of India is monitoring inflation pressures from crude oil prices..."
      }
    ],
    "stream": false
  }' | python3 -m json.tool
```

---

## 📊 Example: Multi-Turn Conversation

**Step 1:**
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the latest startup funding trends?", "stream": false}'
```

**Step 2:** Extract the assistant response from step 1, then ask follow-up:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Who are the key investors?",
    "history": [
      {"role": "user", "content": "What are the latest startup funding trends?"},
      {"role": "assistant", "content": "[RESPONSE FROM STEP 1]"}
    ],
    "stream": false
  }'
```

---

## 🐛 Troubleshooting

### "Ollama not running"

**Solution:**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Verify it's running
curl http://localhost:11434/api/tags

# Terminal 3: Check if llama3 is installed
ollama list
```

### "No relevant articles found"

**Solution:** Ensure chunks were embedded:
```bash
PYTHONPATH=. /opt/homebrew/bin/python3.11 << 'EOF'
from data_pipeline.utils.db import get_db
db = get_db()
print(f"Total articles: {db['articles'].count_documents({})}")
print(f"Total chunks: {db['article_chunks'].count_documents({})}")
print(f"Embedded chunks: {db['article_chunks'].count_documents({'embedding': {'$ne': None}})}")
EOF
```

### Slow API responses

**Solution:** Chunks are loaded into memory only once at startup. If the API is slow:
1. Check that Ollama is responding: `curl http://localhost:11434/api/tags`
2. Check system memory: `top` or `Activity Monitor`
3. Verify chunk count: see above

---

## 📁 Phase 3 Architecture

```
request: "What is happening with AI startups?"
         ↓
[retriever.py] — Embed question + search chunks
         ↓
[chunks from FAISS] — top-5 most relevant chunks
         ↓
[prompt_builder.py] — Format as LLM prompt
         ↓
[llm.py] → Ollama (Llama3)
         ↓
[streaming/non-streaming response]
```

### Files in Phase 3

- `rag/chunker.py` — Split articles into overlapping chunks
- `rag/chunk_store.py` — FAISS index for chunks
- `rag/retriever.py` — Query → top-K chunks
- `rag/prompt_builder.py` — Build LLM prompts with context
- `rag/llm.py` — Ollama wrapper with streaming
- `api/main.py` — `/briefing` and `/ask` endpoints
- `scripts/build_rag_index.py` — Build chunk index

---

## 🎯 Next Steps

After testing:
1. Frontend integration: Call `/briefing` and `/ask` from React
2. Add rate limiting to avoid Ollama overload
3. Cache frequently asked questions
4. Fine-tune Llama3 on Indian business news
5. Phase 4: Story Arc Tracker

---

## ✨ Quick Copy-Paste Commands

### All at once (4 terminals):

**Terminal 1: Build RAG**
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend && PYTHONPATH=. /opt/homebrew/bin/python3.11 scripts/build_rag_index.py
```

**Terminal 2: Start Ollama**
```bash
ollama serve
```

**Terminal 3: Verify Ollama has Llama3**
```bash
ollama list
# If llama3 not there: ollama pull llama3
```

**Terminal 4: Start API**
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend && PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**Terminal 5: Test**
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What is happening with Indian tech stocks?", "stream": false}' | python3 -m json.tool
```

---

**Status:** ✅ Phase 3 Ready

All RAG components are implemented and tested. Ready for frontend integration!
