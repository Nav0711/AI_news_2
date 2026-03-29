import { type Article } from "@/lib/api";

interface FeedPanelProps {
  articles: Article[];
  selectedArticle: Article | null;
  onSelectArticle: (article: Article) => void;
  loading: boolean;
}

export default function FeedPanel({ articles, selectedArticle, onSelectArticle, loading }: FeedPanelProps) {
  const now = new Date();
  const dateStr = now.toLocaleDateString("en-IN", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="flex-1 flex flex-row h-full overflow-hidden bg-transparent">
      <div className="flex-1 max-w-[800px] flex flex-col h-full border-r border-border">
        {/* Header */}
      <div className="px-8 pt-8 pb-4 flex items-start justify-between">
        <div>
          <h2 className="font-display text-4xl leading-[1.1] tracking-tight">
            Your <em className="text-primary italic">personalised</em>
            <br />briefing
          </h2>
          <p className="text-sm text-muted-foreground mt-2">
            Ranked by relevance · {articles.length} articles
          </p>
        </div>
        <div className="text-right font-mono-jet text-xs text-muted-foreground leading-relaxed">
          <div>{dateStr}</div>
          <div className="mt-0.5">Last updated {now.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })} IST</div>
        </div>
      </div>

      {/* Articles */}
      <div className="flex-1 overflow-y-auto scrollbar-none px-6 pb-8">
        {loading ? (
          <div className="space-y-3 mt-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-20 rounded-lg bg-muted/30 animate-pulse" />
            ))}
          </div>
        ) : articles.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-muted-foreground">
            <p className="text-sm">Select interests to see your feed</p>
          </div>
        ) : (
          <div className="space-y-2 mt-2">
            {articles.map((article, i) => (
              <button
                key={article.id}
                onClick={() => onSelectArticle(article)}
                className={`w-full text-left p-5 rounded-xl border bg-card backdrop-blur-sm transition-all duration-300 hover:scale-[1.01] hover:shadow-lg hover:shadow-primary/10 active:scale-[0.99] animate-fade-in ${
                  selectedArticle?.id === article.id
                    ? "border-primary/50 bg-primary/5 shadow-sm shadow-primary/20"
                    : "border-border hover:border-primary/30 hover:bg-muted/80"
                }`}
                style={{ animationDelay: `${i * 40}ms` }}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-medium leading-snug line-clamp-2">{article.title}</h3>
                    {article.description && (
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-1">{article.description}</p>
                    )}
                    <div className="flex items-center gap-3 mt-2 text-[11px] font-mono-jet text-muted-foreground">
                      {article.source && <span>{article.source}</span>}
                      {article.category && (
                        <span className="px-1.5 py-0.5 rounded bg-muted/50 text-[10px]">{article.category}</span>
                      )}
                    </div>
                  </div>
                  <div className="flex-shrink-0 text-right">
                    <span className="text-[10px] font-mono-jet text-primary">{(article.relevance_score * 100).toFixed(0)}%</span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>

      {/* Right Rail (Twitter-like) */}
      <div className="hidden xl:flex w-[350px] flex-col p-8 gap-8 border-l border-border bg-transparent">
        <div className="p-5 rounded-2xl bg-card border border-border shadow-sm">
          <h4 className="font-mono-jet text-[10px] tracking-[0.2em] text-muted-foreground mb-4 uppercase">Trending Topics</h4>
          <div className="space-y-4">
            {["#Budget2026", "#RBI", "#StockMarket", "#TechInd", "#Startups"].map((tag) => (
              <div key={tag} className="group cursor-pointer">
                <div className="text-[11px] text-muted-foreground">Trending in India</div>
                <div className="text-sm font-semibold group-hover:text-primary transition-colors">{tag}</div>
                <div className="text-[10px] text-muted-foreground">1.2K Articles</div>
              </div>
            ))}
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-card border border-border shadow-sm">
          <h4 className="font-mono-jet text-[10px] tracking-[0.2em] text-muted-foreground mb-4 uppercase">Market Pulse</h4>
          <div className="space-y-3">
             <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Sensex</span>
                <span className="text-positive font-mono-jet">+0.43%</span>
             </div>
             <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Nifty 50</span>
                <span className="text-negative font-mono-jet">-0.12%</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
