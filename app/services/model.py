import logging
import re
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

from services.database import DatabaseService
from models.tweet import Tweet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelBuilder:
    
    def __init__(self):
        self.database_service = DatabaseService()
    
    def clean_text(self, text):    
        text = text.lower()   
        text = re.sub(r'[^\w\s]', '', text)   
        return text
    
    def train_model(self, data: pd.DataFrame):
        data['text'] = data['text'].apply(self.clean_text)
        
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(data['text'])
        
        y_positive = data['positive'].values
        y_negative = data['negative'].values
        
        positive_model = LogisticRegression(penalty=None, solver='newton-cg')
        positive_model.fit(X, y_positive)
        
        negative_model = LogisticRegression(penalty=None, solver='newton-cg')
        negative_model.fit(X, y_negative)
        
        os.makedirs('trained_models', exist_ok=True)
        
        with open('trained_models/logistic_model_positive.pkl', 'wb') as model_file:
            pickle.dump(positive_model, model_file)
        with open('trained_models/logistic_model_negative.pkl', 'wb') as model_file:
            pickle.dump(negative_model, model_file)
        with open('trained_models/vectorizer.pkl', 'wb') as vectorizer_file:
            pickle.dump(vectorizer, vectorizer_file)
        
        logger.info("Model trained and saved successfully.")
            
    def load_models(self):
        with open('trained_models/logistic_model_positive.pkl', 'rb') as model_file:
            positive_model = pickle.load(model_file)
        with open('trained_models/logistic_model_negative.pkl', 'rb') as model_file:
            negative_model = pickle.load(model_file)
        with open('trained_models/vectorizer.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        return positive_model, negative_model, vectorizer

    def predict_sentiment(self, tweets: list):
        positive_model, negative_model, vectorizer = self.load_models()
        cleaned_tweets = [self.clean_text(tweet) for tweet in tweets]
        X = vectorizer.transform(cleaned_tweets)
        
        prob_positive = positive_model.predict_proba(X)
        prob_negative = negative_model.predict_proba(X)
        
        results = {}
        for idx, tweet in enumerate(tweets):
            positive_percentage = (prob_positive[idx][1] + prob_negative[idx][0]) / 2
            negative_percentage = (prob_negative[idx][1] + prob_positive[idx][0]) / 2
            
            if positive_percentage > negative_percentage:
                results[f"tweet{idx + 1}"] = round(positive_percentage, 1)
                self.insert_tweet(tweet, 1, 0)
            elif positive_percentage < negative_percentage:
                results[f"tweet{idx + 1}"] = round(negative_percentage * -1, 1)
                self.insert_tweet(tweet, 0, 1)
            else:
                results[f"tweet{idx + 1}"] = 0.0
                self.insert_tweet(tweet, 0, 0)
        
        return results
    
    def insert_tweet(self, text: str, positive: int, negative: int):
        self.database_service.insert_tweet(
            Tweet(
            text=text,
            positive= positive,
            negative= negative
        ))