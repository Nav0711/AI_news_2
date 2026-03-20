Product Requirements Document (PRD)
Product Name

MyET – AI Native Newsroom

Vision

Create a next-generation business news experience where users interact with news instead of just reading static articles. The platform uses AI to deliver personalized news, interactive briefings, story timelines, and vernacular translations.

The goal is to make users feel:

“I can’t go back to reading news the old way.”

Problem Statement

Traditional news delivery is static:

same homepage for all users

articles scattered across pages

no personalization

difficult to track evolving business stories

English-only accessibility barrier

Users want:

personalized news

interactive explanations

quick insights

localized content

Target Users
1. Retail Investors

Interested in:

stock market news

corporate announcements

macroeconomic policies

2. Startup Founders

Interested in:

funding news

competitor moves

policy changes

3. Students

Interested in:

simplified explanations

economic concepts

4. General Business Readers

Interested in:

daily business highlights

major corporate stories

Core Features
1. Personalized Newsroom (My ET)

AI generates a customized news feed for each user.

Personalization signals:

selected interests

reading history

trending stories

Output:

recommended articles

sector-specific news

Example:

User interest: Mutual funds

Feed shows:

SEBI policy updates

AMC performance

SIP trends

2. News Navigator (AI Briefings)

Instead of reading multiple articles, the user gets:

one synthesized briefing

key insights

follow-up Q&A

Example output:

Topic: Union Budget 2026

Sections:

key policy changes

market impact

sector winners/losers

expert reactions

Users can ask:

“Impact on IT stocks?”

3. Story Arc Tracker

Tracks major ongoing business stories.

Example:

Story: Adani Green Expansion

Shows:

timeline of events

key players

sentiment shifts

future outlook

4. Vernacular News Engine

Translates and explains business news into:

Hindi

Tamil

Telugu

Bengali

Important: not literal translation but contextual explanation.

5. AI News Video Generator (Optional Advanced Feature)

Converts article → 60-second video summary.

Includes:

narration

charts

key points

Key Success Metrics
Metric	Goal
User engagement	+40% reading time
Personalized click rate	>30%
AI briefing usage	>25%
Story tracker usage	>20%
System Architecture Overview

Pipeline:

News Sources
↓
News Collector
↓
Processing Pipeline
↓
Embedding Generator
↓
Vector Database
↓
AI Services
↓
Frontend Dashboard

AI components:

recommendation engine

RAG summarization

topic clustering

translation

Technology Stack (Free Tools)
Frontend
Tool	Purpose
Next.js	UI framework
Tailwind CSS	styling
Recharts	charts
D3.js	timelines
Backend
Tool	Purpose
FastAPI	API server
Python	AI processing
Celery	async tasks
Redis	job queue
AI / ML
Tool	Purpose
Ollama	run local LLMs
Llama 3 / Mistral	summarization
Sentence Transformers	embeddings
BERTopic	topic clustering
spaCy	entity extraction
Databases
Tool	Purpose
PostgreSQL	user data
MongoDB	news articles
FAISS	vector search
Data Sources
Source	Use
NewsAPI	business news
GNews	global news
Yahoo Finance API	market data
Translation
Tool	Purpose
IndicTrans2	Indian language translation
NLLB (Meta)	multilingual translation
Video Generation
Tool	Purpose
MoviePy	video editing
Edge TTS	narration
FFmpeg	rendering
5-Phase Implementation Plan
Phase 1 — Data Collection & News Pipeline

Goal:
Build a news ingestion system.

Tasks

Integrate news APIs

Fetch business articles

Clean article content

Store in database

Pipeline

News API
↓
Article Fetcher
↓
Text Cleaner
↓
Database Storage

Tech

Python
NewsAPI
BeautifulSoup
MongoDB

Deliverable

Working database with news articles updated daily.

Phase 2 — AI Personalization Engine

Goal
Build MyET personalized feed.

Steps

Generate embeddings for articles

Store embeddings in FAISS

Create user interest vectors

Build similarity search

Recommendation flow

User Interest
↓
Embedding
↓
Vector Search
↓
Top 10 Articles

Tech

Sentence Transformers
FAISS
FastAPI

Deliverable

Users see personalized article recommendations.

Phase 3 — News Navigator (RAG AI Briefing)

Goal
Create AI-powered interactive briefing.

Steps

chunk articles

store in vector DB

retrieve relevant context

generate explanation using LLM

Pipeline

User Question
↓
Vector Search
↓
Relevant News Chunks
↓
LLM Answer

Tech

Ollama
Llama3
LangChain
FAISS

Deliverable

Users can ask questions about news topics.

Phase 4 — Story Arc Tracker

Goal
Track evolving business stories.

Steps

topic clustering

entity extraction

timeline generation

Pipeline

News Articles
↓
Topic Clustering
↓
Entity Extraction
↓
Timeline Builder

Tech

BERTopic
spaCy
D3.js

Deliverable

Interactive story timeline.

Phase 5 — Vernacular News Engine

Goal
Make business news accessible to Indian languages.

Steps

simplify article

translate

add explanation layer

Pipeline

English Article
↓
Simplified Summary
↓
Translation
↓
Localized Explanation

Tech

IndicTrans2
NLLB
Ollama

Deliverable

Users can read business news in Hindi and regional languages.

Final Demo Flow (Hackathon)

Your demo should show:

User selects interests
↓
Personalized news feed appears
↓
User clicks story
↓
AI briefing opens
↓
Story timeline visualized
↓
Article translated to Hindi

This demonstrates a true AI-native news platform.

Estimated Development Effort
Phase	Time
Phase 1	6 hours
Phase 2	8 hours
Phase 3	10 hours
Phase 4	8 hours
Phase 5	6 hours

Total hackathon build: ~36–40 hours