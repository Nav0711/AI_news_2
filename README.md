# 🚀 MyET – AI Native Financial News Platform

> An advanced **AI-powered financial news platform** that delivers personalized, intelligent news experiences for Indian business markets in under 5 minutes.

Combines machine learning recommendations, Gemini AI briefings, multi-language translation, and story tracking in a sleek, dark-themed interface with red accents.

![MyET](https://img.shields.io/badge/Status-Actively%20Developed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Node.js](https://img.shields.io/badge/Node.js-18+-green)

---

## ⚡ **Quick Start (5 Minutes)**

### Prerequisites
- Python 3.11+, Node.js 18+, MongoDB account, Google Gemini API key

### 3-Step Setup

**Step 1: Backend Setup**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # Add MONGO_URI and GEMINI_API_KEY
uvicorn api.main:app --reload
```

**Step 2: Frontend Setup**
```bash
cd frontend  # New terminal
npm install
cp .env.example .env
npm run dev
```

**Step 3: Access & Test**
```bash
# Open in browser:
http://localhost:5173

# Test API:
curl http://localhost:8000/health
```

**✅ Done!** Register an account and start using MyET.

---

## ⏱️ Time Estimates
| Step | Duration |
|------|----------|
| Prerequisites Installation | 10-20 min |
| Backend Setup | 5-10 min |
| Frontend Setup | 5-10 min |
| Running Locally | 2-3 min |
| **Total** | **22-43 min** |

---

## 🎯 Key Features

### 📰 **Personalized News Feed**
- ML-powered article recommendation engine using FAISS vector embeddings
- User profile tracking based on interests and reading behavior
- Intelligent ranking by relevance and category

### 🤖 **AI Briefings**
- Google Gemini-powered contextual briefings
- Streaming responses for real-time insights
- Indian market focus with export/regulatory context
- Follow-up question support with conversation history

### 🌍 **Regional Language Support**
- Multi-language translation: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati
- Simplified explanations for non-expert readers
- Culturally adapted news interpretations
- Vernacular AI orchestrator for seamless experiences

### 📊 **Story Arc Tracking**
- Timeline visualization of evolving business stories
- Entity extraction and relationship mapping
- Clustered article grouping by narrative

### 🎬 **Video Summaries**
- AI-generated video content from articles (Phase 5)
- Quick visual briefings

### 📈 **Market Statistics**
- Real-time market indices (Sensex, Nifty, Bitcoin, Forex)
- Stock ticker integration via yfinance

---

## 🏗️ Architecture Overview

### **Three-Phase Architecture**

#### Phase 2: Personalized Recommendation Engine
- **FAISS Vector Embeddings**: Sentence-transformers for semantic similarity
- **User Profiling**: Interest-based segmentation
- **Ranking Algorithm**: Relevance scoring with click-through weighting

#### Phase 3: RAG (Retrieval-Augmented Generation)
- **Gemini AI Integration**: Context-aware briefings
- **MongoDB Storage**: Article persistence and context retrieval
- **Streaming API**: Real-time response generation

#### Phase 5: Vernacular News Engine
- **Multi-language Translation**: Gemini-powered localization
- **Article Simplification**: Accessible explanations for general audiences
- **Video Generation**: Programmatic video creation from articles

### **Tech Stack**

**Backend:**
- FastAPI 0.111 - High-performance async web framework
- Python 3.11+ - Language runtime
- MongoDB 4.6 - NoSQL database with SRV support
- FAISS 1.8 - Vector similarity search
- Google Generativeai 0.5.4 - Gemini AI models (2.5-flash)
- Sentence-Transformers 2.7 - Semantic embeddings
- APScheduler 3.10 - Task scheduling
- Uvicorn 0.29 - ASGI server

**Frontend:**
- React 18+ - UI framework
- TypeScript - Type-safe JavaScript
- Vite - Lightning-fast bundler
- Tailwind CSS - Utility-first styling
- ShadCN UI - Accessible component library
- TanStack React Query - Server state management
- React Router - Client-side routing
- Sonner - Toast notifications
- Lucide Icons - SVG icon library

**Infrastructure:**
- Docker (optional) - Containerization
- CORS middleware - Cross-origin request handling

---

## 📋 Prerequisites & Installation

### **1️⃣ System Requirements**
- **macOS/Linux/Windows** with 4GB+ RAM
- **Internet connection** for API calls
- **Terminal/Command Prompt** access

### **2️⃣ Install Python 3.11+**
```bash
# macOS (with Homebrew)
brew install python@3.11

# Windows: Download from https://www.python.org/downloads/
# Check "Add Python to PATH"

# Verify installation
python3 --version  # Should show 3.11+
```

### **3️⃣ Install Node.js 18+**
```bash
# macOS (with Homebrew)
brew install node@18

# Windows: Download from https://nodejs.org/

# Verify installation
node --version      # Should show v18+
npm --version       # Should show 9+
```

### **4️⃣ Create MongoDB Atlas Account**
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a free cluster (M0)
4. Create database user with username/password
5. Add your IP to IP whitelist: Click "Add Current IP Address"
6. Copy connection string: `mongodb+srv://username:password@cluster.mongodb.net/?appName=myET`

### **5️⃣ Get Google Gemini API Key**
1. Go to https://ai.google.dev/tutorials/setup
2. Click "Get API Key"
3. **IMPORTANT:** Enable billing in Google Cloud Console
   - Go to https://console.cloud.google.com/
   - Select your project → Billing
   - Add payment method
   - **Wait 5 minutes** for activation
4. Copy your API key

### **6️⃣ Get News API Key (Optional)**
1. Go to https://newsapi.org/register
2. Sign up for free account
3. Copy your API key from dashboard

---

## 🚀 Complete Setup Instructions

### **Step 0: Clone Repository**
```bash
git clone https://github.com/Nav0711/AI_news_2.git
cd AI_news_2

# You should see:
# ├── backend/
# ├── frontend/
# ├── docs/
# └── README.md
```

---

## 🔧 Backend Setup (Detailed)

### **Terminal 1: Backend**

#### Navigate to Backend
```bash
cd backend
```

#### Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

#### Install Dependencies
```bash
pip install -r requirements.txt

# This installs:
# - FastAPI, Uvicorn (web framework)
# - MongoDB driver (pymongo)
# - Google Generativeai (Gemini AI)
# - FAISS (vector search)
# - Sentence-Transformers (embeddings)
# - APScheduler (background tasks)
# - And 10+ more packages

# Takes 30-60 seconds
```

#### Create .env File
```bash
# Copy template
cp .env.example .env

# Edit with your credentials (use your favorite editor)
nano .env  # or vim, code, etc.
```

**Fill in these values:**
```env
# Required - Get from steps above
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=myET
GEMINI_API_KEY=your_gemini_api_key_here
NEWS_API_KEY=your_newsapi_key_here  # Optional

# Optional - Defaults are fine
ENVIRONMENT=development
BACKEND_PORT=8000
DEBUG=false
LOG_LEVEL=INFO
```

#### Verify Setup
```bash
# Test if all imports work
python -c "
import fastapi
import google.generativeai
import pymongo
import faiss
from sentence_transformers import SentenceTransformer
print('✓ All imports successful!')
"
```

#### Start Backend Server
```bash
uvicorn api.main:app --reload

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**✅ Backend running at:** `http://localhost:8000`

#### Verify Backend Health
```bash
# In another terminal
curl http://localhost:8000/health | jq

# Should return:
# {
#   "status": "online",
#   "database": "connected",
#   "ai_engine": "available",
#   "version": "1.0.0"
# }
```

**API Documentation:** `http://localhost:8000/docs` (Swagger UI)

---

## 🎨 Frontend Setup (Detailed)

### **Terminal 2: Frontend**

#### Navigate to Frontend
```bash
cd frontend
```

#### Install Dependencies
```bash
npm install

# Alternative: Use bun for faster installation
# bun install

# This installs 200+ packages
# Takes 1-2 minutes
```

#### Create .env File
```bash
# Copy template
cp .env.example .env

# Default values usually work, but verify:
# VITE_API_BASE_URL=http://localhost:8000/api
# VITE_ENVIRONMENT=development
```

#### Start Frontend Server
```bash
npm run dev

# Alternative:
# bun run dev

# Expected output:
# VITE v8.0.1 ready in 180 ms
#
# ➜  Local:   http://localhost:5173/
# ➜  Network: http://192.168.x.x:5173/
```

**✅ Frontend running at:** `http://localhost:5173`

---

## ✅ Verify Everything Works

### **Test Backend**
```bash
# In Terminal 3
curl http://localhost:8000/health | jq

# Expected response:
curl http://localhost:8000/interests

# Should return list of interests
```

### **Open Frontend**
```
Open browser: http://localhost:5173
```

**You should see:**
- ✅ MyET login page with red theme
- ✅ Register button
- ✅ Dark theme with red accents

### **Test Registration**
1. Click "Register"
2. Enter email and password
3. Click "Register" → Should redirect to login
4. Login with your credentials
5. Select interests (Stocks, Startups, Macro, Crypto, Real Estate)
6. Should see personalized news feed

---

## 🎬 Build for Production

### **Frontend Production Build**
```bash
cd frontend

# Build
npm run build

# Preview
npm run preview

# Test: Should be accessible at http://localhost:4173
```

### **Backend Production Run**
```bash
cd backend
source venv/bin/activate

# Run without hot reload
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

---

## 📂 Project Structure

```
AI_news_2/
├── backend/                          # FastAPI server
│   ├── api/
│   │   ├── main.py                  # FastAPI app & routes
│   │   ├── auth.py                  # Authentication endpoints
│   │   └── news_stats.py            # Market statistics
│   ├── data_pipeline/
│   │   ├── fetchers/                # News API clients
│   │   ├── cleaners/                # Text sanitization
│   │   ├── models/                  # Data models
│   │   ├── utils/                   # Database & user utilities
│   │   └── scheduler.py             # APScheduler jobs
│   ├── rag/
│   │   └── llm_gemini.py            # Gemini integration
│   ├── recommendation/
│   │   ├── embedder.py              # Sentence-transformers
│   │   ├── faiss_store.py           # FAISS index management
│   │   ├── recommender.py           # Ranking algorithm
│   │   └── user_profile.py          # User interest segments
│   ├── vernacular/
│   │   ├── translator.py            # Multi-language translation
│   │   ├── simplifier.py            # Text simplification
│   │   └── orchestrator.py          # Pipeline orchestration
│   ├── story_arc/
│   │   ├── clustering.py            # Story grouping
│   │   ├── entity_extraction.py     # NLP-based extraction
│   │   └── timeline.py              # Chronological ordering
│   ├── video/
│   │   └── generator.py             # Video synthesis
│   ├── scripts/
│   │   ├── build_index.py           # FAISS index builder
│   │   └── verify_pipeline.py       # Data quality checks
│   ├── static/
│   │   └── videos/                  # Generated video storage
│   ├── requirements.txt
│   ├── .env.example
│   └── uvicorn_logs.txt
│
├── frontend/                         # React SPA
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Index.tsx            # Main dashboard
│   │   │   ├── Login.tsx            # Authentication
│   │   │   ├── Register.tsx         # User signup
│   │   │   └── Onboarding.tsx       # Interest selection
│   │   ├── components/
│   │   │   ├── Navbar.tsx           # Header navigation
│   │   │   ├── Sidebar.tsx          # Left panel
│   │   │   ├── FeedPanel.tsx        # Article feed
│   │   │   ├── AIBriefingPanel.tsx  # AI briefings
│   │   │   ├── StoryArcPanel.tsx    # Timeline visualization
│   │   │   ├── VideoPlayer.tsx      # Video component
│   │   │   └── ui/                  # ShadCN components
│   │   ├── lib/
│   │   │   ├── api.ts               # API client
│   │   │   ├── auth.tsx             # Auth context
│   │   │   └── types.ts             # TypeScript types
│   │   ├── hooks/                   # Custom React hooks
│   │   ├── App.tsx                  # Root component
│   │   └── index.css                # Tailwind styles
│   ├── public/                       # Static assets
│   ├── package.json
│   ├── tailwind.config.ts           # Tailwind config
│   ├── tsconfig.json
│   ├── vite.config.ts               # Vite configuration
│   └── .env.example
│
├── docs/
│   ├── ai_native_news_prd.md        # Product requirements
│   └── architecture.md              # Technical architecture
│
└── README.md                         # This file

```

---

## 🔌 API Endpoints

### **Authentication**
```http
POST   /api/auth/register          # Create new user account
POST   /api/auth/login             # Authenticate user
POST   /api/auth/logout            # End session
```

### **Recommendations (Phase 2)**
```http
POST   /feed                        # Get personalized news feed
GET    /interests                   # List available interests
```

### **AI Briefings (Phase 3)**
```http
POST   /briefing                    # Get AI-generated briefing
POST   /ask                         # Follow-up questions
```

### **Vernacular (Phase 5)**
```http
GET    /languages                   # List supported languages
POST   /translate                   # Translate article
POST   /video-summary               # Generate video
```

### **System**
```http
GET    /health                      # Health check
GET    /market-stats                # Real-time market data
```

**Full API Documentation:** `http://localhost:8000/docs`

---

## ⚙️ Environment Configuration (Detailed)

### **Backend .env Configuration**

Create `backend/.env` with these variables:

```env
# ==== REQUIRED ====

# MongoDB Database Connection
# Format: mongodb+srv://username:password@cluster.mongodb.net/?appName=myET
# Get from: https://www.mongodb.com/cloud/atlas
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/?appName=myET

# Google Gemini AI API Key
# Get from: https://ai.google.dev/tutorials/setup
# IMPORTANT: Enable billing in Google Cloud Console first!
GEMINI_API_KEY=your-gemini-api-key-here

# News API Key for article fetching
# Get from: https://newsapi.org/register (optional but recommended)
NEWS_API_KEY=your-newsapi-key-here

# ==== OPTIONAL (Defaults are fine) ====

# Database name (default: myET_db)
MONGO_DB_NAME=myET_db

# Environment type: development or production
ENVIRONMENT=development

# Backend server port (default: 8000)
BACKEND_PORT=8000

# Enable debug mode (true/false)
DEBUG=false

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Feature toggles
VIDEO_GENERATION_ENABLED=false
RAG_ENABLED=true
VERNACULAR_ENABLED=true

# Cache settings (seconds)
CACHE_EXPIRATION=3600

# Article fetching
MAX_ARTICLES_PER_FETCH=1000
ARTICLE_FETCH_INTERVAL=1800  # 30 minutes

# Gemini Model Configuration
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1000
```

### **Frontend .env Configuration**

Create `frontend/.env` with these variables:

```env
# ==== REQUIRED ====

# Backend API base URL
# Must match where backend is running
VITE_API_BASE_URL=http://localhost:8000/api

# ==== OPTIONAL (Usually don't need changes) ====

# Environment type: development or production
VITE_ENVIRONMENT=development

# App name
VITE_APP_NAME=MyET

# API timeout (milliseconds)
VITE_API_TIMEOUT=30000

# Enable frontend debugging
VITE_DEBUG=false
VITE_DEBUG_API=false

# Analytics (optional)
VITE_ANALYTICS_ENABLED=false
VITE_ANALYTICS_KEY=

# Feature flags
VITE_ENABLE_VIDEO=false
VITE_ENABLE_TRANSLATION=true
VITE_ENABLE_STORY_ARC=true

# UI settings
VITE_DARK_MODE=true
VITE_PRIMARY_COLOR=rgb(255, 0, 0)  # Red color
VITE_ACCENT_COLOR=rgb(255, 0, 0)   # Red accent
```

---

## 🔐 Authentication

MyET uses **JWT (JSON Web Tokens)** for secure authentication:

1. **Register** with email/password
2. **Login** to receive JWT token
3. **Token stored** in browser localStorage
4. **Auto-refresh** on page navigation

**User Interests:**
- Stocks & Mutual Funds
- Startups & Funding
- Macroeconomics
- Cryptocurrency
- Real Estate

Protected routes require valid JWT token.

---

## 🎤 Usage Examples

### **1. Get Personalized Feed**
```bash
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["stocks", "macro"],
    "top_k": 20
  }'
```

### **2. Generate AI Briefing**
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the latest RBI policy changes?",
    "stream": true
  }'
```

### **3. Translate Article**
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Stock Market Update",
    "content": "The Sensex rose 2% due to...",
    "language_code": "hi",
    "simplify": true
  }'
```

### **4. Check Market Stats**
```bash
curl http://localhost:8000/market-stats
```

---

## 🐳 Docker Deployment (Optional)

### **Build Docker Image**
```bash
cd backend
docker build -t myET:latest .
```

### **Run Container**
```bash
docker run -p 8000:8000 \
  --env-file .env \
  myET:latest
```

---

## 🧪 Testing

### **Backend Tests**
```bash
cd backend
pytest tests/ -v
```

### **Frontend Tests**
```bash
cd frontend
npm run test
```

---

## 🐛 Troubleshooting Guide

### **Critical Issues**

#### Backend Won't Start
```
Error: uvicorn: command not found
```
**Solution:**
```bash
# Verify venv is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall uvicorn
pip install uvicorn==0.29.0

# Try again
uvicorn api.main:app --reload
```

---

```
Error: ModuleNotFoundError: No module named 'fastapi'
```
**Solution:**
```bash
# Ensure venv is activated
which python  # Should show .../venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
pip list | grep fastapi
```

---

#### Database Connection Failed
```
Error: ServerSelectionTimeoutError: connection refused
```

**Cause 1: Wrong MONGO_URI**
```bash
# Check .env file
grep MONGO_URI backend/.env

# Should look like:
# mongodb+srv://username:password@cluster.mongodb.net/?appName=myET
```

**Cause 2: IP Address Not Whitelisted**
- Go to https://www.mongodb.com/cloud/atlas
- Click "Network Access" 
- Click "Add IP Address"
- Click "Add Current IP Address"
- Wait 2-3 minutes for changes to apply

**Cause 3: Wrong Credentials**
- Go to MongoDB Atlas → "Database Access"
- Reset password for your user
- Update MONGO_URI in .env
- Restart backend

**Cause 4: Cluster Paused**
- Go to MongoDB Atlas → "Database"
- Check if cluster is paused
- Click "Resume" if needed

---

#### API Returns 503 Errors
```
Error: Service Unavailable
```

**Solution 1: Check Gemini API Status**
```bash
# Check health endpoint
curl http://localhost:8000/health

# If "ai_engine": "unavailable"
# Cause: GEMINI_API_KEY not set or billing not enabled
```

**Solution 2: Enable Billing in Google Cloud**
```
1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Select your project
3. Go to Billing section
4. Add payment method (credit card required)
5. Wait 5 minutes for activation
6. Restart backend
```

**Solution 3: Test API Key Directly**
```bash
python -c "
import google.generativeai as genai
genai.configure(api_key='YOUR_KEY')
response = genai.GenerativeModel('gemini-2.5-flash').generate_content('Hello')
print(response.text)
"
```

---

### **Frontend Issues**

#### Page Blank / Not Loading
```
Symptom: White/blank page, no content
```

**Solution 1: Check Browser Console Errors**
```
Press F12 → Console tab
Look for red error messages
Copy error text and search GitHub issues
```

**Solution 2: Verify Backend is Running**
```bash
# Check if backend is accessible
curl http://localhost:8000/health

# If fails, start backend:
cd backend
source venv/bin/activate
uvicorn api.main:app --reload
```

**Solution 3: Check API URL Configuration**
```bash
# Check frontend .env
cat frontend/.env

# Should be:
# VITE_API_BASE_URL=http://localhost:8000/api
```

**Solution 4: Clear Browser Cache**
```
Press Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)
Select "All time"
Click "Clear data"
Reload page (Ctrl+R or Cmd+R)
```

---

#### Port Already in Use
```
Error: Port 5173 is already in use
```

**Solution 1: Kill Process Using Port (macOS/Linux)**
```bash
# Find process using port 5173
lsof -i :5173

# Kill the process (use PID from above)
kill -9 <PID>

# Start frontend again
npm run dev
```

**Solution 2: Use Different Port**
```bash
# Run on port 3000 instead
npm run dev -- --port 3000

# Access at http://localhost:3000
```

**Solution 3: On Windows**
```bash
# Find process using port
netstat -ano | findstr :5173

# Kill process
taskkill /PID <PID> /F

# Start frontend again
npm run dev
```

---

#### API Calls Failing
```
Error: Failed to fetch from API
```

**Diagnosis:**
```bash
# Test API directly
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests":["stocks"]}'

# Should return articles or error message
```

**Solution 1: Backend Not Running**
```bash
# Check if running
curl http://localhost:8000/health

# If not, follow "Backend Won't Start" section above
```

**Solution 2: CORS Error**
- Check browser console (F12) for "Access-Control-Allow-Origin" error
- Restart both backend and frontend
- Ensure VITE_API_BASE_URL is correct

**Solution 3: Wrong Endpoint**
- Check API docs: `http://localhost:8000/docs`
- Verify endpoint name matches
- Check request method (GET vs POST)
- Verify JSON format

---

### **Authentication Issues**

#### Login Fails
```
Error: Invalid credentials / Unauthorized
```

**Solution 1: Verify User Account Exists**
```bash
# Check MongoDB
mongosh "your_connection_string"
> use myET_db
> db.users.find()

# If empty, register new user via frontend
```

**Solution 2: Clear Browser Storage**
```
Press F12 → Application tab
Click "LocalStorage"
Click "http://localhost:5173"
Click "Clear All"
Reload page and try again
```

**Solution 3: Password Hashing Issue**
- Try registering a new account with different email
- Use a simple password without special characters
- Check response for specific error messages

---

#### JWT Token Expired
```bash
# Check backend logs
tail -f backend/uvicorn_logs.txt

# Look for "token expired" messages
```

**Solution:**
```
Press F12 → Application → LocalStorage
Find "auth_token" entry
Delete it
Reload page and login again
```

---

### **Database Issues**

#### No Data in Feed
```
Symptom: Articles not loading in personalized feed
```

**Solution 1: Background Job Not Running**
```bash
# Check scheduler logs
grep "scheduler" backend/uvicorn_logs.txt

# Background job fetches articles every 30 minutes
# Wait 5-10 minutes after startup
```

**Solution 2: Check Article Count**
```bash
# Open MongoDB
mongosh "your_connection_string"
> use myET_db
> db.articles.countDocuments()

# If 0, articles need to be fetched
# Try making a request to /feed endpoint
```

**Solution 3: Rebuild FAISS Index**
```bash
cd backend
python scripts/build_index.py

# This rebuilds vector embeddings
# Takes 2-5 minutes
```

---

#### Slow Queries / Feed Taking 10+ Seconds
```bash
# Measure response time
time curl http://localhost:8000/feed \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"interests":["stocks"]}'
```

**Solution 1: Add MongoDB Indexes**
```bash
mongosh "your_connection_string"
> use myET_db
> db.articles.createIndex({published_at: -1})
> db.articles.createIndex({category: 1})
```

**Solution 2: Rebuild FAISS Index**
```bash
cd backend
python scripts/build_index.py
```

**Solution 3: Optimize Backend**
```bash
# In backend .env, add:
CACHE_EXPIRATION=3600
MAX_ARTICLES_PER_FETCH=500
```

---

### **Feature-Specific Issues**

#### Video Generation Fails
```
Error: Video generation not available
```

**Solution 1: Enable Feature**
```bash
# In backend .env
VIDEO_GENERATION_ENABLED=true

# Restart backend
```

**Solution 2: Install Missing Dependencies**
```bash
pip install opencv-python pillow
pip install -r requirements.txt
```

---

#### Translation Returns Error
```
Error: Vernacular API not available
```

**Solution 1: Check Gemini API**
```bash
# Test directly
curl http://localhost:8000/languages

# Should return supported languages
```

**Solution 2: Verify Language Code**
Supported languages: `hi` (Hindi), `ta` (Tamil), `te` (Telugu), `bn` (Bengali), `mr` (Marathi), `gu` (Gujarati)

```bash
# Example: Translate to Hindi
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Stock Market Update",
    "content": "The Sensex rose 2%...",
    "language_code": "hi",
    "simplify": true
  }'
```

---

### **Performance Issues**

#### High Memory Usage
```bash
# Check memory (macOS)
top -l 1 | grep -E "python|python3"

# Check memory (Linux)
ps aux | grep python
```

**Solution 1: Reduce FAISS Index Size**
```bash
# In backend .env
MAX_ARTICLES_PER_FETCH=100
```

**Solution 2: Clear Caches Periodically**
```bash
# In backend .env
CACHE_EXPIRATION=600  # 10 minutes instead of 1 hour
```

---

### **Debug Tools**

#### View Live Logs
```bash
# Backend logs
cd backend
tail -f uvicorn_logs.txt

# Frontend console
# F12 → Console tab
```

#### Test API Endpoints
```bash
# Test health check
curl http://localhost:8000/health | jq

# Test interests
curl http://localhost:8000/interests | jq

# Test feed with proper JSON
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests":["stocks"],"top_k":5}' | jq
```

#### Database Browser
```bash
# MongoDB Compass (GUI)
# Download: https://www.mongodb.com/try/download/compass

# MongoDB Shell (CLI)
mongosh "your_connection_string"
```

#### Monitor Open Ports
```bash
# Check backend port
lsof -i :8000  # macOS/Linux

# Check frontend port
lsof -i :5173  # macOS/Linux

# Windows
netstat -ano | findstr :8000
```

---

### **Getting Help**

#### Enable Debug Mode
```bash
# In backend .env
DEBUG=true
LOG_LEVEL=DEBUG

# In frontend .env
VITE_DEBUG=true
VITE_DEBUG_API=true

# Restart both servers
```

#### Collect Debug Information
```bash
# Get versions
python --version
node --version
npm --version

# List installed packages
pip list > backend_packages.txt
npm list > frontend_packages.txt

# Save logs
cp backend/uvicorn_logs.txt backend_logs_backup.txt
```

#### Create GitHub Issue with:
1. Error message (exact text)
2. Steps to reproduce
3. Debug output
4. Your environment (OS, Python version, Node version)
5. What you've already tried

**GitHub Issues:** https://github.com/Nav0711/AI_news_2/issues

---

## ✅ Troubleshooting Checklist

After fixing issues, verify:
- [ ] Backend running: `curl http://localhost:8000/health`
- [ ] Frontend running: `curl http://localhost:5173`
- [ ] Can register account
- [ ] Can login to app
- [ ] Feed loads in < 3 seconds
- [ ] Can ask AI questions
- [ ] Can translate articles
- [ ] Browser console has no errors (F12)
- [ ] Network tab shows 200 responses

---

## 📊 Database Schema

### **Articles Collection**
```json
{
  "_id": ObjectId,
  "title": string,
  "content": string,
  "source": string,
  "url": string,
  "published_at": timestamp,
  "category": string,
  "embedding": [float],
  "created_at": timestamp
}
```

### **Users Collection**
```json
{
  "_id": ObjectId,
  "email": string,
  "password_hash": string,
  "interests": [string],
  "read_article_ids": [string],
  "created_at": timestamp
}
```

---

## 🚀 Performance Optimization

### **Backend**
- **FAISS Vector Indexing**: O(log n) search complexity
- **Redis Caching** (optional): For frequent queries
- **Connection Pooling**: MongoDB SRV connections
- **Async Processing**: APScheduler background tasks

### **Frontend**
- **Code Splitting**: Route-based lazy loading
- **Image Optimization**: Responsive images
- **Query Caching**: TanStack React Query
- **CSS Minification**: Tailwind CSS tree-shaking

---

## 📚 API Response Examples

### **Briefing Response**
```json
{
  "question": "Latest RBI decisions?",
  "answer": "The RBI maintained repo rate at 6.5%...",
  "articles_used": 5,
  "model": "gemini-2.5-flash"
}
```

### **Feed Response**
```json
[
  {
    "id": "article_123",
    "title": "Sensex surges on strong corporate earnings",
    "description": "Benchmark index...",
    "source": "Economic Times",
    "published_at": "2026-03-29T10:30:00Z",
    "category": "stocks",
    "url": "https://...",
    "relevance_score": 0.95
  }
]
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/Nav0711/AI_news_2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Nav0711/AI_news_2/discussions)
- **Email**: navdeep@example.com

---

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- MongoDB for database infrastructure
- Sentence-Transformers for embeddings
- FAISS for vector similarity search
- React and FastAPI communities
- ShadCN UI for component library

---

## 📈 Roadmap

### **Q2 2026**
- [ ] GraphQL API support
- [ ] Real-time WebSocket updates
- [ ] Advanced sentiment analysis
- [ ] Custom alert system

### **Q3 2026**
- [ ] Mobile app (React Native)
- [ ] Podcast generation
- [ ] AR news visualization
- [ ] Multi-user collaboration

### **Q4 2026**
- [ ] Enterprise deployment guide
- [ ] Custom model fine-tuning
- [ ] Advanced analytics dashboard
- [ ] API rate limiting tiers

---

**Last Updated:** March 29, 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅