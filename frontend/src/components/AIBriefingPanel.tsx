import { useState, useEffect, useRef } from "react";
import { type Article, type LanguageInfo, fetchLanguages, streamBriefing, streamFollowUp, streamTranslation, generateVideoSummary } from "@/lib/api";
import { useQuery } from "@tanstack/react-query";
import { Info, Play, Loader2 } from "lucide-react";
import VideoPlayer from "./VideoPlayer";

interface AIBriefingPanelProps {
  selectedArticle: Article | null;
}

const QUICK_QUESTIONS = ["Market impact?", "Key players?", "What next?", "Historical context?"];

export default function AIBriefingPanel({ selectedArticle }: AIBriefingPanelProps) {
  const [briefing, setBriefing] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [followUpInput, setFollowUpInput] = useState("");
  const [history, setHistory] = useState<{ role: string; content: string }[]>([]);
  const [languagesState, setLanguagesState] = useState<LanguageInfo[]>([]);
  const [selectedLang, setSelectedLang] = useState("en");
  const [translation, setTranslation] = useState("");
  const [isTranslating, setIsTranslating] = useState(false);
  const [isGeneratingVideo, setIsGeneratingVideo] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  
  const briefingRef = useRef<HTMLDivElement>(null);
  const { data: languages = [
    { name: "Hindi", native: "हिन्दी", code: "hi", speakers: "600M+", flag: "🇮🇳" },
    { name: "Tamil", native: "தமிழ்", code: "ta", speakers: "80M+", flag: "🇮🇳" },
    { name: "Telugu", native: "తెలుగు", code: "te", speakers: "85M+", flag: "🇮🇳" },
    { name: "Bengali", native: "বাংলা", code: "bn", speakers: "230M+", flag: "🇮🇳" },
  ] } = useQuery({
    queryKey: ["languages"],
    queryFn: fetchLanguages,
  });

  useEffect(() => {
    if (!selectedArticle) return;
    setBriefing("");
    setTranslation("");
    setHistory([]);
    setSelectedLang("en");
    setVideoUrl(null);
    generateBriefing(selectedArticle);
  }, [selectedArticle]);

  async function generateBriefing(article: Article) {
    setIsStreaming(true);
    const question = `Give me a detailed briefing about this article: "${article.title}". ${article.description || ""}`;
    let full = "";
    try {
      for await (const chunk of streamBriefing(question, article.category || undefined)) {
        full += chunk;
        setBriefing(full);
      }
      setHistory([{ role: "user", content: question }, { role: "assistant", content: full }]);
    } catch {
      setBriefing("Failed to generate briefing. Check API connection.");
    }
    setIsStreaming(false);
  }

  async function handleFollowUp(question: string) {
    if (!question.trim() || isStreaming) return;
    setFollowUpInput("");
    setIsStreaming(true);
    const newHistory = [...history, { role: "user", content: question }];
    setHistory(newHistory);
    let full = "";
    setBriefing((prev) => prev + `\n\n**Q: ${question}**\n\n`);
    try {
      for await (const chunk of streamFollowUp(question, newHistory)) {
        full += chunk;
        setBriefing((prev) => {
          const parts = prev.split(`**Q: ${question}**\n\n`);
          return parts[0] + `**Q: ${question}**\n\n` + full;
        });
      }
      setHistory([...newHistory, { role: "assistant", content: full }]);
    } catch {
      setBriefing((prev) => prev + "\n\n_Failed to get response._");
    }
    setIsStreaming(false);
  }

  async function handleTranslate(langCode: string) {
    setSelectedLang(langCode);
    if (langCode === "en" || !selectedArticle || !briefing) {
      setTranslation("");
      return;
    }
    setIsTranslating(true);
    setTranslation("");
    let full = "";
    try {
      for await (const chunk of streamTranslation(selectedArticle.title, briefing, langCode)) {
        full += chunk;
        setTranslation(full);
      }
    } catch {
      setTranslation("Translation failed.");
    }
    setIsTranslating(false);
  }

  async function handleGenerateVideo() {
    if (!selectedArticle || isGeneratingVideo) return;
    setIsGeneratingVideo(true);
    try {
      const url = await generateVideoSummary(
        selectedArticle.id,
        selectedArticle.title,
        selectedArticle.description || ""
      );
      setVideoUrl(url);
    } catch (err) {
      console.error("Failed to generate video", err);
      alert("Failed to generate Video Summary.");
    } finally {
      setIsGeneratingVideo(false);
    }
  }

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden border-l border-white/5 bg-black/20 relative">
      {/* Header */}
      <div className="px-5 pt-5 pb-3 border-b border-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-muted flex items-center justify-center">
              <span className="text-sm">🤖</span>
            </div>
            <div>
              <h3 className="text-[10px] font-mono-jet tracking-[0.2em] text-muted-foreground">AI BRIEFING</h3>
              <p className="text-[11px] text-muted-foreground">Gemini 2.0 Flash · 100 articles in context</p>
            </div>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full animate-pulse-dot" style={{ backgroundColor: "hsl(var(--green))" }} />
            <span className="text-[10px] font-mono-jet text-positive">Live</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto scrollbar-thin px-5 py-4" ref={briefingRef}>
        {!selectedArticle ? (
          <div className="flex flex-col items-center justify-center h-full text-center animate-fade-in">
            <h4 className="text-[10px] font-mono-jet tracking-[0.2em] text-muted-foreground mb-2">SELECTED ARTICLE</h4>
            <p className="text-sm text-muted-foreground italic mb-8">Click any article card to generate an AI briefing</p>
            <div className="w-14 h-14 rounded-full bg-muted/50 flex items-center justify-center mb-4">
              <Info className="w-6 h-6 text-muted-foreground/50" />
            </div>
            <p className="font-display text-xl italic text-muted-foreground/60">No article selected</p>
            <p className="text-xs text-muted-foreground mt-2 max-w-[200px]">
              Select an article from your feed to get an instant AI-powered briefing
            </p>
          </div>
        ) : (
          <div className="animate-fade-in pb-10">
            <h4 className="text-[10px] font-mono-jet tracking-[0.2em] text-muted-foreground mb-1">SELECTED ARTICLE</h4>
            <p className="text-sm font-medium mb-4 text-foreground">{selectedArticle.title}</p>
            <div className="text-sm leading-relaxed text-secondary-foreground whitespace-pre-wrap">
              {briefing}
              {isStreaming && <span className="inline-block w-1.5 h-4 bg-gold animate-pulse ml-0.5" />}
            </div>
            {translation && (
              <div className="mt-4 pt-4 border-t border-border animate-fade-in">
                <h4 className="text-[10px] font-mono-jet tracking-[0.2em] text-muted-foreground mb-2 flex items-center gap-2">
                  TRANSLATION
                  <span className="text-xs font-sans text-gold">({languages.find(l => l.code === selectedLang)?.native})</span>
                </h4>
                <div className="text-sm leading-relaxed text-secondary-foreground whitespace-pre-wrap">
                  {translation}
                  {isTranslating && <span className="inline-block w-1.5 h-4 bg-gold animate-pulse ml-0.5" />}
                </div>
              </div>
            )}
            
            {/* Generate Video Action */}
            {!isStreaming && briefing && (
              <div className="mt-8 flex justify-center animate-fade-in">
                <button
                  onClick={handleGenerateVideo}
                  disabled={isGeneratingVideo}
                  className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-primary text-primary-foreground text-sm font-medium transition-all active:scale-95 disabled:opacity-70 shadow-lg shadow-primary/20"
                >
                  {isGeneratingVideo ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Generating Summary Video...
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4" />
                      Create AI Video Summary
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Languages */}
      <div className="px-5 py-3 border-t border-border bg-background/50 backdrop-blur-md">
        <div className="flex items-center gap-2 overflow-x-auto scrollbar-none pb-1">
          <span className="text-[10px] font-mono-jet tracking-[0.2em] text-muted-foreground flex-shrink-0">TRANSLATE</span>
          <button
            onClick={() => handleTranslate("en")}
            disabled={!selectedArticle || isTranslating}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-all active:scale-95 flex-shrink-0 ${
              selectedLang === "en" ? "bg-gold text-background" : "border border-border text-muted-foreground hover:text-foreground"
            }`}
          >
            English
          </button>
          {languages.map((lang) => (
            <button
              key={lang.code}
              onClick={() => handleTranslate(lang.code)}
              disabled={!selectedArticle || isTranslating}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-all active:scale-95 flex-shrink-0 ${
                selectedLang === lang.code
                  ? "bg-gold text-background"
                  : "border border-border text-muted-foreground hover:text-foreground"
              }`}
            >
              {lang.native}
            </button>
          ))}
        </div>
      </div>

      {/* Follow-up */}
      <div className="px-5 py-4 border-t border-border bg-background">
        <h4 className="text-[10px] font-mono-jet tracking-[0.2em] text-muted-foreground mb-2">ASK A FOLLOW-UP QUESTION</h4>
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={followUpInput}
            onChange={(e) => setFollowUpInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleFollowUp(followUpInput)}
            placeholder="e.g. Which sectors are most affected?"
            className="flex-1 bg-muted/30 border border-border rounded-lg px-3 py-2.5 text-sm placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-ring transition-shadow"
            disabled={!selectedArticle || isStreaming}
          />
          <button
            onClick={() => handleFollowUp(followUpInput)}
            disabled={!followUpInput.trim() || isStreaming}
            className="px-4 py-2.5 rounded-lg border border-border text-sm font-mono-jet text-muted-foreground hover:text-foreground hover:border-foreground/20 transition-all active:scale-95 disabled:opacity-40"
          >
            Ask →
          </button>
        </div>
        <div className="flex flex-wrap gap-2 mt-3">
          {QUICK_QUESTIONS.map((q) => (
            <button
              key={q}
              onClick={() => handleFollowUp(q)}
              disabled={!selectedArticle || isStreaming}
              className="px-3 py-1.5 rounded-lg border border-border text-xs text-muted-foreground hover:text-foreground hover:border-foreground/20 transition-all active:scale-95 disabled:opacity-40"
            >
              {q}
            </button>
          ))}
        </div>
      </div>
      
      {/* Video Overlay */}
      {videoUrl && (
        <VideoPlayer videoUrl={videoUrl} onClose={() => setVideoUrl(null)} />
      )}
    </div>
  );
}
