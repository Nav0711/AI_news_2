import { useState, useEffect, useCallback } from "react";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import FeedPanel from "@/components/FeedPanel";
import AIBriefingPanel from "@/components/AIBriefingPanel";
import StoryArcPanel from "@/components/StoryArcPanel";
import { useQuery } from "@tanstack/react-query";
import { fetchFeed, type Article } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function Index() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState("FEED");
  const defaultInterests = user?.interests?.length ? user.interests : ["Stocks & Equity", "Macro Economy"];
  const [selectedInterests, setSelectedInterests] = useState<string[]>(defaultInterests);
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);

  const { data: articles = [], isLoading: loading } = useQuery({
    queryKey: ["feed", selectedInterests],
    queryFn: () => fetchFeed(selectedInterests),
    enabled: selectedInterests.length > 0,
  });

  const articleCounts: Record<string, number> = {};
  articles.forEach((a) => {
    if (a.category) {
      articleCounts[a.category] = (articleCounts[a.category] || 0) + 1;
    }
  });



  function toggleInterest(interest: string) {
    setSelectedInterests((prev) =>
      prev.includes(interest) ? prev.filter((i) => i !== interest) : [...prev, interest]
    );
  }
  function handleSelectArticle(article: Article) {
    setSelectedArticle(article);
    setActiveTab("BRIEFING"); // automatically navigate to briefing tab
  }

  return (
    <div className="flex flex-col h-screen bg-background overflow-hidden">
      <Navbar activeTab={activeTab} onTabChange={setActiveTab} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          selectedInterests={selectedInterests}
          onToggleInterest={toggleInterest}
          articleCounts={articleCounts}
        />
        <div className="flex-1 flex bg-muted/20 overflow-hidden relative">
          {activeTab === "STORY ARC" && <StoryArcPanel />}
          {activeTab === "FEED" && (
            <FeedPanel
              articles={articles}
              selectedArticle={selectedArticle}
              onSelectArticle={handleSelectArticle}
              loading={loading}
            />
          )}
          {activeTab === "BRIEFING" && <AIBriefingPanel selectedArticle={selectedArticle} />}
        </div>
      </div>
    </div>
  );
}
