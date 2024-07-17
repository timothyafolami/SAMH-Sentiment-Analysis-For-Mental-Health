from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os, sys

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

# Mount the static files directory
app.mount("/static", StaticFiles(directory="fastapi_app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("fastapi_app/static/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "ok"}

@app.post("/predict_sentiment")
def predict_sentiment(input_data: TextInput):
    logger.info(f"Prediction request received with text: {input_data.text}")
    prediction = predict(input_data.text, model)
    logger.info(f"Prediction result: {prediction}")
    return {"text": input_data.text, "prediction": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
