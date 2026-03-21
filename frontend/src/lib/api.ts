const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface Article {
  id: string;
  title: string;
  description: string | null;
  source: string | null;
  published_at: string | null;
  category: string | null;
  url: string | null;
  relevance_score: number;
}

export interface LanguageInfo {
  name: string;
  native: string;
  code: string;
  speakers: string;
  flag: string;
}

export interface HealthStatus {
  status: string;
  faiss_articles: number;
  gemini: boolean;
  vernacular: boolean;
  model: string;
}

export async function fetchFeed(interests: string[], readIds: string[] = [], topK = 20): Promise<Article[]> {
  const res = await fetch(`${API_BASE}/feed`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ interests, read_article_ids: readIds, top_k: topK }),
  });
  if (!res.ok) throw new Error("Failed to fetch feed");
  return res.json();
}

export async function fetchInterests(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/interests`);
  if (!res.ok) throw new Error("Failed to fetch interests");
  return res.json();
}

export async function fetchLanguages(): Promise<LanguageInfo[]> {
  const res = await fetch(`${API_BASE}/languages`);
  if (!res.ok) throw new Error("Failed to fetch languages");
  return res.json();
}

export async function fetchHealth(): Promise<HealthStatus> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function* streamBriefing(question: string, categoryFilter?: string): AsyncGenerator<string> {
  const res = await fetch(`${API_BASE}/briefing`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, stream: true, category_filter: categoryFilter || null }),
  });
  if (!res.ok) throw new Error("Briefing request failed");
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    yield decoder.decode(value, { stream: true });
  }
}

export async function* streamFollowUp(question: string, history: { role: string; content: string }[]): AsyncGenerator<string> {
  const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, history, stream: true }),
  });
  if (!res.ok) throw new Error("Follow-up request failed");
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    yield decoder.decode(value, { stream: true });
  }
}

export async function* streamTranslation(title: string, content: string, languageCode: string): AsyncGenerator<string> {
  const res = await fetch(`${API_BASE}/translate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content, language_code: languageCode, simplify: true, stream: true }),
  });
  if (!res.ok) throw new Error("Translation request failed");
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    yield decoder.decode(value, { stream: true });
  }
}
