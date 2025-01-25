import mysql.connector
from mysql.connector import Error
import os
import pandas as pd

class DatabaseManager:
    def __init__(self):
        self.host = 'localhost:4000'
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')

    def connect(self):
        try:
            print(f"Connexion à la base de données {self.host}")
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except Error as e:
            print(f"Erreur de connexion : {e}")
            return None

    def insert_tweet(self, text, positive, negative):
        query = """
        INSERT INTO tweets (text, positive, negative) 
        VALUES (%s, %s, %s)
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(query, (text, positive, negative))
            connection.commit()
        except Error as e:
            print(f"Erreur d'insertion : {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def read_training_data(self):
        query = "SELECT text, positive, negative FROM tweets"
        try:
            connection = self.connect()
            df = pd.read_sql(query, connection)
            return df
        except Error as e:
            print(f"Erreur de chargement : {e}")
        finally:
            if connection.is_connected():
                connection.close()