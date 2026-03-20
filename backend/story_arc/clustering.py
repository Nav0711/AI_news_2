# Phase 4: Story Arc Tracker - Topic Clustering

from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Initialize BERTopic
model = BERTopic()

def cluster_articles(documents):
    """
    Cluster articles into topics using BERTopic.

    Args:
        documents (list[str]): List of article texts.

    Returns:
        tuple: Topics and probabilities for each document.
    """
    topics, probs = model.fit_transform(documents)
    return topics, probs

# Example usage
if __name__ == "__main__":
    sample_articles = [
        "AI is transforming the tech industry.",
        "The stock market is volatile due to inflation.",
        "AI startups are raising significant funding."
    ]
    print(cluster_articles(sample_articles))