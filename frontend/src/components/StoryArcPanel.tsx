import { useQuery } from "@tanstack/react-query";
import { fetchStoryArc } from "@/lib/api";
import { ScrollArea } from "./ui/scroll-area";

export default function StoryArcPanel() {
  const { data: timeline, isLoading } = useQuery({
    queryKey: ["storyArc"],
    queryFn: () => fetchStoryArc(),
  });

  if (isLoading) {
    return (
      <div className="flex-1 p-8 animate-pulse">
        <div className="h-8 w-48 bg-muted rounded mb-8" />
        <div className="space-y-12">
          {[1, 2, 3].map((i) => (
            <div key={i} className="relative pl-8 border-l-2 border-muted">
              <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-muted" />
              <div className="h-4 w-32 bg-muted rounded mb-3" />
              <div className="h-20 w-full bg-muted rounded" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  const clusters = timeline ? Object.keys(timeline) : [];

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden border-l border-white/5 bg-black/20 relative">
      <div className="px-8 pt-8 pb-4">
        <h2 className="font-display text-4xl leading-[1.1] tracking-tight">
          Story <em className="text-gold italic">Arc</em>
          <br />Tracker
        </h2>
        <p className="text-sm text-muted-foreground mt-2">
          Evolving business narratives through AI clustering
        </p>
      </div>

      <ScrollArea className="flex-1 px-8 pb-8">
        <div className="space-y-16 mt-8">
          {clusters.map((clusterId) => (
            <div key={clusterId} className="space-y-6">
              <h3 className="font-mono-jet text-xs tracking-widest text-gold uppercase">
                Cluster #{clusterId}
              </h3>
              <div className="space-y-8 relative pl-8 border-l border-gold/20">
                {timeline[clusterId].map((event, idx) => (
                  <div key={idx} className="relative animate-fade-in" style={{ animationDelay: `${idx * 100}ms` }}>
                    <div className="absolute -left-[33px] top-1 w-2.5 h-2.5 rounded-full bg-gold shadow-[0_0_8px_rgba(212,175,55,0.5)]" />
                    <div className="text-[10px] font-mono-jet text-muted-foreground mb-1 uppercase">
                      {new Date(event.date).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}
                    </div>
                    <h4 className="text-sm font-medium leading-snug">{event.title}</h4>
                    <p className="text-xs text-muted-foreground mt-1 opacity-70">{event.source}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
          
          {clusters.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
              <p>No story arcs detected in the current feed.</p>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
