import { useState, useEffect, useCallback } from "react";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import FeedPanel from "@/components/FeedPanel";
import AIBriefingPanel from "@/components/AIBriefingPanel";
import { fetchFeed, type Article } from "@/lib/api";

export default function Index() {
  const [activeTab, setActiveTab] = useState("FEED");
  const [selectedInterests, setSelectedInterests] = useState<string[]>(["Stocks & Equity", "Macro Economy"]);
  const [articles, setArticles] = useState<Article[]>([]);
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(false);

  const articleCounts: Record<string, number> = {};
  articles.forEach((a) => {
    if (a.category) {
      articleCounts[a.category] = (articleCounts[a.category] || 0) + 1;
    }
  });

  const loadFeed = useCallback(async () => {
    if (selectedInterests.length === 0) {
      setArticles([]);
      return;
    }
    setLoading(true);
    try {
      const data = await fetchFeed(selectedInterests);
      setArticles(data);
    } catch {
      // API not available — show empty state
      setArticles([]);
    }
    setLoading(false);
  }, [selectedInterests]);

  useEffect(() => {
    loadFeed();
  }, [loadFeed]);

  function toggleInterest(interest: string) {
    setSelectedInterests((prev) =>
      prev.includes(interest) ? prev.filter((i) => i !== interest) : [...prev, interest]
    );
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
        <FeedPanel
          articles={articles}
          selectedArticle={selectedArticle}
          onSelectArticle={setSelectedArticle}
          loading={loading}
        />
        <AIBriefingPanel selectedArticle={selectedArticle} />
      </div>
    </div>
  );
}
