# recommendation/recommender.py
from bson import ObjectId
from data_pipeline.utils.db import get_db
from recommendation.faiss_store import search
from recommendation.user_profile import build_query_vector

def get_personalized_feed(
    interests: list[str],
    read_article_ids: list[str] = None,
    top_k: int = 20,
    exclude_read: bool = True,
) -> list[dict]:
    """
    Main entry point for the recommendation engine.

    Returns a list of enriched article dicts, ranked by relevance.
    Each dict includes the full article + similarity score.
    """
    # 1. Build query vector from user profile
    query_vector = build_query_vector(
        interests=interests,
        read_article_ids=read_article_ids or [],
    )

    # 2. Search FAISS — get more than top_k to allow for filtering
    candidates = search(query_vector, top_k=top_k * 2)

    # 3. Filter out already-read articles
    if exclude_read and read_article_ids:
        read_set = set(read_article_ids)
        candidates = [c for c in candidates if c["article_id"] not in read_set]

    candidates = candidates[:top_k]

    if not candidates:
        return []

    # 4. Fetch full article documents from MongoDB
    db = get_db()
    col = db["articles"]

    ids = [ObjectId(c["article_id"]) for c in candidates]
    score_map = {c["article_id"]: c["score"] for c in candidates}

    docs = list(col.find(
        {"_id": {"$in": ids}},
        {
            "_id": 1, "title": 1, "description": 1,
            "source": 1, "published_at": 1,
            "category": 1, "url": 1, "word_count": 1
        }
    ))

    # 5. Attach scores and sort by relevance
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        doc["relevance_score"] = round(score_map.get(doc["_id"], 0.0), 4)

    docs.sort(key=lambda d: d["relevance_score"], reverse=True)
    return docs