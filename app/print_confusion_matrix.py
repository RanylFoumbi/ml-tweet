import logging
from sklearn.metrics import confusion_matrix
from tabulate import tabulate
import pandas as pd

from services.database import DatabaseService
from services.model import ModelBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_confusion_matrix():
    modelBuilder = ModelBuilder()
    positive_model, negative_model, vectorizer = modelBuilder.load_models()
    
    data = {
    'text': [
        "J'adore cette journée, tout se passe si bien !",
        "Je suis tellement fatigué de tout ça, c'est nul...",
        "Ce repas était incroyable, bravo au chef !",
        "Encore une fois, tout le monde m'a déçu...",
        "Le soleil brille, c'est parfait pour une promenade",
        "Rien ne va aujourd'hui, tout est horrible !",
        "Je suis tellement fier de mes progrès !",
        "Pourquoi est-ce toujours aussi compliqué ?",
        "Félicitations à tous pour ce succès incroyable !",
        "C'est vraiment frustrant, rien ne fonctionne...",
        "Je suis tellement heureux de te voir !",
        "Je déteste quand ça arrive...",
        "Quelle belle surprise, merci beaucoup !",
        "Je suis tellement en colère contre toi !",
        "C'est une journée magnifique !",
        "Je suis tellement déprimé aujourd'hui...",
        "Je suis ravi de ce résultat !",
        "C'est une catastrophe totale...",
        "Je suis tellement reconnaissant pour ton aide !",
        "Je suis vraiment en forme ce matin !"
        ],
        'positive': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        'negative': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
    }

    test_data = pd.DataFrame(data)
    
    test_data['text'] = test_data['text'].apply(modelBuilder.clean_text)
    X_test = vectorizer.transform(test_data['text'])
    
    y_test_positive = test_data['positive'].values
    y_test_negative = test_data['negative'].values
    
    y_pred_positive = positive_model.predict(X_test)
    y_pred_negative = negative_model.predict(X_test)
    
    cm_positive = confusion_matrix(y_test_positive, y_pred_positive)
    cm_negative = confusion_matrix(y_test_negative, y_pred_negative)
    
    logger.info("Positive confusion matrix")
    print(cm_positive)
    print(tabulate(cm_positive, headers='keys', tablefmt='psql'))

    logger.info("Negative confusion matrix")
    print(tabulate(cm_negative, headers='keys', tablefmt='psql'))

get_confusion_matrix()