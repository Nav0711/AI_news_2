import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchInterests, fetchHealth, type HealthStatus } from "@/lib/api";

interface SidebarProps {
  selectedInterests: string[];
  onToggleInterest: (interest: string) => void;
  articleCounts: Record<string, number>;
}

export default function Sidebar({ selectedInterests, onToggleInterest, articleCounts }: SidebarProps) {
  const [trendingTopics] = useState([
    "#RBI", "#Budget2026", "#SEBI", "#Adani", "#Infosys", "#FinTech",
  ]);

  const { data: interests = ["Stocks & Equity", "Macro Economy", "Startup & VC", "Corporate", "Crypto & Web3", "Real Estate"] } = useQuery({
    queryKey: ["interests"],
    queryFn: fetchInterests,
  });

  const { data: health = null } = useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
    refetchInterval: 60000, // Check health every 60 seconds instead of aggressively
  });

  return (
    <aside className="w-72 border-r border-border flex flex-col h-full overflow-y-auto scrollbar-thin bg-card/50">
      <div className="p-5 flex-1">
        <h2 className="text-[10px] font-mono-jet tracking-[0.2em] text-muted-foreground mb-4">YOUR INTERESTS</h2>
        <ul className="space-y-1">
          {interests.map((interest, i) => {
            const selected = selectedInterests.includes(interest);
            const count = articleCounts[interest] || 0;
            return (
              <li
                key={interest}
                onClick={() => onToggleInterest(interest)}
                className={`flex items-center justify-between px-3 py-2.5 rounded-lg cursor-pointer transition-all duration-200 active:scale-[0.97] animate-fade-in ${
                  selected
                    ? "border border-primary/40 bg-primary/5"
                    : "hover:bg-muted/50"
                }`}
                style={{ animationDelay: `${i * 60}ms` }}
              >
                <span className="flex items-center gap-2.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${selected ? "bg-primary" : "bg-muted-foreground/40"}`} />
                  <span className={`text-sm ${selected ? "text-primary font-medium" : "text-secondary-foreground"}`}>
                    {interest}
                  </span>
                </span>
                {count > 0 && (
                  <span className={`text-xs font-mono-jet ${selected ? "text-primary" : "text-muted-foreground"}`}>
                    {count}
                  </span>
                )}
              </li>
            );
          })}
        </ul>
      </div>

      {/* Stats */}
      <div className="px-5 py-4 border-t border-border">
        <div className="font-mono-jet text-[11px] text-muted-foreground space-y-1">
          <div>VECTORS <span className="text-foreground">{health?.faiss_articles || "—"}</span></div>
          <div>INDEX DIM <span className="text-foreground">384</span></div>
          <div>LATENCY <span className="text-foreground">~6ms</span></div>
          <div>MODEL <span className="text-foreground">{health?.model || "gemini-1.5-flash"}</span></div>
          <div>GEMINI <span className={health?.gemini ? "text-positive" : "text-negative"}>{health?.gemini ? "✓" : "✗"}</span></div>
        </div>
      </div>

      {/* Trending */}
      <div className="px-5 py-4 border-t border-border">
        <h2 className="text-[10px] font-mono-jet tracking-[0.2em] text-muted-foreground mb-3">TRENDING TOPICS</h2>
        <div className="flex flex-wrap gap-2">
          {trendingTopics.map((tag) => (
            <span
              key={tag}
              className="px-2.5 py-1 rounded-md border border-border text-xs font-mono-jet text-muted-foreground hover:text-foreground hover:border-foreground/20 transition-colors cursor-pointer active:scale-95"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </aside>
  );
}
