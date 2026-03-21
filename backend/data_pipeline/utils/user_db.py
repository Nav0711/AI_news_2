from typing import Optional, Dict, Any, List
from .db import get_db

def get_user_collection():
    db = get_db()
    return db["users"]

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    col = get_user_collection()
    return col.find_one({"email": email})

def create_user(email: str, password_hash: str) -> Dict[str, Any]:
    col = get_user_collection()
    user_doc = {
        "email": email,
        "password_hash": password_hash,
        "profile_type": None,
        "interests": [],
        "created_at": __import__('datetime').datetime.utcnow()
    }
    result = col.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return user_doc

def update_user_profile(email: str, profile_type: str, interests: List[str]) -> bool:
    col = get_user_collection()
    result = col.update_one(
        {"email": email},
        {"$set": {"profile_type": profile_type, "interests": interests}}
    )
    return result.modified_count > 0

def setup_user_indexes():
    try:
        col = get_user_collection()
        col.create_index("email", unique=True)
        print("✓ MongoDB user indexes created")
    except Exception as e:
        print(f"✗ Failed to create user indexes: {e}")
