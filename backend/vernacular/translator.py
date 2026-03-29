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

Your task: Provide a context-aware, culturally adapted explanation of the following English business article in {LANGUAGE_NAME}.

RULES:
1. **NO LITERAL TRANSLATION:** Provide culturally adapted explanations. Do not just translate word-for-word.
2. **Local Context:** Embed local context to make the news relatable to a regional reader in {LANGUAGE_NAME}.
3. **Accuracy:** Maintain the accuracy of financial facts, figures, and business terms.
4. **Tone:** Keep the tone professional but highly accessible and conversational.
5. **Jargon:** Break down complex financial jargon using simple regional analogies.

IMPORTANT: Respond strictly in {LANGUAGE_NAME}.

Format your response exactly as follows:
- 📰 शीर्षक (Headline in {LANGUAGE_NAME})
- 🎯 मुख्य बिंदु (Key Points in {LANGUAGE_NAME} - bulleted)
- 💡 विस्तृत विवरण (Culturally Adapted Detailed Explanation in {LANGUAGE_NAME})"""

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
        model = genai.GenerativeModel("gemini-2.0-flash")
        
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
        print(f"Gemini API failed, falling back to deep-translator: {e}")
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source='auto', target=language_code)
            fallback_text = translator.translate(content[:2000])
            fallback_text = f"*(Note: AI Contextual Engine is currently sleeping due to API Rate Limits. Providing direct fallback translation.)*\n\n{fallback_text}"
            return {
                "original_title": title,
                "language": lang_info["name"],
                "language_code": language_code,
                "native_name": lang_info["native"],
                "translated_content": fallback_text,
                "character_count": len(fallback_text)
            }
        except Exception as fallback_e:
            raise RuntimeError(f"Translation error and fallback failed: {str(fallback_e)}")


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
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = TRANSLATION_PROMPT_TEMPLATE.replace("{LANGUAGE_NAME}", lang_info["name"])
        prompt += f"\n\nORIGINAL ARTICLE:\nTitle: {title}\nContent: {content[:2000]}"
        
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        print(f"Gemini streaming failed: {e}")
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source='auto', target=language_code)
            fallback_text = translator.translate(content[:2000])
            yield f"*(Note: AI Contextual Engine is currently sleeping due to API Rate Limits. Providing direct fallback translation.)*\n\n"
            
            # Simulated streaming by chunking the output
            words = fallback_text.split()
            for i in range(0, len(words), 5):
                yield " ".join(words[i:i+5]) + " "
        except Exception as fallback_e:
            yield f"ERROR: Fallback translation failed: {str(fallback_e)}"


def get_supported_languages() -> dict:
    """
    Get all supported languages with metadata.
    
    Returns:
        Dictionary of language info
    """
    return SUPPORTED_LANGUAGES
