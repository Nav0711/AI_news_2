# Phase 5: Vernacular News Engine - Article Simplification

import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SIMPLIFICATION_PROMPT = """You are a business news simplifier. Your task is to simplify complex business and financial news articles for general readers.

Guidelines:
1. Break down technical terms with simple explanations
2. Use everyday examples to explain concepts
3. Keep sentences short and clear
4. Highlight "Why it matters?" for readers
5. Remove jargon and industry-specific language
6. Add context and background where helpful
7. Use bullet points for key takeaways

Format your response with:
- Simplified Headline
- Easy-to-understand Summary (3-4 sentences)
- Key Terms Explained (definitions)
- Why It Matters
- What's Next"""

def simplify_article(title: str, content: str) -> dict:
    """
    Simplify a complex article for general audience.
    
    Args:
        title: Article headline
        content: Article content (up to 2000 chars)
    
    Returns:
        Dictionary with simplified version
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = f"""{SIMPLIFICATION_PROMPT}

ARTICLE:
Title: {title}
Content: {content[:2000]}

Please simplify this article for a general audience."""
        
        response = model.generate_content(prompt)
        
        return {
            "original_title": title,
            "simplified": response.text,
            "language": "english",
            "complexity_reduced": True
        }
    except Exception as e:
        raise RuntimeError(f"Simplification error: {str(e)}")


def stream_simplify_article(title: str, content: str):
    """
    Stream simplified article content.
    
    Args:
        title: Article headline
        content: Article content
    
    Yields:
        String chunks of simplified content
    """
    if not GEMINI_API_KEY:
        yield "ERROR: GEMINI_API_KEY not set"
        return
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = f"""{SIMPLIFICATION_PROMPT}

ARTICLE:
Title: {title}
Content: {content[:2000]}

Please simplify this article for a general audience."""
        
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"ERROR: {str(e)}"
