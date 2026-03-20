# data-pipeline/utils/db.py
import os
import atexit
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(
            os.getenv("MONGO_URI"),
            
            # Pool settings — M0 free tier safe limits
            maxPoolSize=10,        # Max 10 concurrent connections (M0 allows 500 total)
            minPoolSize=1,         # Keep 1 warm connection alive always
            maxIdleTimeMS=45000,   # Close idle connections after 45s (Atlas drops at 60s)
            
            # Timeout settings
            connectTimeoutMS=10000,       # 10s to establish connection
            serverSelectionTimeoutMS=10000, # 10s to find a server
            socketTimeoutMS=30000,        # 30s for any single operation
            
            # Retry on transient network blips (common on free tier)
            retryWrites=True,
            retryReads=True,
        )
        # Register cleanup so the pool closes cleanly on process exit
        atexit.register(_client.close)

    return _client

def get_db():
    client = get_client()
    return client[os.getenv("MONGO_DB_NAME", "newset")]

def setup_indexes():
    """Create MongoDB indexes for optimal query performance."""
    try:
        db = get_db()
        collection = db["articles"]
        
        # Ensure we can quickly find articles by URL (deduplication)
        collection.create_index("url_hash", unique=False)
        
        # Fast queries by category
        collection.create_index("category")
        
        # Sort by published date
        collection.create_index("published_at")
        
        # Compound index for filtering by category and date
        collection.create_index([("category", 1), ("published_at", -1)])
        
        print("✓ MongoDB indexes created/verified")
        return True
    except Exception as e:
        print(f"✗ Failed to create indexes: {e}")
        return False

def ping():
    """Health check — call this on startup to catch config errors early."""
    try:
        get_client().admin.command("ping")
        print("✓ Atlas connection healthy")
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ Atlas connection failed: {e}")
        return False