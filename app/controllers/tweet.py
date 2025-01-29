
from services.model import ModelBuilder
from models.tweet import Tweet

from services.database import DatabaseService


class TweetController:
    def __init__(self):
       pass

    def predict_sentiment(self, tweets):
        model = ModelBuilder()
        results = {}
        if isinstance(tweets, list):
            for index, tweet in enumerate(tweets):
                result = model.predict_sentiment(tweet)
                results[f"tweet{index}"] = result
        return results