# recommendation/embedder.py
import numpy as np
from sentence_transformers import SentenceTransformer
from data_pipeline.utils.db import get_db

MODEL_NAME = "all-MiniLM-L6-v2"   # 384 dims, fast, free, good quality
BATCH_SIZE = 64                     # Process 64 articles at a time

_model = None

def get_model() -> SentenceTransformer:
    """Singleton — model takes ~2s to load, reuse across calls."""
    global _model
    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def make_article_text(article: dict) -> str:
    """
    Combine title + description + content for embedding.
    Title is repeated 3x — gives it more semantic weight,
    which improves recommendation relevance significantly.
    """
    title = article.get("title", "")
    description = article.get("description", "")
    content = article.get("content", "")[:500]   # cap at 500 chars to stay within token limit
    return f"{title}. {title}. {title}. {description}. {content}"

def embed_pending_articles() -> int:
    """
    Find all articles with no embedding yet, batch-embed them,
    and write the vectors back to MongoDB.
    Returns number of articles embedded.
    """
    db = get_db()
    col = db["articles"]
    model = get_model()

    pending = list(col.find({"embedding": None}, {
        "_id": 1, "title": 1, "description": 1, "content": 1
    }))

    if not pending:
        print("No pending articles to embed.")
        return 0

    print(f"Embedding {len(pending)} articles in batches of {BATCH_SIZE}...")
    total = 0

    for i in range(0, len(pending), BATCH_SIZE):
        batch = pending[i : i + BATCH_SIZE]
        texts = [make_article_text(a) for a in batch]

        # normalize_embeddings=True gives unit vectors — required for cosine similarity
        vectors = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        # Bulk write back to MongoDB
        for article, vector in zip(batch, vectors):
            col.update_one(
                {"_id": article["_id"]},
                {"$set": {
                    "embedding": vector.tolist(),
                    "embedding_model": MODEL_NAME,
                }}
            )
        total += len(batch)
        print(f"  Embedded {total}/{len(pending)}")

    print(f"✓ Done. {total} articles embedded.")
    return total