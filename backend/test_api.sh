#!/bin/bash
# Phase 2 Comprehensive Test Suite
# Tests all API endpoints and interest profiles

echo "================================"
echo "PHASE 2 API TEST SUITE"
echo "================================"

API="http://localhost:8000"

echo -e "\n📊 TEST 1: /health endpoint"
echo "Command: curl $API/health"
curl -s "$API/health" | python3 -m json.tool

echo -e "\n\n📋 TEST 2: /interests endpoint"
echo "Command: curl $API/interests"
curl -s "$API/interests" | python3 -m json.tool

echo -e "\n\n🔍 TEST 3: /feed with 'stocks' interest"
echo "Command: curl -X POST $API/feed -H 'Content-Type: application/json' -d '{\"interests\": [\"stocks\"], \"top_k\": 3}'"
curl -s -X POST "$API/feed" \
  -H "Content-Type: application/json" \
  -d '{"interests": ["stocks"], "read_article_ids": [], "top_k": 3}' | python3 -m json.tool

echo -e "\n\n🚀 TEST 4: /feed with 'startup' interest"
echo "Command: curl -X POST $API/feed -H 'Content-Type: application/json' -d '{\"interests\": [\"startup\"], \"top_k\": 3}'"
curl -s -X POST "$API/feed" \
  -H "Content-Type: application/json" \
  -d '{"interests": ["startup"], "read_article_ids": [], "top_k": 3}' | python3 -m json.tool

echo -e "\n\n📈 TEST 5: /feed with 'macro' interest"
echo "Command: curl -X POST $API/feed -H 'Content-Type: application/json' -d '{\"interests\": [\"macro\"], \"top_k\": 3}'"
curl -s -X POST "$API/feed" \
  -H "Content-Type: application/json" \
  -d '{"interests": ["macro"], "read_article_ids": [], "top_k": 3}' | python3 -m json.tool

echo -e "\n\n💼 TEST 6: /feed with combined interests (stocks + macro)"
echo "Command: curl -X POST $API/feed -H 'Content-Type: application/json' -d '{\"interests\": [\"stocks\", \"macro\"], \"top_k\": 3}'"
curl -s -X POST "$API/feed" \
  -H "Content-Type: application/json" \
  -d '{"interests": ["stocks", "macro"], "read_article_ids": [], "top_k": 3}' | python3 -m json.tool

echo -e "\n\n================================"
echo "✅ ALL TESTS COMPLETE"
echo "================================"
