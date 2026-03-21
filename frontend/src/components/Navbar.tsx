

import { useQuery } from "@tanstack/react-query";
import { fetchMarketStats } from "@/lib/api";

interface NavbarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const tabs = ["FEED", "STORY ARC", "BRIEFING"];



export default function Navbar({ activeTab, onTabChange }: NavbarProps) {
  const { data: marketStats, isLoading } = useQuery({
    queryKey: ["marketStats"],
    queryFn: fetchMarketStats,
    refetchInterval: 15 * 60 * 1000, // 15 mins
  });
  return (
    <nav className="flex items-center gap-1 px-6 py-3 border-b border-border bg-background/95 backdrop-blur-sm sticky top-0 z-50">
      <h1 className="font-display text-xl tracking-tight mr-6">
        News<span className="text-gold">ET</span>
        <span className="inline-block w-1.5 h-1.5 rounded-full bg-gold ml-1 animate-pulse-dot" />
      </h1>

      <div className="flex items-center gap-1">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => onTabChange(tab)}
            className={`px-4 py-1.5 rounded-md text-xs font-mono-jet tracking-widest transition-all duration-200 active:scale-[0.97] ${
              activeTab === tab
                ? "bg-gold text-background font-semibold"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      <div className="ml-auto flex items-center gap-5 font-mono-jet text-[11px]">
        {isLoading ? (
          <span className="text-muted-foreground animate-pulse">Loading markets...</span>
        ) : (
          marketStats?.map((m) => (
            <span key={m.symbol} className="flex items-center gap-1.5">
              <span className="text-muted-foreground">{m.name}</span>
              <span className="text-foreground">{m.price.toLocaleString()}</span>
              <span className={m.change >= 0 ? "text-positive" : "text-negative"}>
                {m.change >= 0 ? "+" : ""}{m.change_percent.toFixed(2)}%
              </span>
            </span>
          ))
        )}
      </div>
    </nav>
  );
}
