# Phase 4: Story Arc Tracker - Timeline Generation

import json
from datetime import datetime

def generate_timeline(articles):
    """
    Generate a timeline from clustered articles.

    Args:
        articles (list[dict]): List of articles with metadata (title, date, cluster).

    Returns:
        dict: Timeline data grouped by cluster.
    """
    timeline = {}
    for article in articles:
        cluster = article.get("cluster")
        if cluster not in timeline:
            timeline[cluster] = []
        timeline[cluster].append({
            "title": article.get("title"),
            "date": article.get("date"),
            "source": article.get("source")
        })
    return timeline

# Example usage
if __name__ == "__main__":
    sample_articles = [
        {"title": "AI startup raises $10M", "date": "2026-03-20", "cluster": 0, "source": "TechCrunch"},
        {"title": "Inflation impacts tech", "date": "2026-03-19", "cluster": 1, "source": "Reuters"}
    ]
    print(json.dumps(generate_timeline(sample_articles), indent=4))