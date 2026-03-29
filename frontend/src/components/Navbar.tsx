import { useQuery } from "@tanstack/react-query";
import { fetchMarketStats } from "@/lib/api";
import { Moon, Sun, UserCircle } from "lucide-react";
import { useTheme } from "./ThemeProvider";
import { Link } from "react-router-dom";

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
  
  const { theme, setTheme } = useTheme();

  return (
    <nav className="flex items-center gap-1 px-6 py-3 border-b border-border bg-card/95 backdrop-blur-sm sticky top-0 z-50 transition-colors duration-300">
      <Link to="/" className="font-display text-xl tracking-tight mr-6 hover:opacity-80 transition-opacity">
        My<span className="text-primary">ET</span>
        <span className="inline-block w-1.5 h-1.5 rounded-full bg-primary ml-1 animate-pulse-dot" />
      </Link>

      <div className="flex items-center gap-1 hidden sm:flex">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => onTabChange(tab)}
            className={`px-4 py-1.5 rounded-md text-xs font-mono-jet tracking-widest transition-all duration-200 active:scale-[0.97] ${
              activeTab === tab
                ? "bg-primary text-primary-foreground font-semibold shadow-sm shadow-primary/20"
                : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      <div className="ml-auto flex items-center gap-5">
        <div className="hidden lg:flex items-center gap-5 font-mono-jet text-[11px] mr-4 border-r border-border pr-5 py-1">
          {isLoading ? (
            <span className="text-muted-foreground animate-pulse">Loading markets...</span>
          ) : (
            marketStats?.map((m) => (
              <span key={m.symbol} className="flex items-center gap-1.5">
                <span className="text-muted-foreground">{m.name}</span>
                <span className="text-foreground tracking-tight">{m.price.toLocaleString()}</span>
                <span className={m.change >= 0 ? "text-secondary font-bold" : "text-destructive font-bold"}>
                  {m.change >= 0 ? "+" : ""}{m.change_percent.toFixed(2)}%
                </span>
              </span>
            ))
          )}
        </div>
        
        <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-1.5 rounded-full bg-muted/50 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors border border-transparent hover:border-border"
            title="Toggle theme"
          >
            {theme === "dark" ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </button>
        
        <Link to="/profile" className="p-1.5 rounded-full text-foreground hover:text-primary transition-colors active:scale-95" title="User Profile">
            <UserCircle className="w-6 h-6" />
        </Link>
      </div>
    </nav>
  );
}
