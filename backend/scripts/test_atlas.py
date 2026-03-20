# scripts/test_atlas.py
from data_pipeline.utils.db import get_db

db = get_db()
db["articles"].insert_one({"test": True})
print(f"✓ Connected to Atlas. DB: {db.name}")
db["articles"].delete_one({"test": True})
print("✓ Test document cleaned up")