
from services.model import ModelBuilder
class TweetController:
    def __init__(self):
       pass

    def predict_sentiment(self, tweets):
        model = ModelBuilder()
        if isinstance(tweets, list) and all(isinstance(tweet, str) for tweet in tweets):
            return model.predict_sentiment(tweets)
        else:
            raise ValueError("The tweet should be a list of string")