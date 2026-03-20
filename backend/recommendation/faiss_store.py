# recommendation/faiss_store.py
import numpy as np
import faiss
from data_pipeline.utils.db import get_db

# Global index + article ID map — loaded once, reused for all requests
_index = None
_article_ids = []    # Maps FAISS integer position → MongoDB _id string

def build_index() -> faiss.IndexFlatIP:
    """
    Load all embeddings from MongoDB and build a FAISS IndexFlatIP.
    IndexFlatIP = Inner Product = cosine similarity (when vectors are normalized).
    Resets and rebuilds the global index + ID map.
    """
    global _index, _article_ids

    db = get_db()
    col = db["articles"]

    docs = list(col.find(
        {"embedding": {"$ne": None}},
        {"_id": 1, "embedding": 1}
    ))

    if not docs:
        raise ValueError("No embedded articles found. Run embed_pending_articles() first.")

    print(f"Building FAISS index from {len(docs)} articles...")

    vectors = np.array([d["embedding"] for d in docs], dtype="float32")
    dim = vectors.shape[1]   # 384 for all-MiniLM-L6-v2

    _index = faiss.IndexFlatIP(dim)
    _index.add(vectors)

    _article_ids = [str(d["_id"]) for d in docs]

    print(f"✓ FAISS index built. {_index.ntotal} vectors, dim={dim}")
    return _index

def get_index() -> faiss.IndexFlatIP:
    """Return the global index, building it if needed."""
    if _index is None:
        build_index()
    return _index

def search(query_vector: np.ndarray, top_k: int = 20) -> list[dict]:
    """
    Search FAISS for the top_k most similar articles to query_vector.
    Returns list of dicts: [{article_id, score}, ...]
    """
    index = get_index()

    # FAISS expects shape (1, dim)
    query = np.array([query_vector], dtype="float32")
    scores, positions = index.search(query, top_k)

    results = []
    for score, pos in zip(scores[0], positions[0]):
        if pos == -1:   # FAISS returns -1 for empty slots
            continue
        results.append({
            "article_id": _article_ids[pos],
            "score": float(score),
        })
    return results