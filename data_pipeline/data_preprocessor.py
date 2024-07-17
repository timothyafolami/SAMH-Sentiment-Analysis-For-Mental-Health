import os
import sys
import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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
        # logger.info(f"Original text: {text}")
        # Lowercase the text
        text = text.lower()
        # logger.info(f"Lowercased text: {text}")
        
        # Remove punctuation
        text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
        # logger.info(f"Text after punctuation removal: {text}")
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        # logger.info(f"Text after number removal: {text}")
        
        # Tokenize the text
        words = text.split()
        # logger.info(f"Tokenized text: {words}")
        
        # Remove stopwords and apply lemmatization
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        # logger.info(f"Text after stopword removal and lemmatization: {words}")
        
        # Join words back into a single string
        cleaned_text = ' '.join(words)
        # logger.info(f"Cleaned text: {cleaned_text}")
        
        return cleaned_text

def load_and_preprocess_data(file_path):
    # Load the data
    logger.info(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    # dropping missing values
    logger.info("Dropping missing values")
    df.dropna(inplace=True)
    
    # Check if the necessary column exists
    if 'statement' not in df.columns:
        logger.error("The required column 'statement' is missing from the dataset.")
        return
    
    # Initialize the text preprocessor
    preprocessor = TextPreprocessor()
    
    # Apply the preprocessing to the 'statement' column
    logger.info("Starting text preprocessing...")
    df['cleaned_statement'] = df['statement'].apply(preprocessor.preprocess_text)
    logger.info("Text preprocessing completed.")
    
    # Save the cleaned data to a new CSV file
    cleaned_file_path = os.path.join('./data', 'cleaned_data.csv')
    df.to_csv(cleaned_file_path, index=False)
    logger.info(f"Cleaned data saved to {cleaned_file_path}")

if __name__ == "__main__":
    # Path to the downloaded dataset
    dataset_path = os.path.join("./data", "Combined_Data.csv")
    
    # Preprocess the data
    load_and_preprocess_data(dataset_path)
