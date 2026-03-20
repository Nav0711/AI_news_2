# Phase 5: Vernacular News Engine - Main Orchestrator

import os
from typing import Optional, Generator
import google.generativeai as genai
from dotenv import load_dotenv
from vernacular.simplifier import simplify_article, stream_simplify_article
from vernacular.translator import translate_article, stream_translate_article, get_supported_languages

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

CONTEXT_PROMPT = """As an Indian business news expert, provide contextual explanations for this news in {LANGUAGE_NAME}.

Context to provide:
1. Indian market impact
2. Regulatory/policy implications
3. Historical background if relevant
4. Similar past events
5. Expert perspective

Keep explanations accessible to regional readers."""

def translate_with_context(
    title: str,
    content: str,
    language_code: str,
    include_simplification: bool = True
) -> dict:
    """
    Complete translation pipeline: simplify → translate → add context.
    
    Args:
        title: Article title
        content: Article content
        language_code: Target language
        include_simplification: Whether to simplify first
    
    Returns:
        Complete translated article with context
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")
    
    # Step 1: Simplify (optional)
    simplified_content = content
    if include_simplification:
        try:
            simplified = simplify_article(title, content)
            simplified_content = simplified.get("simplified", content)
        except Exception as e:
            print(f"Simplification skipped: {e}")
    
    # Step 2: Translate
    translation = translate_article(simplified_content, language_code, title)
    
    # Step 3: Add context explanation
    context = _add_context(title, content, language_code)
    
    return {
        "original": {
            "title": title,
            "preview": content[:200]
        },
        "simplified": simplified_content if include_simplification else None,
        "language": translation["language"],
        "language_code": language_code,
        "native_name": translation["native_name"],
        "translated_headline": translation["translated_content"].split("\n")[0],  # First line as headline
        "translated_content": translation["translated_content"],
        "contextual_explanation": context,
        "translation_complete": True
    }


def stream_translate_with_context(
    title: str,
    content: str,
    language_code: str,
    include_simplification: bool = True
) -> Generator[str, None, None]:
    """
    Stream complete translation pipeline.
    
    Args:
        title: Article title
        content: Article content
        language_code: Target language
        include_simplification: Whether to simplify first
    
    Yields:
        String chunks of the complete translation
    """
    if not GEMINI_API_KEY:
        yield "ERROR: GEMINI_API_KEY not set"
        return
    
    try:
        # Simplified content
        if include_simplification:
            yield "📝 Simplifying article...\n---\n"
            for chunk in stream_simplify_article(title, content):
                yield chunk
            yield "\n\n---\n🌐 Translating to regional language...\n---\n"
        
        # Translation
        for chunk in stream_translate_article(content, language_code, title):
            yield chunk
        
        yield "\n\n---\n🎯 Adding contextual explanation...\n---\n"
        
        # Context
        context = _add_context(title, content, language_code)
        yield context
        
    except Exception as e:
        yield f"ERROR: {str(e)}"


def _add_context(title: str, content: str, language_code: str) -> str:
    """
    Add contextual explanation for regional readers.
    
    Args:
        title: Article title
        content: Article content
        language_code: Language code
    
    Returns:
        Contextual explanation in target language
    """
    try:
        from vernacular.translator import SUPPORTED_LANGUAGES
        lang_info = SUPPORTED_LANGUAGES.get(language_code, {})
        lang_name = lang_info.get("name", "English")
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = CONTEXT_PROMPT.replace("{LANGUAGE_NAME}", lang_name)
        prompt += f"\n\nARTICLE:\nTitle: {title}\nContent: {content[:1500]}"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Context unavailable: {str(e)}"


def get_all_languages() -> list:
    """
    Get list of all supported languages.
    
    Returns:
        List of language metadata
    """
    return list(get_supported_languages().values())


def check_vernacular_api() -> bool:
    """
    Check if Gemini API is available for Phase 5.
    
    Returns:
        True if API working, False otherwise
    """
    if not GEMINI_API_KEY:
        return False
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say 'ok' in one word only", timeout=5)
        return response is not None and response.text
    except Exception:
        return False
