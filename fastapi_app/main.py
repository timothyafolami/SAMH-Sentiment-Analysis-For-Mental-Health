from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os, sys

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model_pipeline.model_predict import load_model, predict as initial_predict
from llama_pipeline.llama_predict import predict as llama_predict
from db_connection import insert_db
from logging_config.logger_config import get_logger

# Initialize the FastAPI app
app = FastAPI()

# Initialize the logger
logger = get_logger(__name__)

# Load the latest model at startup
model = load_model()

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

class TextInput(BaseModel):
    text: str

class PredictionInput(BaseModel):
    text: str
    initial_prediction: str
    llama_category: str
    llama_explanation: str
    user_rating: int

@app.post("/predict_sentiment")
def predict_sentiment(input_data: TextInput):
    logger.info(f"Prediction request received with text: {input_data.text}")
    
    # Initial model prediction
    initial_prediction = initial_predict(input_data.text, model = model)
    
    # LLaMA 3 prediction
    llama_prediction = llama_predict(input_data.text)
    
    # Prepare response
    response = {
        "text": input_data.text,
        "initial_prediction": initial_prediction,
        "llama_category": llama_prediction['Category'],
        "llama_explanation": llama_prediction['Explanation']
    }
    
    logger.info(f"Prediction response: {response}")
    return response

@app.post("/submit_interaction")
def submit_interaction(data: PredictionInput):
    logger.info(f"Received interaction data: {data}")
    logger.info(f"Received text: {data.text}")
    logger.info(f"Received initial_prediction: {data.initial_prediction}")
    logger.info(f"Received llama_category: {data.llama_category}")
    logger.info(f"Received llama_explanation: {data.llama_explanation}")
    logger.info(f"Received user_rating: {data.user_rating}")

    interaction_data = {
        "Input_text": data.text,
        "Model_prediction": data.initial_prediction,
        "Llama_3_Prediction": data.llama_category,
        "Llama_3_Explanation": data.llama_explanation,
        "User Rating": data.user_rating,
    }
    
    response = insert_db(interaction_data)
    logger.info(f"Database response: {response}")
    return {"status": "success", "response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
