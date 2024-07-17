from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model_pipeline.model_predict import load_model, predict
from logging_config.logger_config import get_logger

# Initialize the FastAPI app
app = FastAPI()

# Initialize the logger
logger = get_logger(__name__)

# Load the latest model at startup
model = load_model()

# Define the input data model
class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    """
    Home endpoint that provides basic information about the app.
    """
    logger.info("Home endpoint accessed.")
    return {"message": "Welcome to the Sentiment Analysis API. Use /predict_sentiment to get predictions."}

@app.get("/health")
def health_check():
    """
    Health check endpoint to ensure the app is running correctly.
    """
    logger.info("Health check endpoint accessed.")
    return {"status": "ok"}

@app.post("/predict_sentiment")
def predict_sentiment(input_data: TextInput):
    """
    Endpoint to predict the sentiment of the input text.
    """
    logger.info(f"Prediction request received with text: {input_data.text}")
    prediction = predict(input_data.text, model)
    logger.info(f"Prediction result: {prediction}")
    return {"text": input_data.text, "prediction": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
