#!/usr/bin/env bash
# Test the AI News Backend Pipeline
# Shows what to expect when running the scheduler

echo "========================================="
echo "AI NEWS BACKEND PIPELINE - QUICK START"
echo "========================================="
echo ""

# Step 1: Navigate to backend
echo "Step 1: Navigate to backend directory"
echo "$ cd backend"
echo ""

# Step 2: Activate virtual environment
echo "Step 2: Activate virtual environment"
echo "$ source venv/bin/activate"
echo ""
echo "✓ You should see (venv) in your terminal prompt now"
echo ""

# Step 3: Run the pipeline
echo "Step 3: Run the scheduler (Option A - Full scheduler)"
echo "$ python3 -m data_pipeline.scheduler"
echo ""
echo "Expected Output:"
echo "  ✓ Atlas connection healthy"
echo "  ✓ MongoDB indexes created/verified"
echo "  [2026-03-18T19:46:12.940507] Starting news fetch pipeline..."
echo "    ✓ Fetched 92 raw articles for topic: stocks"
echo "    ✓ Fetched 14 raw articles for topic: startup"
echo "    ✓ Fetched 5 raw articles for topic: macro"
echo "    ✓ Fetched 0 raw articles for topic: corporate"
echo "    ✓ Fetched 0 raw articles for topic: crypto"
echo "  ✓ Pipeline complete. +90 new articles. Total in DB: 90"
echo ""
echo "  [Scheduler will then wait for 30 minutes before next fetch]"
echo "  Press Ctrl+C to stop"
echo ""

# Step 4: Alternative - One time run
echo "Step 4: Run pipeline once (Option B - Development/Testing)"
echo "$ python3 -c \"from data_pipeline.fetchers.newsapi_fetchers import run_full_pipeline; run_full_pipeline(days_back=1)\""
echo ""

# Step 5: Run from convenience script
echo "Step 5: Run via convenience script (Option C - Easiest)"
echo "$ cd backend"
echo "$ ./run_pipeline.sh"
echo ""
echo "========================================="
