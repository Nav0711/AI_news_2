# recommendation/user_profile.py
import numpy as np
from sentence_transformers import SentenceTransformer
from recommendation.embedder import get_model

# Predefined interest categories → seed phrases for embedding
# These are tuned for the 4 NewsET user segments from the PRD
INTEREST_SEEDS = {
    "stocks":        "NSE BSE stock market equity mutual funds SIP SEBI",
    "startup":       "startup funding venture capital Series A founder unicorn",
    "macro":         "GDP inflation RBI monetary policy interest rate economy",
    "corporate":     "company earnings merger acquisition quarterly results",
    "crypto":        "cryptocurrency Bitcoin blockchain DeFi Web3 regulation",
    "real_estate":   "real estate property housing market RERA home loan",
}

def embed_interests(interest_keys: list[str]) -> np.ndarray:
    """
    Convert a list of interest keys (e.g. ['stocks', 'startup'])
    into a single averaged, normalized query vector.
    """
    model = get_model()
    seeds = [INTEREST_SEEDS.get(k, k) for k in interest_keys]

    vectors = model.encode(seeds, normalize_embeddings=True)
    avg = vectors.mean(axis=0)

    # Re-normalize after averaging
    avg = avg / np.linalg.norm(avg)
    return avg

def build_query_vector(
    interests: list[str],
    read_article_ids: list[str] = None,
    interest_weight: float = 0.7,
) -> np.ndarray:
    """
    Build a query vector from a user's interests + reading history.

    interests:          list of interest keys (e.g. ['stocks', 'macro'])
    read_article_ids:   MongoDB _id strings of recently read articles
    interest_weight:    how much to weight static interests vs reading history
                        0.7 = 70% interests, 30% history (good default)

    Returns a normalized 384-dim query vector.
    """
    from data_pipeline.utils.db import get_db
    from recommendation.embedder import get_model
    import numpy as np

    interest_vector = embed_interests(interests)

    if not read_article_ids:
        return interest_vector

    # Fetch embeddings of recently-read articles from MongoDB
    from bson import ObjectId
    db = get_db()
    col = db["articles"]

    read_docs = list(col.find(
        {"_id": {"$in": [ObjectId(id) for id in read_article_ids]},
         "embedding": {"$ne": None}},
        {"embedding": 1}
    ))

    if not read_docs:
        return interest_vector

    history_vectors = np.array([d["embedding"] for d in read_docs], dtype="float32")
    history_avg = history_vectors.mean(axis=0)
    history_avg = history_avg / np.linalg.norm(history_avg)

    # Weighted blend
    combined = (interest_weight * interest_vector) + ((1 - interest_weight) * history_avg)
    combined = combined / np.linalg.norm(combined)
    return combined