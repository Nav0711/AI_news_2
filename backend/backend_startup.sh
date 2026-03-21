#!/bin/bash
# Unified startup script for AI_news_2 backend (Python 3.11 venv)
# Usage: bash backend_startup.sh

set -e

cd "$(dirname "$0")"

# 1. Activate venv if exists, else create
if [ ! -d "venv" ]; then
  echo "[INFO] Creating Python 3.11 venv..."
  python3.11 -m venv venv
fi
source venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Check .env
if [ ! -f ".env" ]; then
  echo "[ERROR] .env file missing! Please create backend/.env with API keys and DB config."
  exit 1
fi

# 4. Start FastAPI server
PYTHONPATH=. uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
