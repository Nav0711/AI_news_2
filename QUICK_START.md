# ⚡ MyET Quick Start (5 Minutes)

Get MyET running in under 5 minutes.

---

## 📋 Prerequisites (Already Have?)

- Python 3.11+
- Node.js 18+
- MongoDB URI (get from MongoDB Atlas)
- Google Gemini API key (get free at Google AI Studio)

---

## 🚀 Run in 3 Steps

### Step 1: Backend Setup (2 minutes)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env - add your keys:
# MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?appName=myET
# GEMINI_API_KEY=your_api_key_here

# Start server
uvicorn api.main:app --reload
```

**Server running at:** `http://localhost:8000`

---

### Step 2: Frontend Setup (2 minutes)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# (Frontend .env usually doesn't need changes)

# Start dev server
npm run dev
```

**App running at:** `http://localhost:5173`

---

### Step 3: Verify It Works (1 minute)

```bash
# In new terminal, test API health
curl http://localhost:8000/health

# Should see:
# {
#   "status": "healthy",
#   "ai_engine": "available"
# }
```

Open http://localhost:5173 → Register → Try it!

---

## ⚙️ Configuration Essentials

### Backend .env (Most Important)

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=myET
GEMINI_API_KEY=your-api-key-here
ENVIRONMENT=development
```

### Frontend .env (Optional - Usually Works As-Is)

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 🎯 Key Features to Try

1. **Register Account**
   - Click "Get Started"
   - Sign up with email

2. **Personalized Feed**
   - Select interests
   - Feed updates automatically

3. **AI Briefing**
   - Click "Ask AI a Question"
   - Get instant analysis

4. **Multi-Language Translation**
   - Switch language in sidebar
   - Article simplified for reading level
   - Available: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati

---

## 🐛 Troubleshooting 30-Second Fixes

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `source venv/bin/activate` first |
| Port 8000/5173 in use | Kill process or change port |
| Blank page | Check browser console (F12) |
| "Service unavailable" | Enable billing in Google Cloud |
| LoginFailed | Register new account first |

**Still stuck?** See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

## 📚 Next Steps

- **Full setup guide:** See [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **API documentation:** Visit `http://localhost:8000/docs`
- **Architecture details:** See [README.md](./README.md)
- **Production deploy:** See README → Docker section

---

## 💡 Pro Tips

```bash
# Run both servers in background
cd backend && uvicorn api.main:app --reload &
cd frontend && npm run dev &

# Hot reload enabled - edit code and it updates instantly

# Monitor logs in another terminal
tail -f backend/uvicorn_logs.txt
```

---

**Ready?** Open `http://localhost:5173` and start! 🚀
