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

SYSTEM_PROMPT = """You are NewsET, an AI business news analyst specializing in Indian markets.
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

def fetch_articles_for_context(limit: int = 100, category_filter: str = None) -> tuple[str, int]:
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
    
    # Fetch articles
    context, article_count = fetch_articles_for_context(limit=100, category_filter=category_filter)
    
    if not context:
        return {
            "question": question,
            "answer": "No articles available for this query.",
            "articles_used": 0,
            "model": "gemini-1.5-flash"
        }
    
    # Build prompt
    prompt = f"""{SYSTEM_PROMPT}

ARTICLES CONTEXT:
{context}

USER QUESTION: {question}

Please provide a comprehensive answer based on the articles above."""
    
    try:
        # Call Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        return {
            "question": question,
            "answer": response.text,
            "articles_used": article_count,
            "model": "gemini-1.5-flash"
        }
    except Exception as e:
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
    
    # Fetch articles
    context, article_count = fetch_articles_for_context(limit=100, category_filter=category_filter)
    
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
        # Call Gemini with streaming
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"ERROR: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────
# 4. check_gemini() -> bool
# ─────────────────────────────────────────────────────────────────────────

def check_gemini() -> bool:
    """
    Check if Gemini API is available and working.
    
    Returns:
        True if API key is valid, False otherwise
    """
    if not GEMINI_API_KEY:
        return False
    
    try:
        # Try a minimal API call
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say 'ok'", timeout=5)
        return response is not None and response.text
    except Exception as e:
        print(f"Gemini health check failed: {e}")
        return False
