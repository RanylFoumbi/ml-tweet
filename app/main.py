import signal
import sys
from flask import Flask, request, jsonify
from controllers.tweet import TweetController
from train_model_once import train_model_once
from services.scheduler import Scheduler
import threading
import logging

app = Flask(__name__)
scheduler_thread = None
scheduler = Scheduler()

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

def graceful_shutdown(_, __):
    logger.info("Graceful shutdown initiated...")
    if scheduler_thread:
        logger.info("Stopping scheduler thread...")
        scheduler.stop_schedule()
        scheduler_thread.join()
    logger.info("App is shutting down...")
    sys.exit(0)
    
if __name__ == "__main__":
    try:
        train_model_once()

        scheduler_thread = threading.Thread(target=scheduler.start_scheduler)
        scheduler_thread.start()

        signal.signal(signal.SIGINT, graceful_shutdown)

        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Failed to start the application: {e}")