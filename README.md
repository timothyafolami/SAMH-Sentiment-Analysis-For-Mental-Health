# Sentiment Analysis API
![alt text](image.png)

This project provides a sentiment analysis API using FastAPI and a machine learning model trained on textual data.

## Features

- Data ingestion and preprocessing
- Model training and saving
- FastAPI application for serving predictions
- Dockerized for easy deployment

## Setup

### Prerequisites

- Docker installed on your system

### Build and Run

1. Build the Docker image:

    ```bash
    docker build -t sentiment-analysis-api .
    ```

2. Run the Docker container:

    ```bash
    docker run -p 8000:8000 sentiment-analysis-api
    ```

3. Access the API:

    - Home: [http://localhost:8000](http://localhost:8000)
    - Health Check: [http://localhost:8000/health](http://localhost:8000/health)
    - Predict Sentiment: Use a POST request to [http://localhost:8000/predict_sentiment](http://localhost:8000/predict_sentiment) with a JSON body.

## Example cURL Command

```bash
curl -X POST "http://localhost:8000/predict_sentiment" -H "Content-Type: application/json" -d '{"text": "I love programming in Python."}'
