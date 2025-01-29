import threading
import schedule
import time
from services.database import DatabaseService
from services.model import ModelBuilder

class Scheduler: 
    
    def __init__(self):
        self.__stop_event = threading.Event()

    def train_model_job(self):
        db_service = DatabaseService()
        data = db_service.read_training_data()
        model_builder = ModelBuilder()
        model_builder.train_model(data)
        print("Model trained and saved successfully.")
        
    def stop_schedule(self):
        self.__stop_event.set()
        
    def start_scheduler(self):
        schedule.every().week.do(self.train_model_job)

        while not self.__stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)