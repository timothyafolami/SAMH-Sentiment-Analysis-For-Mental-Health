import os
import sys
import pandas as pd
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging_config.logger_config import get_logger

# Get the logger
logger = get_logger(__name__)

def load_data(file_path):
    logger.info(f"Loading data from {file_path}")
    return pd.read_csv(file_path)

def train_model(data):
    logger.info("Starting model training...")
    # check for missing values
    if data.isnull().sum().sum() > 0:
        logger.error("Missing values found in the dataset.")
        # Drop missing values
        data.dropna(inplace=True)
        logger.info("Missing values dropped.")
        # checking the shape of the data
        logger.info(f"Data shape: {data.shape}")
    
    # Split data into features and labels
    X = data['cleaned_statement']
    y = data['status']  # Assuming 'sentiment' is the target column
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create a pipeline with TF-IDF Vectorizer and Logistic Regression
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ])
    
    # Train the pipeline
    pipeline.fit(X_train, y_train)
    logger.info("Model training completed.")
    
    # Make predictions
    y_pred = pipeline.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    logger.info(f"Accuracy: {accuracy}")
    logger.info(f"Classification Report:\n{report}")
    
    return pipeline, accuracy, report

def save_model(pipeline, version):
    # Create the models directory if it doesn't exist
    os.makedirs('./models', exist_ok=True)
    
    # Save the pipeline with versioning
    model_filename = f'model_v{version}.joblib'
    model_path = os.path.join('models', model_filename)
    joblib.dump(pipeline, model_path)
    logger.info(f"Model saved as {model_path}")

if __name__ == "__main__":
    # Path to the cleaned dataset
    cleaned_data_path = os.path.join('./data', 'cleaned_data.csv')
    
    # Load the data
    data = load_data(cleaned_data_path)
    
    # Train the model
    pipeline, accuracy, report = train_model(data)
    
    # Define the model version based on the current datetime
    version = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Save the model
    save_model(pipeline, version)
    
    # Print the results
    print(f"Model version: {version}")
    print(f"Accuracy: {accuracy}")
    print(f"Classification Report:\n{report}")
