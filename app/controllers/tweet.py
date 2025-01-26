
from app.models.tweet import Tweet

from app.services.database import DatabaseService


class TweetController:
    def __init__(self):
        self.database_service = DatabaseService()

    def insert_tweet(self, tweets):
            if isinstance(tweets, list):
                for tweet in tweets:
                    data = Tweet.model_validate(tweet)
                    self.database_service.insert_tweet(data)

    def read_training_data(self):   
        return self.database_service.read_training_data()