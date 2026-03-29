# 🚀 MyET Development Setup Guide

**Quick Reference:** Complete setup from zero to running locally

---

## ⏱️ Time Estimates

| Step | Duration | Difficulty |
|------|----------|-----------|
| Prerequisites Installation | 10-20 min | Easy |
| Backend Setup | 5-10 min | Easy |
| Frontend Setup | 5-10 min | Easy |
| Running Locally | 2-3 min | Very Easy |
| **Total** | **22-43 min** | **Easy** |

---

## 📋 Checklist

### Prerequisites
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB account created
- [ ] Google Gemini API key obtained
- [ ] News API key obtained (optional)

### Backend
- [ ] Backend directory entered
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file created with API keys
- [ ] Backend started on localhost:8000

### Frontend
- [ ] Frontend directory entered
- [ ] Dependencies installed
- [ ] `.env` file created
- [ ] Frontend started on localhost:5173

---

## Step-by-Step Setup

### 1️⃣ Install Prerequisites

#### Python 3.11+
```bash
# macOS (with Homebrew)
brew install python@3.11

# Windows
# Download from: https://www.python.org/downloads/
# Check "Add Python to PATH"

# Verify installation
python3 --version  # Should show 3.11+
```

#### Node.js 18+
```bash
# macOS (with Homebrew)
brew install node@18

# Windows
# Download from: https://nodejs.org/

# Verify installation
node --version      # Should show v18+
npm --version       # Should show 9+
```

#### MongoDB Atlas (Cloud Database)
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a free cluster (M0)
4. Create database user with username/password
5. Add your IP to IP whitelist: `Add Current IP Address`
6. Copy connection string: `mongodb+srv://username:password@cluster.mongodb.net/?appName=myET`

#### Google Gemini API
1. Go to https://ai.google.dev/tutorials/setup
2. Click "Get API Key"
3. **Important:** Enable billing on the Google Cloud project
   - Go to Google Cloud Console
   - Select your project
   - Navigate to Billing
   - Add payment method
   - Wait 5 minutes for activation
4. Copy your API key

#### News API (Optional)
1. Go to https://newsapi.org/register
2. Sign up for free account
3. Copy your API key from dashboard

---

### 2️⃣ Clone Repository

```bash
# Clone the project
git clone https://github.com/Nav0711/AI_news_2.git
cd AI_news_2

# You should see this structure:
# ├── backend/
# ├── frontend/
# ├── docs/
# └── README.md
```

---

### 3️⃣ Backend Setup

#### Open Terminal 1: Backend
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
# - MongoDB driver
# - Google Gemini AI
# - FAISS (vector search)
# - Sentence-Transformers
# - And 15+ more packages

# Takes 30-60 seconds
```

#### Create .env File
```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your favorite editor

# Required values to add:
# NEWS_API_KEY=your_key
# GEMINI_API_KEY=your_key
# MONGO_URI=your_uri
```

#### Verify Setup
```bash
# Test if all imports work
python -c "
import fastapi
import google.generativeai
import pymongo
import faiss
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

Test it:
```bash
# In new terminal
curl http://localhost:8000/docs  # API docs page
curl http://localhost:8000/health  # Health check
```

---

### 4️⃣ Frontend Setup

#### Open Terminal 2: Frontend
```bash
# In a new terminal (keep backend running in Terminal 1)
cd frontend
```

#### Install Dependencies
```bash
npm install

# This installs 200+ packages using npm
# Alternative: use bun (faster)
# bun install

# Takes 1-2 minutes
```

#### Create .env File
```bash
# Copy template
cp .env.example .env

# Default values are usually fine:
# VITE_API_BASE_URL=http://localhost:8000/api
# VITE_ENVIRONMENT=development
```

#### Start Frontend Server
```bash
npm run dev

# Or with bun:
# bun run dev

# Expected output:
# VITE v8.0.1 ready in 180 ms
# ➜  Local:   http://localhost:5173/
# ➜  Network: http://192.168.x.x:5173/
```

**✅ Frontend running at:** `http://localhost:5173`

---

### 5️⃣ Access the Application

#### Navigate to Frontend
```
http://localhost:5173
```

#### Expected to see:
- ✅ MyET login page
- ✅ Register button
- ✅ Dark theme with red accents

#### Test Registration
1. Click "Register"
2. Enter email and password
3. Click "Register"
4. Should redirect to login
5. Login with credentials
6. Select interests (Stocks, Startups, Macro, etc.)
7. Should see personalized feed

#### API Documentation
```
http://localhost:8000/docs
```

Shows all available endpoints with test interface

---

## 📊 Verify Everything Works

### Backend Health Check
```bash
# Terminal 1
curl http://localhost:8000/health | jq

# Expected response:
# {
#   "status": "online",
#   "database": "connected",
#   "ai_engine": "unavailable",  # OK if API quota is exhausted
#   "version": "1.0.0"
# }
```

### Frontend Load Test
```bash
# Terminal 3
curl -s http://localhost:5173 | grep -o "MyET" | head -3

# Should see "MyET" in HTML
```

### API Test
```bash
# Get available interests
curl http://localhost:8000/interests

# Expected: List of interest categories
```

---

## 🎯 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
1. Confirm venv is activated: `source venv/bin/activate`
2. Verify pip installation: `pip list | grep fastapi`
3. Reinstall: `pip install -r requirements.txt`

### Issue: "Port 5173 already in use"
**Solution:**
```bash
# Use different port
npm run dev -- --port 3000

# Or kill process using port
lsof -i :5173  # Find process
kill -9 <PID>   # Kill it
```

### Issue: "MongoDB connection timeout"
**Solution:**
1. Check MONGO_URI in `.env`
2. Add your IP to MongoDB Atlas whitelist
3. Verify credentials are correct
4. Check internet connection

### Issue: "GEMINI_API_KEY returns 429 quota exceeded"
**Solution:**
1. Enable billing in Google Cloud Console
2. Go to https://console.cloud.google.com/
3. Add valid payment method
4. Wait 5 minutes for activation
5. Restart backend

### Issue: "Frontend shows 'API unavailable'"
**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check VITE_API_BASE_URL in frontend `.env`
3. Restart frontend: `npm run dev`
4. Clear browser cache: `Ctrl+Shift+Delete`

---

## 🔄 Workflow: Making Changes

### Backend Changes
```bash
# Automatic with --reload flag
# Just save file, server reloads automatically
# Check http://localhost:8000/docs for changes

# If issues:
# 1. Press Ctrl+C in backend terminal
# 2. Run: uvicorn api.main:app --reload
```

### Frontend Changes
```bash
# Automatic with Vite HMR
# Just save file, page reloads automatically
# Check http://localhost:5173 for changes

# If issues:
# 1. Press Ctrl+C in frontend terminal
# 2. Run: npm run dev
# 3. Clear browser cache if needed
```

---

## 📦 Production Build

### Frontend Build
```bash
cd frontend
npm run build
# Creates optimized dist/ folder
# ~50KB gzipped
```

### Backend Deployment
```bash
cd backend
# Remove --reload for production
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Or with Gunicorn (recommended)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app
```

---

## 🧪 Testing

### Backend Unit Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Unit Tests
```bash
cd frontend
npm run test
```

### Frontend E2E Tests
```bash
cd frontend
npm run playwright  # If configured
```

---

## 📚 Useful Commands

### Backend
```bash
# Restart server
# Press Ctrl+C, then run:
uvicorn api.main:app --reload

# Check dependencies
pip list

# Update dependencies
pip install -r requirements.txt --upgrade

# View logs
tail -f uvicorn_logs.txt
```

### Frontend
```bash
# Restart dev server
# Press Ctrl+C, then run:
npm run dev

# Check dependencies
npm list

# Update dependencies
npm update

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Database
```bash
# Check MongoDB connection
python -c "from data_pipeline.utils.db import get_db; db = get_db(); print('Connected!' if db.command('ping') else 'Failed')"

# View data (requires MongoDB CLI)
mongosh "your_connection_string"
> use myET_db
> db.articles.find().limit(5)
```

---

## 🌐 Network Access

### From Different Machine
```bash
# Get your machine IP
ifconfig | grep inet  # macOS/Linux
ipconfig              # Windows

# Access from other machine
# Backend: http://192.168.x.x:8000
# Frontend: http://192.168.x.x:5173

# Update frontend .env:
VITE_API_BASE_URL=http://192.168.x.x:8000/api
```

---

## 📈 Next Steps After Setup

1. **Explore API:** Visit `http://localhost:8000/docs`
2. **Register Account:** Create test user on frontend
3. **Select Interests:** Complete onboarding flow
4. **View Feed:** See personalized articles
5. **Test Briefings:** Ask AI questions
6. **Try Translation:** Translate to other languages

---

## 📞 Support

**Issues?**
- Check troubleshooting section above
- Read main [README.md](../README.md)
- Check relevant documentation in `/docs/`
- Open GitHub issue: https://github.com/Nav0711/AI_news_2/issues

**Want to contribute?**
1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

---

**Happy Coding! 🎉**

For more details, see the [main README](../README.md) file.
