#!/bin/bash
# Terminal Commands for Phase 3 Setup
# Copy and paste these commands into your terminal

# ============================================================================
# PHASE 3: AI NEWS NAVIGATOR (RAG) — COMPLETE SETUP COMMANDS
# ============================================================================

echo "
╔════════════════════════════════════════════════════════════════════════════╗
║                    PHASE 3 SETUP COMMANDS                                  ║
║         NewsET AI News Navigator with RAG                                  ║
╚════════════════════════════════════════════════════════════════════════════╝
"

# ============================================================================
# STEP 0: Prerequisites (one-time)
# ============================================================================

echo "
════════════════════════════════════════════════════════════════════════════
1️⃣  INSTALL PREREQUISITES (one-time)
════════════════════════════════════════════════════════════════════════════
"

echo "Installing Ollama via Homebrew..."
echo "  brew install ollama"

echo ""
echo "Or download from: https://ollama.ai"
echo ""

# ============================================================================
# STEP 1: Install Python packages
# ============================================================================

echo "
════════════════════════════════════════════════════════════════════════════
2️⃣  INSTALL PYTHON PACKAGES (run once)
════════════════════════════════════════════════════════════════════════════
"

CMD1="cd /Users/navdeeop/Developer/projects/AI_News/backend && /opt/homebrew/bin/python3.11 -m pip install ollama==0.2.1 -q"
echo "Running: $CMD1"
echo ""
$CMD1

echo "✓ Python packages installed"
echo ""

# ============================================================================
# STEP 2: Build RAG Index
# ============================================================================

echo "
════════════════════════════════════════════════════════════════════════════
3️⃣  BUILD RAG INDEX (Terminal 1)
════════════════════════════════════════════════════════════════════════════

Copy and paste this command:

    cd /Users/navdeeop/Developer/projects/AI_News/backend && \\
    PYTHONPATH=. /opt/homebrew/bin/python3.11 scripts/build_rag_index.py

Expected output:
    === Phase 3 RAG Index Build ===
    ✓ Chunking complete. XXX new chunks created.
    Embedding XXX chunks...
    ✓ Chunk embedding complete.
    ✓ Chunk index ready. ZZZ vectors, dim=384
    ✓ RAG index ready: ZZZ chunk vectors

"

# ============================================================================
# STEP 3: Start Ollama
# ============================================================================

echo "
════════════════════════════════════════════════════════════════════════════
4️⃣  START OLLAMA (Terminal 2 — keep running)
════════════════════════════════════════════════════════════════════════════

Copy and paste this command:

    ollama serve

Expected output:
    2026/03/20 10:30:00 routes.go:1048: listening on 127.0.0.1:11434

If you see 'Model not found' error, run in Terminal 3:
    ollama pull llama3

"

# ============================================================================
# STEP 4: Start API Server
# ============================================================================

echo "
════════════════════════════════════════════════════════════════════════════
5️⃣  START API SERVER (Terminal 3)
════════════════════════════════════════════════════════════════════════════

Copy and paste this command:

    cd /Users/navdeeop/Developer/projects/AI_News/backend && \\
    PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --host 0.0.0.0 --port 8000

Expected output:
    Starting up NewsET API...
      ✓ Phase 2: Article embeddings & FAISS ready
      ✓ Phase 3: Chunks & RAG index ready
      ✓ Ollama available for RAG
    ✓ API ready on http://localhost:8000
    INFO: Application startup complete.
    INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

"

# ============================================================================
# TESTING
# ============================================================================

echo "
════════════════════════════════════════════════════════════════════════════
🧪 TEST ENDPOINTS (Terminal 4)
════════════════════════════════════════════════════════════════════════════
"

echo "
TEST 1: Health Check
──────────────────────────────────────────────────────────────────────────

curl http://localhost:8000/health | python3 -m json.tool

Expected:
{
  \"status\": \"ok\",
  \"faiss_articles\": 326,
  \"faiss_chunks\": 1200,
  \"ollama_available\": true
}

"

echo "
TEST 2: List Interest Categories
──────────────────────────────────────────────────────────────────────────

curl http://localhost:8000/interests | python3 -m json.tool

Expected:
[
  \"stocks\",
  \"startup\",
  \"macro\",
  \"corporate\",
  \"crypto\",
  \"real_estate\"
]

"

echo "
TEST 3: Streaming RAG Briefing
──────────────────────────────────────────────────────────────────────────

curl -X POST http://localhost:8000/briefing \\
  -H \"Content-Type: application/json\" \\
  -d '{\"question\": \"What is happening with AI startups in India?\", \"stream\": true}'

Expected: Tokens stream in real-time

"

echo "
TEST 4: Non-Streaming RAG Briefing with Sources
──────────────────────────────────────────────────────────────────────────

curl -X POST http://localhost:8000/briefing \\
  -H \"Content-Type: application/json\" \\
  -d '{\"question\": \"What is the inflation situation?\", \"stream\": false}' | python3 -m json.tool

Expected:
{
  \"answer\": \"The Reserve Bank of India...\",
  \"sources\": [
    {
      \"title\": \"RBI unlikely to hike rates...\",
      \"source\": \"The Times of India\",
      \"url\": \"https://...\",
      \"score\": 0.723
    }
  ]
}

"

echo "
TEST 5: Multi-Turn Follow-up
──────────────────────────────────────────────────────────────────────────

curl -X POST http://localhost:8000/ask \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"question\": \"What about startups regulatory changes?\",
    \"history\": [
      {\"role\": \"user\", \"content\": \"What is happening with startups?\"},
      {\"role\": \"assistant\", \"content\": \"Indian startups are growing rapidly...\"}
    ],
    \"stream\": false
  }' | python3 -m json.tool

"

# ============================================================================
# SUMMARY
# ============================================================================

echo "
════════════════════════════════════════════════════════════════════════════
📋 QUICK SUMMARY
════════════════════════════════════════════════════════════════════════════

Phase 3 Files Created:
  ✓ rag/chunker.py          — Article chunking
  ✓ rag/chunk_store.py      — Chunk FAISS index
  ✓ rag/retriever.py        — Query → chunks
  ✓ rag/prompt_builder.py   — LLM prompt assembly
  ✓ rag/llm.py              — Ollama wrapper
  ✓ api/main.py             — /briefing + /ask endpoints
  ✓ scripts/build_rag_index.py — Build script

API Endpoints:
  POST /briefing           → Main RAG briefing endpoint
  POST /ask               → Multi-turn follow-up
  GET  /health            → Health check with chunk count
  GET  /interests         → Interest categories
  POST /feed              → Personalized recommendations (Phase 2)

"

echo "
════════════════════════════════════════════════════════════════════════════
✨ PHASE 3 IS READY!
════════════════════════════════════════════════════════════════════════════

To get started:
  1. Follow the 5 steps above in separate terminals
  2. Test with curl commands from Step 5
  3. Integrate with frontend
  4. Build a Streamlit/React UI

Documentation:
  • PHASE3_SETUP.md → Detailed setup guide
  • rag/chunker.py → Chunk settings
  • rag/llm.py → LLM configuration

Questions or issues?
  • Check PHASE3_SETUP.md Troubleshooting section
  • Verify Ollama is running: curl http://localhost:11434/api/tags
  • Verify chunks are embedded: see build_rag_index.py

"
