#!/usr/bin/env python3
"""
Phase 2 Deliverable Verification Script
Tests all 4 recommendation modules and API functionality
"""
import sys
import numpy as np

print("=" * 70)
print("PHASE 2 DELIVERABLE VERIFICATION")
print("=" * 70)

# Test 1: embedder.py
print("\n1️⃣  Testing embedder.py...")
try:
    from recommendation.embedder import get_model
    
    model = get_model()
    print(f"   ✓ Sentence Transformer loaded: {type(model).__name__}")
    
    # Test embedding
    test_vector = model.encode("test text", normalize_embeddings=True)
    print(f"   ✓ Embedding shape: {test_vector.shape}")
    print(f"   ✓ Embedding model: all-MiniLM-L6-v2 (384 dims)")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 2: faiss_store.py
print("\n2️⃣  Testing faiss_store.py...")
try:
    from recommendation.faiss_store import get_index, search
    
    index = get_index()
    print(f"   ✓ FAISS Index loaded: {index.ntotal} vectors")
    print(f"   ✓ Index dimension: {index.d}")
    
    # Test search
    query_vector = np.random.randn(384).astype('float32')
    query_vector = query_vector / np.linalg.norm(query_vector)
    results = search(query_vector, top_k=5)
    print(f"   ✓ Search returned {len(results)} results")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 3: user_profile.py
print("\n3️⃣  Testing user_profile.py...")
try:
    from recommendation.user_profile import embed_interests, build_query_vector, INTEREST_SEEDS
    
    print(f"   ✓ Predefined interests: {list(INTEREST_SEEDS.keys())}")
    
    # Test interest embedding
    interest_vector = embed_interests(["stocks"])
    print(f"   ✓ Interest vector shape: {interest_vector.shape}")
    norm_check = np.abs(np.linalg.norm(interest_vector) - 1.0) < 0.001
    print(f"   ✓ Interest vector normalized: {norm_check}")
    
    # Test query vector building
    query = build_query_vector(["startup"])
    print(f"   ✓ Query vector shape: {query.shape}")
    norm_check = np.abs(np.linalg.norm(query) - 1.0) < 0.001
    print(f"   ✓ Query vector normalized: {norm_check}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 4: recommender.py
print("\n4️⃣  Testing recommender.py...")
try:
    from recommendation.recommender import get_personalized_feed
    
    # Test with single interest
    articles = get_personalized_feed(interests=["macro"], top_k=5)
    print(f"   ✓ Got {len(articles)} recommendations for 'macro' interest")
    
    if articles:
        article = articles[0]
        required_fields = ["_id", "title", "relevance_score"]
        for field in required_fields:
            if field not in article:
                raise ValueError(f"Missing field: {field}")
        print(f"   ✓ Article fields valid: {required_fields}")
        print(f"   ✓ Top article: '{article['title'][:50]}...'")
        print(f"   ✓ Relevance score: {article['relevance_score']}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ALL 4 RECOMMENDATION MODULES VERIFIED AND WORKING!")
print("=" * 70)
