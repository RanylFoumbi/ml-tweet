from services.database import DatabaseService
from services.model import ModelBuilder


def train_model_once():
    db_service = DatabaseService()
    data = db_service.read_training_data()
    model_builder = ModelBuilder()
    model_builder.train_model(data)