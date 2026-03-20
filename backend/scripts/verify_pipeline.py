# scripts/verify_pipeline.py
from data_pipeline.utils.db import get_db

def run_checks():
    db = get_db()
    col = db["articles"]

    total = col.count_documents({})
    print(f"\n=== NewsET Data Quality Report ===")
    print(f"Total articles: {total}")

    if total == 0:
        print("⚠ Database is empty — run the scheduler first.")
        return

    # Articles per category
    print("\nArticles per category:")
    pipeline = [{"$group": {"_id": "$category", "count": {"$sum": 1}}}]
    for result in col.aggregate(pipeline):
        print(f"  {result['_id']:15s}: {result['count']}")

    # Average word count
    pipeline = [{"$group": {"_id": None, "avg_words": {"$avg": "$word_count"}}}]
    result = list(col.aggregate(pipeline))
    if result:
        print(f"\nAverage article word count: {result[0]['avg_words']:.0f}")

    # Sample article
    sample = col.find_one({}, sort=[("fetched_at", -1)])
    if sample:
        print(f"\nLatest article:")
        print(f"  Title   : {sample['title']}")
        print(f"  Source  : {sample['source']}")
        print(f"  Category: {sample['category']}")
        print(f"  Words   : {sample['word_count']}")

    print("\n✓ Checks complete")

if __name__ == "__main__":
    run_checks()