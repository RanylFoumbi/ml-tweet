import logging
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text
from models.tweet import Tweet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    insertions = [
        ("J'adore cette journée, tout se passe si bien !", 1, 0),
        ("Je suis tellement fatigué de tout ça, c'est nul...", 0, 1),
        ("Ce repas était incroyable, bravo au chef !", 1, 0),
        ("Encore une fois, tout le monde m'a déçu...", 0, 1),
        ("Le soleil brille, c'est parfait pour une promenade", 1, 0),
        ("Rien ne va aujourd'hui, tout est horrible !", 0, 1),
        ("Je suis tellement fier de mes progrès !", 1, 0),
        ("Pourquoi est-ce toujours aussi compliqué ?", 0, 1),
        ("Félicitations à tous pour ce succès incroyable !", 1, 0),
        ("C'est vraiment frustrant, rien ne fonctionne...", 0, 1),
        ("Je suis tellement heureux de te voir !", 1, 0),
        ("Je déteste quand ça arrive...", 0, 1),
        ("Quelle belle surprise, merci beaucoup !", 1, 0),
        ("Je suis tellement en colère contre toi !", 0, 1),
        ("C'est une journée magnifique !", 1, 0),
        ("Je suis tellement déprimé aujourd'hui...", 0, 1),
        ("Je suis ravi de ce résultat !", 1, 0),
        ("C'est une catastrophe totale...", 0, 1),
        ("Je suis tellement reconnaissant pour ton aide !", 1, 0),
        ("Je suis tellement frustré par cette situation...", 0, 1),
        ("C'est un jour merveilleux !", 1, 0),
        ("Je suis tellement déçu par ce résultat...", 0, 1),
        ("Je suis tellement content de ce que j'ai accompli !", 1, 0),
        ("C'est vraiment décevant...", 0, 1),
        ("Je suis tellement excité pour demain !", 1, 0),
        ("Je suis tellement fatigué de tout ça...", 0, 1),
        ("C'est une excellente nouvelle !", 1, 0),
        ("Je suis tellement en colère contre cette situation...", 0, 1),
        ("Je suis tellement heureux pour toi !", 1, 0),
        ("C'est vraiment frustrant...", 0, 1),
        ("Je suis tellement fier de toi !", 1, 0),
        ("Je suis tellement déçu par toi...", 0, 1),
        ("C'est une journée fantastique !", 1, 0),
        ("Je suis tellement triste aujourd'hui...", 0, 1),
        ("Je suis tellement reconnaissant pour tout ce que tu fais !", 1, 0),
        ("C'est vraiment déprimant...", 0, 1),
        ("Je suis tellement content de te voir !", 1, 0),
        ("Je suis tellement en colère contre toi...", 0, 1),
        ("C'est une journée merveilleuse !", 1, 0),
        ("Je suis tellement déprimé par cette situation...", 0, 1)
    ]
    
    def __init__(self):
        load_dotenv(override=True)
        self.host = os.getenv('MYSQL_HOST')
        self.port = os.getenv('MYSQL_PORT')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('MYSQL_ROOT_USER')
        self.password = os.getenv('MYSQL_ROOT_PASSWORD')
        self.engine = create_engine(f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}")
        logging.info(f"Host: {self.host}, Port: {self.port}, Database: {self.database}, User: {self.user}, Password: {self.password}")

    def create_database(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database}"))
                
                conn.execute(text(f"USE {self.database}"))

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
            logging.info(f"Error creating database: {e}")

    def insert_first_data(self):
        values_str = ', '.join([f"('{text.replace("'", "''")}', {positive}, {negative})" for text, positive, negative in self.insertions])
        query = f"""
        INSERT INTO tweets (text, positive, negative) VALUES
            {values_str};
        """
        try:
            with self.engine.begin() as conn:
                conn.execute(text(f"USE {self.database}"))
                conn.execute(text(query))
            logging.info("Database initialized successfully!")
        except Exception as e:
            logging.info(f"Error inserting data: {e}")
    
    def insert_tweet(self, tweet: Tweet):
        print(f"Inserting tweet: {tweet.text}")
        query = """
        INSERT INTO tweets (text, positive, negative) 
        VALUES (:text, :positive, :negative)
        """
        try:
            with self.engine.begin() as conn:
                conn.execute(text(f"USE {self.database}"))
                conn.execute(text(query), {'text': tweet.text, 'positive': tweet.positive, 'negative': tweet.negative})
            logging.info("Tweet inserted successfully!")
        except Exception as e:
            logging.info(f"Error inserting tweet: {e}")

    def read_training_data(self):
        query = "SELECT text, positive, negative FROM tweets"
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"USE {self.database}"))
                df = pd.read_sql(query, conn)
                return df
        except Exception as e:
            logging.info(f"Error loading data: {e}")