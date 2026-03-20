# Phase 5: Vernacular News Engine - Multi-Language Translation

import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SUPPORTED_LANGUAGES = {
    "hi": {
        "name": "Hindi",
        "native": "हिंदी",
        "code": "hi",
        "speakers": "345M+",
        "flag": "🇮🇳"
    },
    "ta": {
        "name": "Tamil",
        "native": "தமிழ்",
        "code": "ta",
        "speakers": "75M+",
        "flag": "🇮🇳"
    },
    "te": {
        "name": "Telugu",
        "native": "తెలుగు",
        "code": "te",
        "speakers": "75M+",
        "flag": "🇮🇳"
    },
    "bn": {
        "name": "Bengali",
        "native": "বাংলা",
        "code": "bn",
        "speakers": "230M+",
        "flag": "🇮🇳"
    },
    "mr": {
        "name": "Marathi",
        "native": "मराठी",
        "code": "mr",
        "speakers": "83M+",
        "flag": "🇮🇳"
    },
    "gu": {
        "name": "Gujarati",
        "native": "ગુજરાતી",
        "code": "gu",
        "speakers": "50M+",
        "flag": "🇮🇳"
    }
}

TRANSLATION_PROMPT_TEMPLATE = """You are a professional translator specializing in Indian regional languages and business news.

Your task: Translate the following business article to {LANGUAGE_NAME} with these rules:

1. Maintain accuracy of financial/business terms
2. Use regional context where relevant
3. Explain Indian market references clearly
4. Keep the tone professional but accessible
5. Add explanatory notes for complex terms
6. Preserve the original meaning

IMPORTANT: Respond in {LANGUAGE_NAME} only. Do not mix with English unless necessary for clarification.

Format your response with:
- शीर्षक / തലക്കം / ခေါင်းစီး (Headline in {LANGUAGE_NAME})
- मुख्य बिंदु / പ്രധാന പ്പോയിന്റുകൾ (Key Points - bulleted)
- വിപ്ലവകരമായ വിവരണം (Detailed Explanation)"""

def translate_article(content: str, language_code: str, title: str = "Business News") -> dict:
    """
    Translate article to regional language.
    
    Args:
        content: Article text to translate
        language_code: Language code (hi, ta, te, bn, mr, gu)
        title: Article title
    
    Returns:
        Dictionary with translated content
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")
    
    if language_code not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language_code}. Supported: {list(SUPPORTED_LANGUAGES.keys())}")
    
    lang_info = SUPPORTED_LANGUAGES[language_code]
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = TRANSLATION_PROMPT_TEMPLATE.replace("{LANGUAGE_NAME}", lang_info["name"])
        prompt += f"\n\nORIGINAL ARTICLE:\nTitle: {title}\nContent: {content[:2000]}"
        
        response = model.generate_content(prompt)
        
        return {
            "original_title": title,
            "language": lang_info["name"],
            "language_code": language_code,
            "native_name": lang_info["native"],
            "translated_content": response.text,
            "character_count": len(response.text)
        }
    except Exception as e:
        raise RuntimeError(f"Translation error: {str(e)}")


def stream_translate_article(content: str, language_code: str, title: str = "Business News"):
    """
    Stream translated article.
    
    Args:
        content: Article text
        language_code: Language code
        title: Article title
    
    Yields:
        String chunks of translated content
    """
    if not GEMINI_API_KEY:
        yield "ERROR: GEMINI_API_KEY not set"
        return
    
    if language_code not in SUPPORTED_LANGUAGES:
        yield f"ERROR: Unsupported language: {language_code}"
        return
    
    lang_info = SUPPORTED_LANGUAGES[language_code]
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = TRANSLATION_PROMPT_TEMPLATE.replace("{LANGUAGE_NAME}", lang_info["name"])
        prompt += f"\n\nORIGINAL ARTICLE:\nTitle: {title}\nContent: {content[:2000]}"
        
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"ERROR: {str(e)}"


def get_supported_languages() -> dict:
    """
    Get all supported languages with metadata.
    
    Returns:
        Dictionary of language info
    """
    return SUPPORTED_LANGUAGES
