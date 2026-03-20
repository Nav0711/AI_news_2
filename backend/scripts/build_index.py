# scripts/build_index.py
from data_pipeline.utils.db import ping, setup_indexes
from recommendation.embedder import embed_pending_articles
from recommendation.faiss_store import build_index

if __name__ == "__main__":
    if not ping():
        exit(1)
    setup_indexes()
    embed_pending_articles()
    index = build_index()
    print(f"\n✓ Index ready: {index.ntotal} vectors")