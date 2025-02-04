import threading
import schedule
import time
from services.database import DatabaseService
from services.model import ModelBuilder

class Scheduler: 
    def __init__(self):
        self.__stop_event = threading.Event()
        self.__scheduler_thread = None

    def train_model_job(self):
        db_service = DatabaseService()
        data = db_service.read_training_data()
        model_builder = ModelBuilder()
        model_builder.train_model(data)

    def stop_schedule(self):
        self.__stop_event.set()
        if self.__scheduler_thread and self.__scheduler_thread.is_alive():
            self.__scheduler_thread.join()

    def start_scheduler(self):
        schedule.every().week.do(self.train_model_job)

        self.__scheduler_thread = threading.Thread(target=self.__run_scheduler)
        self.__scheduler_thread.start()

    def __run_scheduler(self):
        while not self.__stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)
