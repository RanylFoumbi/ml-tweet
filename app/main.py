from flask import Flask
from services import database

app = Flask(__name__)

@app.get("/predict")
def main():
    db = database.DatabaseManager()
    df = db.read_training_data()
    return df.to_json()