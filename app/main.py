from wsgiref import validate
from flask import Flask, request
from app.controllers.tweet import TweetController
from app.models.tweet import Tweet

app = Flask(__name__)

@app.route("/predict", methods=['POST'])
def main():
    try:
        tweets = request.get_json()
        controller = TweetController()
        controller.insert_tweet(tweets)
        results = controller.read_training_data()

        return results.to_json(orient='records'), 200
    except Exception as e:
        return {"message": f"Erreur lors de l'insertion des tweets : {e}"}, 400
