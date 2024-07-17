#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Data Ingestion
echo "Running data ingestion..."
python data_pipeline/data_ingestion.py

# Step 2: Data Preprocessing
echo "Running data preprocessing..."
python data_pipeline/data_preprocessor.py

# Step 3: Model Training
echo "Running model training..."
python model_pipeline/model_trainer.py

# Step 4: Run FastAPI App
echo "Starting FastAPI app..."
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000
