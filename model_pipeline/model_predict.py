import os
import sys
import re
import string
import joblib
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from glob import glob

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logging_config.logger_config import get_logger

# Download necessary NLTK data files
nltk.download('stopwords')
nltk.download('wordnet')

# Get the logger
logger = get_logger(__name__)

# Custom Preprocessor Class
class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        logger.info("TextPreprocessor initialized.")
    
    def preprocess_text(self, text):
        logger.info(f"Original text: {text}")
        # Lowercase the text
        text = text.lower()
        logger.info(f"Lowercased text: {text}")
        
        # Remove punctuation
        text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
        logger.info(f"Text after punctuation removal: {text}")
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        logger.info(f"Text after number removal: {text}")
        
        # Tokenize the text
        words = text.split()
        logger.info(f"Tokenized text: {words}")
        
        # Remove stopwords and apply lemmatization
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        logger.info(f"Text after stopword removal and lemmatization: {words}")
        
        # Join words back into a single string
        cleaned_text = ' '.join(words)
        logger.info(f"Cleaned text: {cleaned_text}")
        
        return cleaned_text

def get_latest_model_path(models_dir='./models'):
    model_files = glob(os.path.join(models_dir, 'model_v*.joblib'))
    if not model_files:
        logger.error("No model files found in the models directory.")
        raise FileNotFoundError("No model files found in the models directory.")
    
    latest_model_file = max(model_files, key=os.path.getctime)
    logger.info(f"Latest model file found: {latest_model_file}")
    return latest_model_file

def load_model():
    model_path = get_latest_model_path()
    logger.info(f"Loading model from {model_path}")
    return joblib.load(model_path)

def predict(text, model):
    # Initialize the text preprocessor
    preprocessor = TextPreprocessor()
    
    # Preprocess the input text
    logger.info("Preprocessing input text...")
    cleaned_text = preprocessor.preprocess_text(text)
    
    # Make a prediction
    logger.info("Making prediction...")
    prediction = model.predict([cleaned_text])
    
    logger.info(f"Prediction: {prediction}")
    return prediction[0]

if __name__ == "__main__":
    # Example text input
    example_text = "I love programming in Python."
    
    # Load the latest model
    model = load_model()
    
    # Make a prediction
    prediction = predict(example_text, model)
    
    # Print the prediction
    print(f"Prediction: {prediction}")
