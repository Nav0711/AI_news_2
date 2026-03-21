

interface NavbarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const tabs = ["FEED", "STORY ARC", "BRIEFING"];

const marketData = [
  { label: "SENSEX", value: "73,847", change: "+0.43%", positive: true },
  { label: "NIFTY", value: "22,402", change: "-0.12%", positive: false },
  { label: "₹/USD", value: "83.47", change: "-0.08%", positive: false },
];

export default function Navbar({ activeTab, onTabChange }: NavbarProps) {
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
        {marketData.map((m) => (
          <span key={m.label} className="flex items-center gap-1.5">
            <span className="text-muted-foreground">{m.label}</span>
            <span className="text-foreground">{m.value}</span>
            <span className={m.positive ? "text-positive" : "text-negative"}>{m.change}</span>
          </span>
        ))}
      </div>
    </nav>
  );
}
