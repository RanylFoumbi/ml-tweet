import re
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

from services.database import DatabaseService
from models.tweet import Tweet

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
        
        model_positive = LogisticRegression(penalty=None, solver='newton-cg')
        model_positive.fit(X, y_positive)
        
        model_negative = LogisticRegression(penalty=None, solver='newton-cg')
        model_negative.fit(X, y_negative)
        
        os.makedirs('trained_models', exist_ok=True)
        
        with open('trained_models/logistic_model_positive.pkl', 'wb') as model_file:
            pickle.dump(model_positive, model_file)
        with open('trained_models/logistic_model_negative.pkl', 'wb') as model_file:
            pickle.dump(model_negative, model_file)
        with open('trained_models/vectorizer.pkl', 'wb') as vectorizer_file:
            pickle.dump(vectorizer, vectorizer_file)
            
    def load_models(self):
        with open('trained_models/logistic_model_positive.pkl', 'rb') as model_file:
            model_positive = pickle.load(model_file)
        with open('trained_models/logistic_model_negative.pkl', 'rb') as model_file:
            model_negative = pickle.load(model_file)
        with open('trained_models/vectorizer.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        return model_positive, model_negative, vectorizer

    def predict_sentiment(self, tweet: str):
        model_positive, model_negative, vectorizer = self.load_models()
        cleaned_tweet = self.clean_text(tweet)
        X = vectorizer.transform([cleaned_tweet])
        
        prob_positive = model_positive.predict_proba(X)[0][1]
        prob_negative = model_negative.predict_proba(X)[0][1]
        self.database_service.insert_tweet(Tweet(
            text=tweet,
            positive= 1 if prob_negative < prob_positive else 0,
            negative= 1 if prob_negative > prob_positive else 0
        ))
        
        avg_probability = (prob_positive + prob_negative) / 2
        return avg_probability