# api/main.py — NewsET API with Phase 2 (Recommendations) & Phase 3 (RAG)
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from recommendation.embedder import embed_pending_articles
from recommendation.faiss_store import build_index
from recommendation.recommender import get_personalized_feed
from rag.llm_gemini import ask, stream_ask, check_gemini
from vernacular.orchestrator import translate_with_context, stream_translate_with_context, get_all_languages, check_vernacular_api
from vernacular.orchestrator import translate_with_context, stream_translate_with_context, get_all_languages, check_vernacular_api

# ── Update lifespan to include Phase 3 startup ────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up NewsET API...")

    # Phase 2 startup (unchanged)
    embed_pending_articles()
    build_index()
    print("  ✓ Phase 2: Article embeddings & FAISS ready")

    # Phase 3 startup (Gemini)
    if not check_gemini():
        print("  ⚠ WARNING: Gemini API key missing or invalid. Check .env GEMINI_API_KEY")
    else:
        print("  ✓ Phase 3: Gemini 1.5 Flash ready")

    # Phase 5 startup (Vernacular)
    if not check_vernacular_api():
        print("  ⚠ WARNING: Vernacular API not available. Check Gemini API key.")
    else:
        print("  ✓ Phase 5: Vernacular News Engine ready")

    print("✓ API ready on http://localhost:8000")
    yield
    print("Shutting down...")

app = FastAPI(title="NewsET API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────────────────────
# PHASE 2: RECOMMENDATION ENGINE
# ──────────────────────────────────────────────────────────────────────────

class FeedRequest(BaseModel):
    interests: list[str]
    read_article_ids: list[str] = []
    top_k: int = 20

class ArticleOut(BaseModel):
    id: str
    title: str
    description: str | None
    source: str | None
    published_at: str | None
    category: str | None
    url: str | None
    relevance_score: float

@app.post("/feed", response_model=list[ArticleOut], tags=["Phase 2: Recommendations"])
def get_feed(req: FeedRequest):
    """
    Returns a personalized ranked news feed for the given user profile.
    """
    articles = get_personalized_feed(
        interests=req.interests,
        read_article_ids=req.read_article_ids,
        top_k=req.top_k,
    )
    return [
        ArticleOut(
            id=a["_id"],
            title=a.get("title", ""),
            description=a.get("description"),
            source=a.get("source"),
            published_at=a.get("published_at"),
            category=a.get("category"),
            url=a.get("url"),
            relevance_score=a["relevance_score"],
        )
        for a in articles
    ]

@app.get("/interests", tags=["Phase 2: Recommendations"])
def list_interests():
    """Returns all valid interest categories."""
    from recommendation.user_profile import INTEREST_SEEDS
    return list(INTEREST_SEEDS.keys())

# ──────────────────────────────────────────────────────────────────────────
# PHASE 3: AI NEWS NAVIGATOR (RAG)
# ──────────────────────────────────────────────────────────────────────────

class BriefingRequest(BaseModel):
    question: str
    stream: bool = True
    category_filter: str | None = None  # optional: stocks|startup|macro|corporate|crypto|real_estate

class FollowUpRequest(BaseModel):
    question: str
    history: list[dict]
    stream: bool = True

class BriefingResponse(BaseModel):
    answer: str
    sources: list[dict] | None = None

@app.post("/briefing", tags=["Phase 3: RAG"])
def get_briefing(req: BriefingRequest):
    """
    AI briefing powered by Gemini 1.5 Flash.
    Sends up to 100 recent articles as context — no chunking needed.
    
    With stream=true (default): returns streaming response
    With stream=false: returns full JSON response
    """
    if not check_gemini():
        raise HTTPException(503, detail="Gemini API key not configured. Add GEMINI_API_KEY to .env")
    
    category = req.category_filter if hasattr(req, 'category_filter') and req.category_filter else None
    
    if req.stream:
        return StreamingResponse(
            stream_ask(req.question, category_filter=category),
            media_type="text/plain"
        )
    
    result = ask(req.question, category_filter=category)
    return result

@app.post("/ask", tags=["Phase 3: RAG"])
def ask_followup(req: FollowUpRequest):
    """
    Follow-up questions. For Gemini, history is prepended as context in the prompt.
    """
    if not check_gemini():
        raise HTTPException(503, detail="Gemini API key not configured.")
    
    # Prepend conversation history to question for context
    history_text = ""
    if req.history:
        history_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in req.history[-4:]  # last 4 turns only
        ])
        question_with_history = f"Previous conversation:\n{history_text}\n\nNew question: {req.question}"
    else:
        question_with_history = req.question
    
    if req.stream:
        return StreamingResponse(
            stream_ask(question_with_history),
            media_type="text/plain"
        )
    
    result = ask(question_with_history)
    return result

# ──────────────────────────────────────────────────────────────────────────
# HEALTH CHECK
# ──────────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────────
# PHASE 5: VERNACULAR NEWS ENGINE
# ──────────────────────────────────────────────────────────────────────────

class TranslationRequest(BaseModel):
    article_id: str = None  # Optional: for tracking
    title: str
    content: str
    language_code: str  # hi|ta|te|bn|mr|gu
    simplify: bool = True
    stream: bool = False

class LanguageInfo(BaseModel):
    name: str
    native: str
    code: str
    speakers: str
    flag: str

@app.get("/languages", tags=["Phase 5: Vernacular"])
def list_languages():
    """
    Returns all supported regional languages for translation.
    Includes Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati.
    """
    if not check_vernacular_api():
        raise HTTPException(503, detail="Vernacular API not available")
    return get_all_languages()

@app.post("/translate", tags=["Phase 5: Vernacular"])
def translate(req: TranslationRequest):
    """
    Translate an article to a regional language with simplification and context.
    Supports: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati
    
    Returns simplified + translated + contextual explanation.
    """
    if not check_vernacular_api():
        raise HTTPException(503, detail="Vernacular API not configured")
    
    try:
        if req.stream:
            return StreamingResponse(
                stream_translate_with_context(
                    title=req.title,
                    content=req.content,
                    language_code=req.language_code,
                    include_simplification=req.simplify
                ),
                media_type="text/plain"
            )
        
        result = translate_with_context(
            title=req.title,
            content=req.content,
            language_code=req.language_code,
            include_simplification=req.simplify
        )
        return result
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Translation error: {str(e)}")

# ──────────────────────────────────────────────────────────────────────────
# HEALTH CHECK
# ──────────────────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
def health():
    """
    Health check endpoint. Returns status and API availability.
    """
    from recommendation.faiss_store import _index
    return {
        "status": "ok",
        "faiss_articles": _index.ntotal if _index else 0,
        "gemini": check_gemini(),
        "vernacular": check_vernacular_api(),
        "model": "gemini-1.5-flash"
    }
