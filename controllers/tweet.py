
from models.tweet import Tweet
from services.database import DatabaseService
from pydantic_core import from_json


class TweetController:
    def __init__(self):
        self.database_service = DatabaseService()

    def insert_tweet(self, tweets):
        if isinstance(tweets, list):
            for tweet in tweets:
                data = Tweet(tweet)
                self.database_service.insert_tweet(data)

    def read_training_data(self):   
        return self.database_service.read_training_data()