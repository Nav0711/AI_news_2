# 🚀 Phase 3 Terminal Commands Cheat Sheet

## ⚡ Quick Start (Copy & Paste)

### Terminal 1: Build RAG Index
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend && \
PYTHONPATH=. /opt/homebrew/bin/python3.11 scripts/build_rag_index.py
```

### Terminal 2: Start Ollama (keep running)
```bash
ollama serve
```

### Terminal 3: Start API
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend && \
PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Terminal 4: Test API
```bash
# Health check
curl http://localhost:8000/health | python3 -m json.tool

# Ask a question  
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What is happening with AI startups in India?", "stream": false}' | python3 -m json.tool
```

---

## 📋 Step-by-Step Setup

### Step 1: Install Ollama (one-time)
```bash
# macOS via Homebrew
brew install ollama

# Or download from: https://ollama.ai
```

### Step 2: Install Python Dependencies
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend
/opt/homebrew/bin/python3.11 -m pip install ollama==0.2.1 langchain==0.2.0 -q
```

### Step 3: Build RAG Index
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend
PYTHONPATH=. /opt/homebrew/bin/python3.11 scripts/build_rag_index.py
```

**Expected Output:**
```
=== Phase 3 RAG Index Build ===

✓ Chunking complete. XXX new chunks created.
  Total chunks in DB: YYY
Embedding ZZZ chunks...
  YYY/ZZZ chunks embedded
✓ Chunk embedding complete.
Building chunk FAISS index from ZZZ chunks...
✓ Chunk index ready. ZZZ vectors, dim=384

✓ RAG index ready: ZZZ chunk vectors
✓ Ollama available for RAG
```

### Step 4: Start Ollama Server

**Terminal 2 (keep running):**
```bash
ollama serve
```

**First time:** Download Llama3 model (in another terminal)
```bash
ollama pull llama3
# Downloads ~4.7GB (one-time, takes 5-10 minutes)
```

Check if Llama3 is available:
```bash
ollama list
```

### Step 5: Start NewsET API

**Terminal 3:**
```bash
cd /Users/navdeeop/Developer/projects/AI_News/backend
PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**Expected Output:**
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

## 🧪 Comprehensive Test Commands

### 1. Health Check
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

**Expected Response:**
```json
{
  "status": "ok",
  "faiss_articles": 326,
  "faiss_chunks": 1850,
  "ollama_available": true
}
```

### 2. List Interest Categories
```bash
curl http://localhost:8000/interests | python3 -m json.tool
```

### 3. Get Personalized Feed (Phase 2)
```bash
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests": ["stocks", "startup"], "top_k": 3}' | python3 -m json.tool
```

### 4. Streaming RAG Briefing
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What is happening with AI startups in India?", "stream": true}'
```

**Output:** Tokens stream in real-time as LLM generates response

### 5. Non-Streaming RAG Briefing (with sources)
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the inflation situation in India?", "stream": false}' | python3 -m json.tool
```

**Expected Response:**
```json
{
  "answer": "The Reserve Bank of India (RBI) is monitoring inflation pressures...",
  "sources": [
    {
      "title": "RBI unlikely to hike rates...",
      "source": "The Times of India",
      "url": "https://...",
      "score": 0.7234
    },
    {
      "title": "Inflation concerns persist...",
      "source": "BusinessLine",
      "url": "https://...",
      "score": 0.6891
    }
  ]
}
```

### 6. Multi-Turn Conversation (Follow-up)
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What about the impact on household budgets?",
    "history": [
      {
        "role": "user",
        "content": "What is the inflation situation in India?"
      },
      {
        "role": "assistant",
        "content": "The Reserve Bank of India is monitoring inflation pressures from crude oil prices and food costs..."
      }
    ],
    "stream": false
  }' | python3 -m json.tool
```

### 7. Different Question Types

**Market Analysis:**
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the top performing stocks today?", "stream": false}' | python3 -m json.tool
```

**Sector Analysis:**
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the impact of AI on Indian tech companies?", "stream": false}' | python3 -m json.tool
```

**Policy & Regulations:**
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the recent regulatory changes affecting startups?", "stream": false}' | python3 -m json.tool
```

---

## 🐛 Troubleshooting

### Issue: "Ollama not running"
```bash
# Check if Ollama is listening
curl http://localhost:11434/api/tags

# If error, start Ollama:
ollama serve
```

### Issue: "Model not found"
```bash
# Download Llama3
ollama pull llama3

# Verify it's installed
ollama list
```

### Issue: "No relevant articles found"
```bash
# Check if chunks were created
cd /Users/navdeeop/Developer/projects/AI_News/backend
PYTHONPATH=. /opt/homebrew/bin/python3.11 << 'EOF'
from data_pipeline.utils.db import get_db
db = get_db()
print(f"Articles: {db['articles'].count_documents({})}")
print(f"Chunks: {db['article_chunks'].count_documents({})}")
print(f"Embedded chunks: {db['article_chunks'].count_documents({'embedding': {'$ne': None}})}")
EOF
```

### Issue: Slow responses
```bash
# Check system memory
top  # or Activity Monitor on macOS

# Verify Ollama is responding
curl http://localhost:11434/api/tags

# Reduce chunk index load (restart API):
# Modify api/main.py to load fewer chunks into memory
```

---

## 📊 Phase 3 Architecture

```
User Question
     ↓
[/briefing or /ask endpoint]
     ↓
[retriever.py] — Embed question + search FAISS
     ↓
[Top-5 relevant chunks from DB]
     ↓
[prompt_builder.py] — Format chunks into LLM context
     ↓
[llm.py] — Call Ollama (Llama3)
     ↓
[streaming/non-streaming response]
```

---

## 🎯 Next Steps

After everything is working:

1. **Test with Frontend** — Call `/briefing` from React/Vue
2. **Add Rate Limiting** — Prevent API overload
3. **Implement Caching** — Cache common questions
4. **Fine-tune Llama3** — On Indian business news (optional)
5. **Phase 4** — Story Arc Tracker

---

## 📝 File Reference

| File | Purpose |
|------|---------|
| `rag/chunker.py` | Split articles into overlapping chunks |
| `rag/chunk_store.py` | FAISS index for chunk retrieval |
| `rag/retriever.py` | Query embedding + chunk search |
| `rag/prompt_builder.py` | Build LLM prompts with context |
| `rag/llm.py` | Ollama wrapper with streaming |
| `api/main.py` | FastAPI endpoints (/briefing, /ask) |
| `scripts/build_rag_index.py` | Build RAG index from articles |
| `PHASE3_SETUP.md` | Detailed setup guide |

---

## ✨ Summary

**Phase 3 is now ready to use!**

- ✅ All RAG modules implemented
- ✅ Ollama integration with Llama3
- ✅ Streaming support for real-time responses
- ✅ Multi-turn conversation history
- ✅ Source attribution for all answers
- ✅ Production-ready error handling

**Status:** Ready for frontend integration and user testing
