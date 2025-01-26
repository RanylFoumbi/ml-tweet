from wsgiref import validate
from flask import Flask, request
from controllers.tweet import TweetController
from models.tweet import Tweet

app = Flask(__name__)

@app.route("/predict", methods=['POST'])
# @validate()
def main(body=[Tweet]):
    # payload = request.json
    print(f"Payload is {body}")
    controller = TweetController()
    controller.insert_tweet(body)
    results = controller.read_training_data()

    return results.to_json()
