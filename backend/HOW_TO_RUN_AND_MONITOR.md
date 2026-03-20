# How to Run & Monitor the Backend Pipeline

## Quick Start (3 commands)

```bash
cd backend
source venv/bin/activate
python3 -m data_pipeline.scheduler
```

---

## Option 1: Full Scheduler (Production Mode)

### Start It:
```bash
cd backend
source venv/bin/activate
python3 -m data_pipeline.scheduler
```

### What You'll See:
```
✓ Atlas connection healthy
✓ MongoDB indexes created/verified

[2026-03-18T19:46:12.940507] Starting news fetch pipeline...
  ✓ Fetched 92 raw articles for topic: stocks
  ✓ Fetched 14 raw articles for topic: startup
  ✓ Fetched 5 raw articles for topic: macro
  ✓ Fetched 0 raw articles for topic: corporate
  ✓ Fetched 0 raw articles for topic: crypto

✓ Pipeline complete. +90 new articles. Total in DB: 90

[Wait 30 minutes for next fetch...]
```

### Important:
- **The script runs FOREVER** (that's normal - it's a scheduler)
- It fetches **every 30 minutes** automatically
- **Press `Ctrl+C`** to stop it gracefully
- Logs appear in real-time in your terminal

---

## Option 2: One-Time Fetch (Testing/Debug)

### Start It:
```bash
cd backend
source venv/bin/activate
python3 << 'EOF'
from data_pipeline.fetchers.newsapi_fetchers import run_full_pipeline
print("🚀 Starting pipeline...")
result = run_full_pipeline(days_back=1)
print(f"✅ Done! Check MongoDB for results")
EOF
```

### What You'll See:
```
🚀 Starting pipeline...

[2026-03-18T19:46:12.940507] Starting news fetch pipeline...
  ✓ Fetched 92 raw articles for topic: stocks
  ✓ Fetched 14 raw articles for topic: startup
  ...
✓ Pipeline complete. +90 new articles. Total in DB: 90

✅ Done! Check MongoDB for results
[Terminal returns to prompt]
```

### Advantage:
- Script **exits after 1 run** (good for testing)
- You can adjust `days_back=7` to fetch older articles
- Faster to iterate

---

## Option 3: Shell Script (Easiest)

### Start It:
```bash
./backend/run_pipeline.sh
```

### Same output as Option 1, but no need to remember commands

---

## How to See the Results

### Method 1: Terminal Output (Real-Time)
Just watch the terminal while it runs - you'll see:
```
✓ Pipeline complete. +90 new articles. Total in DB: 90
```

The `+90` means 90 **new** articles were added.

---

### Method 2: Check MongoDB in Terminal

**While scheduler is running in one terminal, open a SECOND terminal:**

```bash
# Terminal 2 - Check what's in MongoDB
cd backend
source venv/bin/activate

python3 << 'EOF'
from data_pipeline.utils.db import get_db

db = get_db()
collection = db["articles"]

# How many total articles?
total = collection.count_documents({})
print(f"📊 Total articles in DB: {total}")

# How many by category?
categories = collection.aggregate([
    {"$group": {"_id": "$category", "count": {"$sum": 1}}}
])
print("\n📂 Articles by category:")
for cat in categories:
    print(f"   {cat['_id']:10} → {cat['count']} articles")

# Show the 3 most recent articles
print("\n📰 Most recent articles:")
recent = collection.find().sort("published_at", -1).limit(3)
for i, article in enumerate(recent, 1):
    print(f"\n  [{i}] {article['title'][:60]}...")
    print(f"      Category: {article['category']}")
    print(f"      Source: {article['source']}")
    print(f"      Words: {article['word_count']}")
EOF
```

### Sample Output:
```
📊 Total articles in DB: 90

📂 Articles by category:
   stocks     → 42 articles
   startup    → 31 articles
   macro      →  12 articles
   crypto     →  5 articles
   corporate  →  0 articles

📰 Most recent articles:

  [1] Stock market surges as RBI signals rate cut...
      Category: stocks
      Source: Reuters
      Words: 287

  [2] Reliance startup hub launches AI accelerator program...
      Category: startup
      Source: Economic Times
      Words: 452

  [3] India's inflation drops to 4.2% in March...
      Category: macro
      Source: CNBC India
      Words: 318
```

---

### Method 3: MongoDB Compass GUI (Visual)

If you have MongoDB Compass installed:

1. Open MongoDB Compass
2. Connect with your MongoDB URI from `.env`
3. Navigate to: `newset` → `articles`
4. See articles displayed in a table with real-time updates

---

## Monitoring Checklist

### ✓ Script Started Successfully?
Look for:
```
✓ Atlas connection healthy
✓ MongoDB indexes created/verified
```

### ✓ Articles Being Fetched?
You should see lines like:
```
✓ Fetched 92 raw articles for topic: stocks
```

### ✓ Articles Being Stored?
You should see:
```
✓ Pipeline complete. +90 new articles. Total in DB: 90
```

### ✓ Is it Running Continually?
The scheduler shows:
```
✓ Scheduler started. Fetching every 30 minutes. Press Ctrl+C to stop.
```

Then waits. This is normal!

---

## Troubleshooting Output

### ❌ Error: "MongoDB connection failed"
```
✗ Atlas connection failed: [error details]
```
**Fix**: Check your `.env` file `MONGO_URI` credentials

### ❌ Error: "NewsAPI error"
```
✗ NewsAPI error for 'stocks': Your API key is invalid
```
**Fix**: Check `NEWS_API_KEY` in `.env`

### ❌ No articles stored despite fetching
```
✓ Fetched 92 raw articles for topic: stocks
✓ Pipeline complete. +0 new articles. Total in DB: 90
```
**Reason**: Articles were already in DB (duplicates filtered out). Run again to see change.

---

## Running in Background (Optional)

If you want the scheduler to run in the background on Mac:

```bash
# Start in background (logs won't show)
cd backend && nohup ./venv/bin/python3 -m data_pipeline.scheduler > pipeline.log 2>&1 &

# View live logs
tail -f pipeline.log

# Stop the process
pkill -f "data_pipeline.scheduler"
```

---

## Summary

| Task | Command |
|------|---------|
| **Run scheduler (forever)** | `python3 -m data_pipeline.scheduler` |
| **Run once (quick test)** | `python3 -c "from data_pipeline.fetchers.newsapi_fetchers import run_full_pipeline; run_full_pipeline(days_back=1)"` |
| **Run via script** | `./run_pipeline.sh` |
| **Check results in terminal** | `python3 [see Method 2 above]` |
| **View in MongoDB Compass** | Connect → newset → articles |
| **Stop scheduler** | `Ctrl+C` |

---

## Expected Output Timeline

```
Time: 0s
    ✓ Atlas connection healthy
    ✓ MongoDB indexes created

Time: 1-10s
    ✓ Fetched 92 raw articles (stocks)
    ✓ Fetched 14 raw articles (startup)
    ...

Time: 15s
    ✓ Pipeline complete. +90 new articles
    
Time: 15s - 30 min mark
    [Waiting for next fetch...]

Time: 30 min
    [Fetches again automatically]
```

---

**You're all set! Start with Option 2 for a quick test, then run Option 1 for production.** ✅
