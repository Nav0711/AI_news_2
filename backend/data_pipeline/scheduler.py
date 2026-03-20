# data-pipeline/scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from data_pipeline.fetchers.newsapi_fetchers import run_full_pipeline
from data_pipeline.utils.db import setup_indexes, ping


def main():
    # Create indexes on first run
    setup_indexes()

    # Initial bulk fetch — go 7 days back to seed the DB quickly
    print("Running initial seed fetch (7 days back)...")
    run_full_pipeline(days_back=7)

    # Then schedule incremental fetches every 30 minutes
    scheduler = BlockingScheduler()
    scheduler.add_job(
        func=lambda: run_full_pipeline(days_back=1),
        trigger="interval",
        minutes=30,
        id="news_fetch",
        name="Fetch latest news",
        replace_existing=True,
    )

    print("\n✓ Scheduler started. Fetching every 30 minutes. Press Ctrl+C to stop.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped.")

if __name__ == "__main__":
    main()