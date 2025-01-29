
from services.model import ModelBuilder
class TweetController:
    def __init__(self):
       pass

    def predict_sentiment(self, tweets):
        model = ModelBuilder()
        results = {}
        if isinstance(tweets, list):
            for index, tweet in enumerate(tweets):
                result = model.predict_sentiment(tweet)
                results[f"tweet{index + 1}"] = result
        return results