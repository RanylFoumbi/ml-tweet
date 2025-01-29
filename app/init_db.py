from services.database import DatabaseService


def initialize_database():
    db_service = DatabaseService()
    db_service.create_database()
    db_service.insert_first_data()