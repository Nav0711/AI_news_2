# Phase 3: AI News Navigator — Google Gemini 1.5 Flash Integration

import os
from typing import Generator
import google.generativeai as genai
from dotenv import load_dotenv
from data_pipeline.utils.db import get_db

# Load environment variables
load_dotenv()

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are MyET, an AI business news analyst specializing in Indian markets.
You have been given a set of recent news articles as context.
Answer the user's question using ONLY information from these articles.
Be structured, concise, and always mention the source name when citing facts.
Format your response with:
- Key Highlights (3-5 bullet points)
- Market/Business Impact
- What to Watch Next
If the articles don't contain enough information, say so clearly. Never hallucinate."""

# ─────────────────────────────────────────────────────────────────────────
# 1. fetch_articles_for_context(limit=100) -> str
# ─────────────────────────────────────────────────────────────────────────

def fetch_articles_for_context(limit: int = 5, category_filter: str = None) -> tuple[str, int]:
    """
    Fetch recent articles from MongoDB and format as context string for Gemini.
    
    Args:
        limit: Maximum number of articles to fetch
        category_filter: Optional category to filter (stocks|startup|macro|corporate|crypto|real_estate)
    
    Returns:
        Tuple of (formatted_context_string, article_count)
    """
    db = get_db()
    articles_coll = db["articles"]
    
    # Build query
    query = {}
    if category_filter:
        query["category"] = category_filter
    
    # Fetch articles sorted by published_at descending
    articles = list(
        articles_coll.find(query)
        .sort("published_at", -1)
        .limit(limit)
    )
    
    # Format articles as context
    context_lines = []
    for article in articles:
        title = article.get("title", "No title")
        source = article.get("source", "Unknown source")
        published_at = article.get("published_at", "No date")[:10]  # YYYY-MM-DD
        category = article.get("category", "uncategorized")
        content = article.get("content", "")[:800]  # Limit to 800 chars
        
        formatted = f"[{source} | {published_at} | {category}]\nHEADLINE: {title}\nCONTENT: {content}"
        context_lines.append(formatted)
    
    context_str = "\n---\n".join(context_lines)
    return context_str, len(articles)


# ─────────────────────────────────────────────────────────────────────────
# 2. ask(question: str, category_filter: str = None) -> dict
# ─────────────────────────────────────────────────────────────────────────

def ask(question: str, category_filter: str = None) -> dict:
    """
    Ask a question using Gemini with recent articles as context.
    Non-streaming mode.
    
    Args:
        question: User question
        category_filter: Optional category filter
    
    Returns:
        Dictionary with question, answer, articles_used, and model name
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set. Add to .env file.")
    
    # 1. Check Cache first
    db = get_db()
    cache_coll = db["ai_briefing_cache"]
    # Simple cache key: question + category
    cache_key = f"{question}_{category_filter or 'all'}"
    cached = cache_coll.find_one({"key": cache_key})
    if cached:
        return {
            "question": question,
            "answer": cached["answer"],
            "articles_used": cached.get("articles_used", 0),
            "model": "cached"
        }

    # Fetch articles - limited to 5 for prototype efficiency
    context, article_count = fetch_articles_for_context(limit=5, category_filter=category_filter)
    
    if not context:
        return {
            "question": question,
            "answer": "No articles available for this query.",
            "articles_used": 0,
            "model": "gemini-2.0-flash"
        }
    
    # Build prompt
    prompt = f"""{SYSTEM_PROMPT}

ARTICLES CONTEXT:
{context}

USER QUESTION: {question}

Please provide a comprehensive answer based on the articles above."""
    
    try:
        # Call Gemini with token limits
        generation_config = {
            "max_output_tokens": 512,
            "temperature": 0.7,
        }
        model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config)
        response = model.generate_content(prompt)
        
        # Save to cache
        cache_coll.update_one(
            {"key": cache_key},
            {"$set": {
                "key": cache_key,
                "answer": response.text,
                "articles_used": article_count,
                "timestamp": time.time()
            }},
            upsert=True
        )
        
        return {
            "question": question,
            "answer": response.text,
            "articles_used": article_count,
            "model": "gemini-2.0-flash"
        }
    except Exception as e:
        # Ptototype Mock Fallback if Quota hit
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            return {
                "question": question,
                "answer": f"Prototype Note: Gemini Quota Exceeded. \n\nBriefing Summary (Mock):\nThis article discusses key shifts in the Indian business landscape. The key highlights include increased domestic capital flow and strategic expansions by major players. Expected market impact: Positive long-term sentiment.",
                "articles_used": article_count,
                "model": "mock-fallback"
            }
        raise RuntimeError(f"Gemini API error: {str(e)}")


# ─────────────────────────────────────────────────────────────────────────
# 3. stream_ask(question: str, category_filter: str = None) -> Generator
# ─────────────────────────────────────────────────────────────────────────

def stream_ask(question: str, category_filter: str = None) -> Generator[str, None, None]:
    """
    Ask a question using Gemini with streaming response.
    Yields tokens as they are generated.
    
    Args:
        question: User question
        category_filter: Optional category filter
    
    Yields:
        String chunks of the response
    """
    if not GEMINI_API_KEY:
        yield "ERROR: GEMINI_API_KEY not set. Add to .env file."
        return
    
    # Check Cache first (Streaming mode doesn't cache as easily, but we'll check if a full answer exists)
    db = get_db()
    cache_coll = db["ai_briefing_cache"]
    cache_key = f"{question}_{category_filter or 'all'}"
    cached = cache_coll.find_one({"key": cache_key})
    if cached:
        yield cached["answer"]
        return

    # Fetch articles - limited to 5 for prototype efficiency
    context, article_count = fetch_articles_for_context(limit=5, category_filter=category_filter)
    
    if not context:
        yield "No articles available for this query."
        return
    
    # Build prompt
    prompt = f"""{SYSTEM_PROMPT}

ARTICLES CONTEXT:
{context}

USER QUESTION: {question}

Please provide a comprehensive answer based on the articles above."""
    
    try:
        # Call Gemini with streaming and limits
        generation_config = {
            "max_output_tokens": 512,
            "temperature": 0.7,
        }
        model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config)
        response = model.generate_content(prompt, stream=True)
        
        full_text = ""
        for chunk in response:
            if chunk.text:
                full_text += chunk.text
                yield chunk.text
        
        # Cache the full response afterward
        if full_text:
            cache_coll.update_one(
                {"key": cache_key},
                {"$set": {
                    "key": cache_key,
                    "answer": full_text,
                    "articles_used": article_count,
                    "timestamp": time.time()
                }},
                upsert=True
            )
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            yield "Prototype Note: Gemini Quota Exceeded. Returning Mock Briefing...\n\n"
            yield f"Summary for: {question}\n\n"
            yield "- Key Highlights: Domestic venture capital is scaling up rapidly.\n"
            yield "- Market Impact: Neutral to Positive as local funds replace global exits.\n"
            yield "- Watch next: Further regulatory updates from SEBI and RBI."
            return
        yield f"ERROR: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────
# 4. check_gemini() -> bool
# ─────────────────────────────────────────────────────────────────────────

import time
from typing import Dict, Any

_gemini_health_cache: Dict[str, Any] = {
    "status": False,
    "last_checked": 0.0
}

def check_gemini() -> bool:
    """
    Check if Gemini API is available and working.
    Caches the result for 60 seconds to prevent rate limiting.
    
    Returns:
        True if API key is valid, False otherwise
    """
    if not GEMINI_API_KEY:
        return False
        
    current_time = time.time()
    
    # Return cached value if within 60 seconds
    if current_time - _gemini_health_cache["last_checked"] < 60:
        return _gemini_health_cache["status"]
    
    try:
        # Try a minimal API call
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content("Say 'ok'")
        is_healthy = response is not None and response.text is not None
        
        _gemini_health_cache["status"] = is_healthy
        _gemini_health_cache["last_checked"] = current_time
        
        return is_healthy
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            pass # Suppress rate limit giant blocks since fallback is configured
        else:
            print(f"Gemini check issue: {error_msg.splitlines()[0]}")
            
        _gemini_health_cache["status"] = False
        _gemini_health_cache["last_checked"] = current_time
        return False
