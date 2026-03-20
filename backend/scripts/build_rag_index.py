# scripts/build_rag_index.py
from data_pipeline.utils.db import ping
from rag.chunker import chunk_all_articles
from rag.chunk_store import embed_pending_chunks, build_chunk_index
from rag.llm import check_ollama

if __name__ == "__main__":
    if not ping():
        exit(1)

    print("=== Phase 3 RAG Index Build ===\n")
    chunk_all_articles()
    embed_pending_chunks()
    index = build_chunk_index()

    print(f"\n✓ RAG index ready: {index.ntotal} chunk vectors")

    if not check_ollama():
        print("\n⚠ Ollama not running — start it before using /briefing")
        print("  Terminal 1: ollama serve")
        print("  Terminal 2: ollama pull llama3  (if not already done)")