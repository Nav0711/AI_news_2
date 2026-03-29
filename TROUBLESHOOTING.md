# 🔧 MyET Troubleshooting Guide

Quick solutions for common issues

---

## 🚨 Critical Issues

### Backend Won't Start
```
Error: uvicorn: command not found
```
**Solution:**
```bash
# Verify venv is activated
source venv/bin/activate
# or on Windows:
venv\Scripts\activate

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

### Database Connection Failed
```
Error: ServerSelectionTimeoutError: connection refused
```
**Causes & Solutions:**

1. **Wrong MONGO_URI:**
   ```bash
   # Check .env file
   grep MONGO_URI backend/.env
   
   # Should look like:
   # mongodb+srv://username:password@cluster.mongodb.net/?appName=myET
   ```

2. **IP Address Not Whitelisted:**
   - Go to MongoDB Atlas dashboard
   - Click "Network Access" 
   - Click "Add IP Address"
   - Click "Add Current IP Address"
   - Wait 2-3 minutes

3. **Wrong Credentials:**
   - Go to MongoDB Atlas
   - Click "Database Access"
   - Reset password for your user
   - Update MONGO_URI in .env
   - Restart backend

4. **Cluster Paused:**
   - Go to MongoDB Atlas
   - Click "Database"
   - Check if cluster is paused
   - Click "Resume" if needed

---

### API Returns 503 Errors
```
Error: Service Unavailable
```
**Solutions:**

1. **Gemini API Not Available:**
   ```bash
   # Check health endpoint
   curl http://localhost:8000/health
   
   # If "ai_engine": "unavailable"
   # Cause: GEMINI_API_KEY not set or billing not enabled
   ```

2. **Billing Not Enabled:**
   ```
   1. Go to Google Cloud Console: https://console.cloud.google.com/
   2. Select your project
   3. Go to Billing section
   4. Add payment method (even if not charged)
   5. Wait 5 minutes for activation
   6. Restart backend
   ```

3. **API Key Invalid:**
   ```bash
   # Test directly
   python -c "
   import google.generativeai as genai
   genai.configure(api_key='YOUR_KEY')
   response = genai.GenerativeModel('gemini-2.5-flash').generate_content('Hello')
   print(response.text)
   "
   ```

---

## 🌐 Frontend Issues

### Page Blank / Not Loading
```
Symptom: White/blank page, no content
```
**Solutions:**

1. **Check Console Errors:**
   ```
   Press F12 → Console tab
   Look for red error messages
   Copy and search GitHub issues
   ```

2. **Backend Not Running:**
   ```bash
   # Check if backend is accessible
   curl http://localhost:8000/health
   
   # If fails, start backend:
   cd backend
   source venv/bin/activate
   uvicorn api.main:app --reload
   ```

3. **Wrong API URL:**
   ```bash
   # Check frontend .env
   cat frontend/.env
   
   # Should be:
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

4. **Browser Cache Issue:**
   ```
   Press Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)
   Clear all cache
   Reload page (Ctrl+R or Cmd+R)
   ```

---

### Port Already in Use
```
Error: Port 5173 is already in use
```
**Solution:**

```bash
# Find process using port
lsof -i :5173  # macOS/Linux

# Kill the process
kill -9 <PID>

# Or use different port
npm run dev -- --port 3000

# Then access at http://localhost:3000
```

---

### API Calls Failing
```
Error: Failed to fetch from API
```
**Diagnosis:**

```bash
# Test API directly
curl http://localhost:8000/feed -X POST \
  -H "Content-Type: application/json" \
  -d '{"interests":["stocks"]}'

# Should return articles or error message
```

**Solutions:**

1. **Backend Not Running:**
   ```bash
   # Check if running
   curl http://localhost:8000/health
   
   # If not, follow Backend Won't Start section
   ```

2. **CORS Issue:**
   - Check browser console (F12)
   - Look for "Access-Control-Allow-Origin" error
   - Restart both backend and frontend

3. **Wrong Endpoint:**
   - Check API docs: `http://localhost:8000/docs`
   - Verify endpoint URL in code
   - Check request method (GET vs POST)

---

## 🔐 Authentication Issues

### Login Fails
```
Error: Invalid credentials / Unauthorized
```
**Solutions:**

1. **Ensure User Exists:**
   ```bash
   # MongoDB CLI
   mongosh "your_connection_string"
   > use myET_db
   > db.users.find()
   
   # If empty, register new user via frontend
   ```

2. **Password Hashing Issue:**
   - Try registering new account
   - Use different email/password
   - Check response for errors

3. **JWT Token Expired:**
   ```bash
   # Clear localStorage
   # F12 → Application → LocalStorage → Clear All
   # Reload and login again
   ```

---

### Persistent Login Issues
```bash
# Check backend logs for auth errors
tail -f backend/uvicorn_logs.txt

# Check if auth tables exist
mongosh "your_connection_string"
> use myET_db
> db.users.find().pretty()
```

---

## 📊 Database Issues

### No Data in Feed
```
Symptom: Articles not loading in personalized feed
```
**Solutions:**

1. **Background Job Not Running:**
   ```bash
   # Check scheduler logs
   grep "scheduler" backend/uvicorn_logs.txt
   
   # Background fetching articles might take 5-10 minutes
   ```

2. **No Articles in Database:**
   ```bash
   # Check articles count
   mongosh "your_connection_string"
   > use myET_db
   > db.articles.countDocuments()
   
   # If 0, manually trigger fetch:
   # POST to /feed endpoint
   ```

3. **FAISS Index Not Built:**
   ```bash
   # Rebuild index
   cd backend
   python scripts/build_index.py
   ```

---

### Slow Queries
```
Symptom: Feed takes 10+ seconds to load
```
**Solutions:**

1. **Add MongoDB Index:**
   ```bash
   mongosh "your_connection_string"
   > use myET_db
   > db.articles.createIndex({published_at: -1})
   > db.articles.createIndex({category: 1})
   ```

2. **Rebuild FAISS Index:**
   ```bash
   cd backend
   python scripts/build_index.py
   ```

3. **Increase Server Resources:**
   - If using cloud DB, upgrade cluster
   - Add more RAM to server
   - Enable compression in MongoDB

---

## 🎬 Feature-Specific Issues

### Video Generation Fails
```
Error: Video generation not available
```
**Solutions:**

1. **Enable Feature:**
   ```bash
   # In backend .env
   VIDEO_GENERATION_ENABLED=true
   
   # Restart backend
   ```

2. **Missing Dependencies:**
   ```bash
   pip install opencv-python pillow
   ```

---

### Translation Returns Error
```
Error: Vernacular API not available
```
**Solutions:**

1. **Check Gemini API:**
   ```bash
   # Test directly
   curl http://localhost:8000/languages
   
   # If fails, check Gemini billing
   ```

2. **Language Not Supported:**
   - Supported: hi, ta, te, bn, mr, gu
   - Check language code in request

---

## 📈 Performance Issues

### Slow API Responses
**Diagnosis:**
```bash
# Measure response time
time curl http://localhost:8000/health

# Should be < 100ms for health
# Feed requests < 2-3 seconds
```

**Solutions:**

1. **Enable Response Caching:**
   ```bash
   # In backend .env
   CACHE_EXPIRATION=3600  # 1 hour
   ```

2. **Optimize Database Queries:**
   ```bash
   # Increase FAISS batch size
   # Limit articles per fetch
   MAX_ARTICLES_PER_FETCH=500  # Reduce from 1000
   ```

3. **Use Connection Pooling:**
   ```bash
   # In backend .env
   MONGO_POOL_SIZE=20
   ```

---

### High Memory Usage
**Diagnosis:**
```bash
# macOS
top -l 1 | grep -E "python|python3"

# Linux
ps aux | grep python
```

**Solutions:**

1. **Reduce FAISS Index Size:**
   ```bash
   # Limit articles
   MAX_ARTICLES_PER_FETCH=100
   ```

2. **Clear Caches Periodically:**
   ```bash
   # Add to .env
   CACHE_EXPIRATION=600  # 10 minutes instead of 1 hour
   ```

3. **Restart Periodically:**
   ```bash
   # Create restart script
   # Restart backend every 6 hours
   ```

---

## 🧰 Debug Tools

### View Live Logs
```bash
# Backend logs
cd backend
tail -f uvicorn_logs.txt

# Frontend console
# F12 → Console tab
```

### Test API Endpoints
```bash
# Install curl (if needed)
# macOS: brew install curl
# Windows: Already installed

# Test health
curl http://localhost:8000/health

# Test feed with proper JSON
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests":["stocks"],"top_k":5}'
```

### Database Browser
```bash
# MongoDB Compass (GUI)
# Download from: https://www.mongodb.com/try/download/compass

# MongoDB Shell (CLI)
mongosh "your_connection_string"
```

### Network Analysis
```bash
# Check open ports
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Check DNS
nslookup api.example.com
```

---

## 🆘 Still Stuck?

### Get Help
1. **Check Documentation:**
   - [Main README.md](../README.md)
   - [Setup Guide](./SETUP_GUIDE.md)
   - [API Docs](http://localhost:8000/docs)

2. **Search GitHub Issues:**
   - https://github.com/Nav0711/AI_news_2/issues
   - Search for your error message

3. **Enable Debug Mode:**
   ```bash
   # In backend .env
   DEBUG=true
   LOG_LEVEL=DEBUG
   
   # In frontend .env
   VITE_DEBUG=true
   VITE_DEBUG_API=true
   ```

4. **Collect Debug Info:**
   ```bash
   # Backend version
   python -c "import fastapi; print(fastapi.__version__)"
   
   # Node version
   node --version
   
   # Python version
   python --version
   
   # Installed packages
   pip list > backend_packages.txt
   npm list > frontend_packages.txt
   ```

5. **Create GitHub Issue with:**
   - Error message (exact)
   - Steps to reproduce
   - Debug output
   - Your environment (OS, versions)

---

## ✅ Verification Checklist

After troubleshooting, verify:

- [ ] Backend running: `curl http://localhost:8000/health`
- [ ] Frontend running: `curl http://localhost:5173`
- [ ] Can login to app
- [ ] Feed loads in < 3 seconds
- [ ] Can ask AI questions
- [ ] Can translate articles
- [ ] Browser console has no errors
- [ ] Network tab shows 200 responses

---

**Last Updated:** March 29, 2026  
**For Latest:** Check GitHub repository
