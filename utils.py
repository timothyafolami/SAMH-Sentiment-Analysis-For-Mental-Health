import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

# Download necessary NLTK data files
nltk.download('stopwords')
nltk.download('wordnet')

# Custom transformer for text preprocessing
class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def preprocess_text(self, text):
        # Lowercase the text
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Tokenize the text
        words = text.split()
        
        # Remove stopwords and apply lemmatization
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        
        # Join words back into a single string
        cleaned_text = ' '.join(words)
        
        return cleaned_text
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return [self.preprocess_text(text) for text in X]
    

# Model pipeline
pipeline = Pipeline([
    ('preprocessor', TextPreprocessor()),
    ('vectorizer', TfidfVectorizer()),
    ('classifier', RandomForestClassifier())
])

