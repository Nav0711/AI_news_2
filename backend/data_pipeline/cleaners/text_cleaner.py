# data-pipeline/cleaners/text_cleaner.py
import re
from bs4 import BeautifulSoup

def clean_html(raw_html: str) -> str:
    """Strip all HTML tags and return plain text."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces, newlines, and tabs into single spaces."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def remove_boilerplate(text: str) -> str:
    """
    Remove common news article noise phrases that appear across many sources.
    These patterns add noise to embeddings and summaries.
    """
    noise_patterns = [
        r'\(Reuters\)',
        r'\(AP\)',
        r'Subscribe to read more',
        r'Read more at.*',
        r'Click here to.*',
        r'Follow us on.*',
        r'Sign up for.*newsletter',
        r'\[\+\d+ chars\]',        # NewsAPI truncation artifact
    ]
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return text.strip()

def clean_article_text(raw: str) -> str:
    """
    Full cleaning pipeline for a single article body.
    Order matters: HTML → boilerplate → whitespace.
    """
    text = clean_html(raw)
    text = remove_boilerplate(text)
    text = normalize_whitespace(text)
    return text

def is_too_short(text: str, min_words: int = 50) -> bool:
    """
    Reject articles with fewer than min_words — these are usually stubs,
    paywalled content, or API truncation artifacts.
    """
    return len(text.split()) < min_words