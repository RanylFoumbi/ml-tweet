import logging
from services.database import DatabaseService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    db_service = DatabaseService()
    db_service.create_database()
    db_service.insert_first_data()
    logging.info("Database initialized successfully!")
    
initialize_database()