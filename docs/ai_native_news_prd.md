
# AI-Native News Experience — Product Requirements Document (PRD)

## Product Name
**NewsET – AI Native Newsroom**

---

# 1. Product Vision

Create a **next-generation AI-powered business news platform** where users interact with news rather than passively reading static articles.

The system will:
- Personalize news for each user
- Provide AI-generated briefings
- Track evolving business stories
- Translate business news into Indian languages
- Generate quick video summaries

Goal:
> Deliver a news experience where users say *“I can’t go back to reading news the old way.”*

This document defines a **prototype-friendly architecture using free tools** suitable for hackathons or early-stage MVP development.

---

# 2. Problem Statement

Current news platforms suffer from:

- Static news feeds
- Same homepage for every user
- Fragmented articles about the same story
- No intelligent summaries
- Limited accessibility due to language barriers

Users need:

- Personalized news feeds
- Context-aware AI explanations
- Story timelines
- Multi-language accessibility

---

# 3. Target Users

## Retail Investors
Interested in:
- stock market news
- company earnings
- regulatory announcements

## Startup Founders
Interested in:
- funding announcements
- competitor activity
- tech sector trends

## Students
Interested in:
- simplified explanations
- economic insights

## Business Readers
Interested in:
- macroeconomic updates
- corporate developments

---

# 4. Core Features

## Feature 1 — Personalized Newsroom (NewsET)

Each user sees a **customized news feed**.

### Inputs
- user interests
- reading behavior
- trending stories

### Output
Recommended articles ranked by relevance.

Example:
User interest = "Mutual Funds"

Feed shows:
- SIP trends
- SEBI policy updates
- AMC performance

---

## Feature 2 — AI News Navigator (Interactive Briefing)

Instead of reading multiple articles about a topic, the user receives a **single AI-generated briefing**.

Example Topic:
Union Budget 2026

AI generates:

- key policy highlights
- sector impacts
- expert reactions
- future outlook

Users can ask follow-up questions.

---

## Feature 3 — Story Arc Tracker

Tracks major ongoing stories and visualizes them.

Example:
Adani Infrastructure Expansion

Timeline shows:
- major announcements
- key players
- market reactions
- future predictions

---

## Feature 4 — Vernacular News Engine

Translate and explain business news into:

- Hindi
- Tamil
- Telugu
- Bengali

Important:
Translation must include **context explanation**, not literal translation.

---

## Feature 5 — AI Video Summary (Optional)

Convert news articles into short videos.

Output:
- 60 second summary
- narration
- data visualizations

---

# 5. System Architecture

High-level architecture:

News Sources
→ News Ingestion Pipeline
→ Article Processing
→ Embedding Generator
→ Vector Database
→ AI Processing Layer
→ API Services
→ Frontend UI

---

# 6. Technology Stack (Free Tools Only)

## Frontend

Next.js
React
Tailwind CSS
Recharts (charts)
D3.js (timelines)

Free hosting:
Vercel

---

## Backend

FastAPI (Python API server)

Additional tools:

Celery (background tasks)
Redis (task queue)

Hosting:
Railway / Render free tier

---

## AI Models

Run locally using:

Ollama

Recommended models:

Llama 3
Mistral
Phi-3

---

## NLP / ML Tools

Sentence Transformers (embeddings)

Model:
all-MiniLM-L6-v2

spaCy (entity recognition)

BERTopic (topic clustering)

---

## Databases

MongoDB (news storage)

PostgreSQL (user data)

FAISS (vector search)

---

## Data Sources

NewsAPI
GNews
Yahoo Finance API

---

## Translation

IndicTrans2

or

Meta NLLB model

---

## Video Generation

MoviePy
FFmpeg
Edge TTS

---

# 7. Development Phases

The system will be implemented in **5 phases**.

Total estimated time for prototype:
36–40 hours.

---

# Phase 1 — News Data Pipeline

Goal:
Collect and store news articles.

Steps:

1. Register for NewsAPI key
2. Create Python script to fetch news
3. Clean article text
4. Store articles in MongoDB

Pipeline:

News API
→ Article Fetcher
→ Text Cleaner
→ Database

Tools:

Python
NewsAPI
BeautifulSoup
MongoDB

Deliverable:
Database with 500+ news articles.

---

# Phase 2 — Personalized Recommendation Engine

Goal:
Build the **NewsET personalized feed**.

Steps:

1. Generate embeddings for articles
2. Store embeddings in FAISS
3. Create user profile vectors
4. Implement similarity search

Pipeline:

User Interest
→ Embedding
→ Vector Search
→ Top Articles

Tools:

Sentence Transformers
FAISS
FastAPI

Deliverable:
Personalized news feed.

---

# Phase 3 — AI News Navigator (RAG)

Goal:
Create AI-powered news briefings.

Steps:

1. Split articles into chunks
2. Store chunks in vector DB
3. Retrieve relevant chunks
4. Generate response using LLM

Pipeline:

User Question
→ Vector Search
→ Relevant Chunks
→ LLM Answer

Tools:

Ollama
Llama3
LangChain
FAISS

Deliverable:
Interactive AI briefing system.

---

# Phase 4 — Story Arc Tracker

Goal:
Track evolving news stories.

Steps:

1. Cluster news articles by topic
2. Extract entities
3. Generate story timeline

Pipeline:

Articles
→ Topic Clustering
→ Entity Extraction
→ Timeline

Tools:

BERTopic
spaCy
D3.js

Deliverable:
Interactive timeline visualization.

---

# Phase 5 — Vernacular News Engine

Goal:
Translate business news to regional languages.

Steps:

1. Simplify article
2. Translate
3. Add contextual explanation

Pipeline:

English Article
→ Summary
→ Translation
→ Explanation

Tools:

IndicTrans2
NLLB
Ollama

Deliverable:
Hindi and regional language news.

---

# 8. Demo Flow

Final hackathon demo:

User selects interests
→ Personalized news feed appears
→ User opens article
→ AI briefing is generated
→ Story timeline appears
→ Article translated to Hindi

---

# 9. Repository Structure

Recommended project structure:

ai-news-platform/

frontend/

backend/

ai-services/

data-pipeline/

vector-db/

scripts/

README.md

---

# 10. Success Criteria

Prototype should demonstrate:

- AI-powered personalized news
- Interactive briefing capability
- Story evolution tracking
- Multi-language support

Judges should see a **clear AI workflow and user interaction.**

---

# End of PRD
