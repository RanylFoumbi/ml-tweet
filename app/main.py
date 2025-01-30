from flask import Flask, request, jsonify
from controllers.tweet import TweetController
from services.scheduler import Scheduler
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/predict", methods=['POST'])
def predict():
    try:
        tweets = request.get_json()
        if not tweets:
            raise ValueError("No tweets provided")

        controller = TweetController()
        results = controller.predict_sentiment(tweets)

        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Error during tweet prediction: {e}")
        return jsonify({"message": f"Erreur lors de l'insertion des tweets : {e}"}), 400
    
if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Failed to start the application: {e}")