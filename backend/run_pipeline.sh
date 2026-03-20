#!/bin/bash
# Run the AI News data pipeline
cd "$(dirname "$0")"
source venv/bin/activate
python3 -m data_pipeline.scheduler
