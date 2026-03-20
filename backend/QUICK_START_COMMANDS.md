# 🎯 Quick Terminal Commands — NewsET Backend Startup

**Copy-paste commands to get API running in 2 minutes**

---

## ✅ Pre-flight Checklist

```bash
# 1. Verify Python 3.11 is available
/opt/homebrew/bin/python3.11 --version

# 2. Verify you're in backend directory
cd /Users/navdeeop/Developer/projects/AI_News/backend && pwd

# 3. Verify .env file exists
ls -la .env
```

**Expected output:** Python 3.11.x, path to backend/, and .env file listed

---

## 🔑 Step 1: Configure Environment (2 minutes)

### A. Get Gemini API Key

```bash
# Open in browser (manual step)
# Visit: https://aistudio.google.com/app/apikey
# Click "Create API Key"
# Copy the key (starts with AIzaSy...)
```

### B. Create/Update .env File

```bash
# Create .env in backend directory
cat > .env << 'EOF'
GEMINI_API_KEY=AIzaSyC_YOUR_KEY_HERE
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=newsdb
FETCH_STORIES=false
EOF

# Verify it was created
cat .env
```

**Alternative: Edit manually**
```bash
nano .env
# Add your keys, press Ctrl+O, Enter, Ctrl+X
```

---

## 📦 Step 2: Install Dependencies (1 minute)

```bash
# Navigate to backend
cd /Users/navdeeop/Developer/projects/AI_News/backend

# Install all Python dependencies
/opt/homebrew/bin/python3.11 -m pip install -r requirements.txt -q

# Verify installation
/opt/homebrew/bin/python3.11 -m pip list | grep -E "fastapi|google-generativeai|sentence-transformers|faiss"
```

**Expected:** Should show all packages installed

---

## 🚀 Step 3: Start API Server

```bash
# Set up environment and start server
cd /Users/navdeeop/Developer/projects/AI_News/backend

PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
✓ Phase 2: FAISS ready
✓ Phase 3: Gemini ready
✓ Phase 5: Vernacular Engine ready
```

**Server is now live!** Leave this terminal open.

---

## 🧪 Step 4: Test in New Terminal

**Open a NEW terminal** (keep API server running)

### Test 1: Health Check
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

**Expected:** Status "ok" with all components ✓

### Test 2: Get Languages (Phase 5)
```bash
curl http://localhost:8000/languages | python3 -m json.tool | head -20
```

**Expected:** List of languages (hi, ta, te, bn, mr, gu)

### Test 3: Get Interests (Phase 2)
```bash
curl http://localhost:8000/interests
```

**Expected:** 
```json
["stocks", "startup", "macro", "corporate", "crypto", "real_estate"]
```

### Test 4: Get Personalized Feed (Phase 2)
```bash
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["stocks"],
    "read_article_ids": [],
    "top_k": 3
  }' | python3 -m json.tool | head -50
```

**Expected:** Array of 3 ranked articles

### Test 5: AI Briefing (Phase 3)
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is happening with Indian startups?",
    "stream": false,
    "category_filter": "startup"
  }' | python3 -m json.tool
```

**Expected:** AI-generated answer based on articles

### Test 6: Translate Article (Phase 5)
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Reserve Bank Raises Interest Rates",
    "content": "The Reserve Bank of India (RBI) announced a 50 basis point increase in repo rate. This decision aims to control inflation and stabilize the rupee. Higher repo rates increase borrowing costs for banks.",
    "language_code": "hi",
    "simplify": true,
    "stream": false
  }' | python3 -m json.tool | head -30
```

**Expected:** Translated Hindi content

---

## 📝 Common Command Patterns

### Get All 6 Languages Translations (Loop)

```bash
ARTICLE="Reserve Bank Raises Interest Rates"
CONTENT="The RBI announced a 50 basis point rate increase to control inflation."

for LANG in hi ta te bn mr gu; do
  echo "=== Translating to $LANG ==="
  curl -s -X POST http://localhost:8000/translate \
    -H "Content-Type: application/json" \
    -d "{
      \"title\": \"$ARTICLE\",
      \"content\": \"$CONTENT\",
      \"language_code\": \"$LANG\",
      \"stream\": false
    }" | jq '.translated_headline' 2>/dev/null || echo "Error"
  echo ""
done
```

### Multi-Turn Conversation (Phase 3)

```bash
# First question
RESPONSE=$(curl -s -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question":"Impact of RBI rate hike?","stream":false}')

FIRST_ANSWER=$(echo $RESPONSE | jq -r '.answer')

echo "First answer received, asking follow-up..."

# Follow-up question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"Which sectors are most affected?\",
    \"history\": [
      {\"role\":\"user\",\"content\":\"Impact of RBI rate hike?\"},
      {\"role\":\"assistant\",\"content\":\"$FIRST_ANSWER\"}
    ],
    \"stream\": false
  }" | jq '.answer'
```

### Streaming Response (Real-time)

```bash
# Phase 5 translation with streaming
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Article",
    "content": "Testing streaming response...",
    "language_code": "hi",
    "stream": true
  }'

# Phase 3 briefing with streaming
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question":"News briefing?","stream":true}'
```

### Save Response to File

```bash
# Save translation
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"Content","language_code":"hi","stream":false}' \
  > translation_output.json

# View it
cat translation_output.json | python3 -m json.tool

# Extract just translated content
jq '.translated_content' translation_output.json
```

---

## 🔧 Troubleshooting Commands

### Issue: "Connection refused" on port 8000

```bash
# Check if something is already using port 8000
lsof -i :8000

# Kill the process (if needed)
kill -9 <PID>

# Try a different port
PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --port 8001
```

### Issue: "GEMINI_API_KEY not found"

```bash
# Verify .env has the key
grep GEMINI_API_KEY .env

# If missing, add it
echo "GEMINI_API_KEY=your_key_here" >> .env

# Restart API server
```

### Issue: "ModuleNotFoundError: No module named 'google'"

```bash
# Install missing dependency
/opt/homebrew/bin/python3.11 -m pip install google-generativeai==0.5.4

# Verify
/opt/homebrew/bin/python3.11 -c "import google.generativeai; print('✓ Google AI installed')"
```

### Issue: Import errors on startup

```bash
# Test entire API imports
PYTHONPATH=. /opt/homebrew/bin/python3.11 -c "from api.main import app; print('✓ API loads successfully')"

# Test individual phases
PYTHONPATH=. /opt/homebrew/bin/python3.11 -c "from recommendation.faiss_store import FAISSStore; print('✓ Phase 2 loads')"
PYTHONPATH=. /opt/homebrew/bin/python3.11 -c "from rag.llm_gemini import ask; print('✓ Phase 3 loads')"
PYTHONPATH=. /opt/homebrew/bin/python3.11 -c "from vernacular.orchestrator import translate_with_context; print('✓ Phase 5 loads')"
```

### Check MongoDB Connection

```bash
# Test MongoDB URI (replace with your actual URI)
PYTHONPATH=. /opt/homebrew/bin/python3.11 << 'EOF'
from pymongo import MongoClient
import os
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client[os.getenv("MONGODB_DB", "newsdb")]
count = db.articles.count_documents({})
print(f"✓ Connected! Articles in DB: {count}")
EOF
```

### Monitor Server in Real-time

```bash
# While server is running, open another terminal

# Monitor CPU/Memory
top -p $(pgrep -f "uvicorn")

# Check open connections
lsof -p $(pgrep -f "uvicorn") | grep TCP
```

---

## 📊 Useful Info Commands

### Check Python Version
```bash
/opt/homebrew/bin/python3.11 --version
```

### Check Installed Packages
```bash
/opt/homebrew/bin/python3.11 -m pip list | grep -E "fastapi|google|sentence-transform|faiss|pymongo"
```

### Check Disk Usage
```bash
du -sh .
du -sh ../*
```

### View Recent Logs
```bash
# API logs are printed to terminal
# For persistent logging, add to server start:
# > api.log 2>&1

# Then view:
tail -f api.log
```

---

## 🎯 Quick Reference: All Endpoints

```bash
# Endpoint, Method, Description

GET     /health                 # Status check
GET     /interests              # Phase 2 - Interest categories
POST    /feed                   # Phase 2 - Personalized feed
POST    /briefing               # Phase 3 - AI briefing
POST    /ask                    # Phase 3 - Follow-up questions
GET     /languages              # Phase 5 - Supported languages
POST    /translate              # Phase 5 - Translate articles
GET     /docs                   # Interactive API docs
GET     /redoc                  # ReDoc documentation
```

---

## 🚀 Production Deployment Commands

### Deploy to Railway

```bash
# Login to Railway
railway login

# Link current directory to Railway project
railway link

# Set environment variables
railway variables set GEMINI_API_KEY=your_key
railway variables set MONGODB_URI=your_uri

# Deploy
railway up

# View logs
railway logs

# Get deployment URL
railway env
```

### Deploy to Render

```bash
# In render.com dashboard:
# 1. Connect GitHub repository
# 2. Create new Web Service
# 3. Set Python environment
# 4. Set build command: pip install -r backend/requirements.txt
# 5. Set start command: cd backend && uvicorn api.main:app --host 0.0.0.0
# 6. Add environment variables
```

### Docker Deployment

```bash
# Build Docker image
docker build -t newsET-api -f backend/Dockerfile .

# Run container locally
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e MONGODB_URI=your_uri \
  newsET-api

# Push to Docker Hub
docker tag newsET-api your-username/newsET-api:latest
docker push your-username/newsET-api:latest
```

---

## 📱 Testing with Alternative Tools

### Using httpie (more readable than curl)

```bash
# Install
brew install httpie

# Test endpoint
http GET http://localhost:8000/health

# POST request
http POST http://localhost:8000/feed \
  interests:='["stocks"]' top_k:=5
```

### Using Python requests

```python
import requests

# Test health
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test translation
data = {
    "title": "Test",
    "content": "Test content",
    "language_code": "hi",
    "stream": False
}
response = requests.post("http://localhost:8000/translate", json=data)
print(response.json())
```

---

## 🎪 Demo Scenario

**Complete workflow from start to finish:**

```bash
# 1. Start API in terminal 1
cd /Users/navdeeop/Developer/projects/AI_News/backend
PYTHONPATH=. /opt/homebrew/bin/python3.11 -m uvicorn api.main:app --port 8000 --reload

# 2. Wait for startup messages
# 3. In terminal 2, run:

# Get interests
echo "=== Step 1: Get Categories ==="
curl -s http://localhost:8000/interests | python3 -m json.tool

# Get personalized feed
echo "=== Step 2: Get Personalized Feed ==="
curl -s -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests":["startup"],"top_k":1}' | jq '.[] | .title'

# Get AI briefing
echo "=== Step 3: Get AI Briefing ==="
curl -s -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question":"Latest startup news?","stream":false}' | jq '.answer' | head -5

# Translate to Hindi
echo "=== Step 4: Translate to Hindi ==="
curl -s -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"title":"Startup Funding","content":"Latest startup funding round details...","language_code":"hi","stream":false}' \
  | jq '.translated_headline'

echo "✓ All systems operational!"
```

---

## 📞 Getting Help

### API Documentation
- **Automatic Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### External Resources
- Gemini API Docs: https://ai.google.dev/
- FastAPI: https://fastapi.tiangolo.com/
- MongoDB: https://docs.mongodb.com/
- FAISS: https://github.com/facebookresearch/faiss

---

**You're all set! Happy coding! 🎉**

