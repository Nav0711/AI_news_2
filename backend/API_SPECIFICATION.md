# NewsET API Specification — Phase 3 Gemini Edition

**API Version:** 2.0 (Gemini 1.5 Flash)  
**Last Updated:** March 20, 2026  
**Base URL:** http://localhost:8000  
**Documentation (Interactive):** http://localhost:8000/docs

---

## Authentication

No authentication required for free tier.

For free tier rate limits, see: https://ai.google.dev/pricing

---

## API Endpoints

### ═══════════════════════════════════════════════════════════════════════════════
### PHASE 2: RECOMMENDATION ENGINE (Unchanged)
### ═══════════════════════════════════════════════════════════════════════════════

## 1. GET `/interests` — List Interest Categories

Returns all valid interest categories for user profiling.

**URL:** `GET http://localhost:8000/interests`

**Request:** None (query parameters not used)

**Response:**
```json
[
  "stocks",
  "startup",
  "macro",
  "corporate",
  "crypto",
  "real_estate"
]
```

**Status Code:** 200 OK

**Example:**
```bash
curl http://localhost:8000/interests
```

---

## 2. POST `/feed` — Get Personalized News Feed

Returns ranked articles based on user interests and reading history.

**URL:** `POST http://localhost:8000/feed`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "interests": ["stocks", "startup"],
  "read_article_ids": ["64f8a3c9..."],
  "top_k": 20
}
```

**Parameters:**
- `interests` (array[str], required): List of interest categories
- `read_article_ids` (array[str], optional): Article IDs user has already read
- `top_k` (int, optional, default=20): Number of articles to return

**Response:**
```json
[
  {
    "id": "64f8a3c9b12e4c0012345678",
    "title": "RBI Raises Interest Rates by 50bps",
    "description": "The Reserve Bank of India announced...",
    "source": "Reuters",
    "published_at": "2026-03-20T08:30:00Z",
    "category": "stocks",
    "url": "https://reuters.com/...",
    "relevance_score": 0.8234
  },
  ...
]
```

**Status Code:** 200 OK

**Example:**
```bash
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["stocks", "startup"],
    "read_article_ids": [],
    "top_k": 5
  }'
```

---

### ═══════════════════════════════════════════════════════════════════════════════
### PHASE 3: AI NEWS NAVIGATOR (NEW — Gemini Powered)
### ═══════════════════════════════════════════════════════════════════════════════

## 3. POST `/briefing` — Get AI-Generated News Briefing

Returns an AI-generated briefing answering the user's question using recent articles as context.

**URL:** `POST http://localhost:8000/briefing`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "What is the impact of RBI decisions on the stock market?",
  "stream": false,
  "category_filter": "stocks"
}
```

**Parameters:**
- `question` (string, required): User's question about news
- `stream` (boolean, optional, default=true): Whether to stream response
- `category_filter` (string, optional): Filter articles by category (stocks|startup|macro|corporate|crypto|real_estate)

**Response (stream=false):**
```json
{
  "question": "What is the impact of RBI decisions on the stock market?",
  "answer": "Based on recent articles:\n\n**Key Highlights:**\n- RBI raised repo rate by 50 basis points...\n\n**Market/Business Impact:**\n- PSU banks gained 2-3% in afternoon trading...\n\n**What to Watch Next:**\n- Q4 FY26 earnings season...",
  "articles_used": 42,
  "model": "gemini-1.5-flash"
}
```

**Response (stream=true):**
```
HTTP/1.1 200 OK
Content-Type: text/plain
Transfer-Encoding: chunked

Based on recent
 articles:

**Key Highlights:**
- RBI raised repo
 rate by 50 basis
...
```

**Status Codes:**
- `200 OK` — Success
- `503 Service Unavailable` — Gemini API key not configured

**Examples:**

Non-streaming briefing:
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the latest startup funding news?",
    "stream": false
  }' | python3 -m json.tool
```

Streaming briefing:
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Macro economic updates",
    "stream": true
  }'
```

Category-filtered briefing:
```bash
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are SEBI updates?",
    "stream": false,
    "category_filter": "stocks"
  }' | python3 -m json.tool
```

---

## 4. POST `/ask` — Follow-up Questions

Continues a conversation by answering follow-up questions with context from previous responses.

**URL:** `POST http://localhost:8000/ask`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "Which sectors were most affected?",
  "history": [
    {
      "role": "user",
      "content": "What is the impact of RBI decisions?"
    },
    {
      "role": "assistant",
      "content": "Based on recent articles, RBI decisions have impacted..."
    }
  ],
  "stream": false
}
```

**Parameters:**
- `question` (string, required): User's follow-up question
- `history` (array[object], optional): Previous conversation turns
  - Each turn has `role` ("user" or "assistant") and `content` (string)
- `stream` (boolean, optional, default=true): Whether to stream response

**Response (stream=false):**
```json
{
  "question": "Which sectors were most affected?",
  "answer": "Based on the earlier discussion and recent articles:\n\n**Affected Sectors:**\n- Banking sector: PSU banks up 2-3%, private banks mixed...\n\n**Market/Business Impact:**\n- Insurance stocks rallied as yields rose...\n\n**What to Watch Next:**\n- Credit growth trends in Q4...",
  "articles_used": 38,
  "model": "gemini-1.5-flash"
}
```

**Response (stream=true):** Text stream (same as /briefing streaming)

**Status Codes:**
- `200 OK` — Success
- `503 Service Unavailable` — Gemini API key not configured

**Note:** Only the last 4 conversation turns are used to maintain context window limits.

**Example:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Will this impact real estate?",
    "history": [
      {"role": "user", "content": "Impact of RBI decisions?"},
      {"role": "assistant", "content": "RBI raised rates by 50bps..."}
    ],
    "stream": false
  }' | python3 -m json.tool
```

---

### ═══════════════════════════════════════════════════════════════════════════════
### SYSTEM ENDPOINTS
### ═══════════════════════════════════════════════════════════════════════════════

## 5. GET `/health` — API Health Check

Returns API status and component availability.

**URL:** `GET http://localhost:8000/health`

**Request:** None

**Response:**
```json
{
  "status": "ok",
  "faiss_articles": 326,
  "gemini": true,
  "model": "gemini-1.5-flash"
}
```

**Response Fields:**
- `status`: API operational status ("ok" or "degraded")
- `faiss_articles`: Number of articles in FAISS index (Phase 2)
- `gemini`: Boolean, true if Gemini API key is valid
- `model`: LLM model name

**Status Code:** 200 OK

**Example:**
```bash
curl http://localhost:8000/health | python3 -m json.tool
```

---

## 6. GET `/docs` — Interactive API Documentation

FastAPI's automatic OpenAPI documentation.

**URL:** `GET http://localhost:8000/docs`

Opens interactive Swagger UI in browser where you can test all endpoints.

---

## Request/Response Format Details

### All Endpoints Use:
- **Format:** JSON
- **Encoding:** UTF-8
- **Content-Type:** `application/json`

### Error Responses:

**503 Gemini Not Available:**
```json
{
  "detail": "Gemini API key not configured. Add GEMINI_API_KEY to .env"
}
```

**500 Internal Error:**
```json
{
  "detail": "Gemini API error: ..."
}
```

---

## Rate Limits

**Free Tier:**
- 1500 requests per day
- 1M tokens per request

**Retry Strategy:**
```bash
# If you get 429 (quota exceeded), wait and retry
sleep 60
curl http://localhost:8000/health
```

---

## Example Workflows

### Workflow 1: Personalized Feed + Briefing

```bash
# 1. Get interests
curl http://localhost:8000/interests

# 2. Get personalized feed
curl -X POST http://localhost:8000/feed \
  -H "Content-Type: application/json" \
  -d '{"interests": ["stocks", "startup"], "top_k": 5}'

# 3. Ask about an article
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize the stock market trends", "stream": false}'
```

### Workflow 2: Multi-Turn Conversation

```bash
# 1. Initial briefing question
Q1="What is the RBI decision impact?"

curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"$Q1\", \"stream\": false}" > response1.json

# 2. Extract answer from response1.json
A1=$(cat response1.json | jq -r '.answer')

# 3. Follow-up question with history
Q2="Which sectors are most affected?"

curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"$Q2\",
    \"history\": [
      {\"role\": \"user\", \"content\": \"$Q1\"},
      {\"role\": \"assistant\", \"content\": \"$A1\"}
    ],
    \"stream\": false
  }" > response2.json
```

### Workflow 3: Category-Specific Research

```bash
# Research only stock market news
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Major stock movements today",
    "stream": false,
    "category_filter": "stocks"
  }'

# Research only startup news
curl -X POST http://localhost:8000/briefing \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Latest startup funding rounds",
    "stream": false,
    "category_filter": "startup"
  }'
```

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| **Initial Response Time** | 500-2000ms |
| **Streaming Token Rate** | ~20-50 tokens/sec |
| **Max Questions/Day** | 1500 (free tier) |
| **Context Window** | Up to 100 articles (~80KB) |
| **API Availability** | 99.9% uptime |

---

## Data Privacy

- No user authentication (free tier)
- Questions are not logged/stored
- Uses MongoDB + Google Gemini API
- Complies with Google's data privacy terms

---

## SDK/Library Support

The API is implemented in FastAPI and can be called from:
- **Python:** requests library
- **JavaScript/Node:** fetch API or axios
- **cURL:** command line
- **Postman:** API testing tool

---

## Migration from Ollama Version

| Feature | Ollama | Gemini |
|---------|--------|--------|
| Chunking endpoint | `/build-index` | None (automatic) |
| Streaming | `/briefing?stream=true` | `/briefing` with `stream=true` |
| Follow-ups | `/ask` with full history | `/ask` with last 4 turns |
| Category filter | Not available | `category_filter` parameter |
| Health check | Included Ollama status | Now includes Gemini status |

---

## Support & Troubleshooting

**API Documentation:** http://localhost:8000/docs  
**Gemini Docs:** https://ai.google.dev/  
**API Key Management:** https://aistudio.google.com/app/apikey  
**FastAPI Docs:** https://fastapi.tiangolo.com/

---

**Last Updated:** March 20, 2026
