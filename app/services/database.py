import mysql.connector
from mysql.connector import Error
import os
import pandas as pd

from models.tweet import Tweet
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatabaseService:
    def __init__(self):
        self.host = 'localhost'
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
    
    def create_database(self):

        engine = create_engine(f"mysql+mysqlconnector://{self.user}:{self.password}@localhost/")
        try:
            with engine.connect() as conn:
                conn.execute(text("CREATE DATABASE IF NOT EXISTS machine_learning"))
                conn.execute(text("USE machine_learning"))
                
                create_table_query = text("""
                CREATE TABLE IF NOT EXISTS tweets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text TEXT,
                    positive TINYINT,
                    negative TINYINT
                )
                """)
                
                conn.execute(create_table_query)
                conn.commit()  
            
        except Exception as e:
            print(f"Error creating database: {e}")

    
    def insert_first_data(self):
        query = """
        INSERT INTO tweets (id, TEXT, positive, negative) VALUES
            (1, "J'adore cette journée, tout se passe si bien !", 1, 0),
            (2, "Je suis tellement fatigué de tout ça, c'est nul...", 0, 1),
            (3, "Ce repas était incroyable, bravo au chef !", 1, 0),
            (4, "Encore une fois, tout le monde m'a déçu...", 0, 1),
            (5, "Le soleil brille, c'est parfait pour une promenade", 1, 0),
            (6, "Rien ne va aujourd'hui, tout est horrible !", 0, 1),
            (7, "Je suis tellement fier de mes progrès !", 1, 0),
            (8, "Pourquoi est-ce toujours aussi compliqué ?", 0, 1),
            (9, "Félicitations à tous pour ce succès incroyable !", 1, 0),
            (10, "C'est vraiment frustrant, rien ne fonctionne...", 0, 1);
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except Error as e:
            print(f"Erreur d'insertion : {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    

    def insert_tweet(self, tweet: Tweet):
        print(f"Insertion du tweet {tweet.text}")
        query = """
        INSERT INTO tweets (text, positive, negative) 
        VALUES (%s, %s, %s)
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()
            values = (tweet.text, tweet.positive, tweet.negative)
            cursor.execute(query, values)
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