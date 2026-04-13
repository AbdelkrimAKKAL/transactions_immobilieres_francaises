import pandas as pd
from sqlalchemy import create_engine
import logging
from src.database.connection import engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_to_db(df: pd.DataFrame, table_name: str = 'transactions', if_exists: str = 'append'):
    """
    Charge le dataframe Pandas dans la base de données (MySQL ou SQLite).
    """
    if engine is None:
        logging.error("Impossible de se connecter à la base de données. Chargement annulé.")
        return False
        
    logging.info(f"Chargement de {len(df)} lignes dans la table '{table_name}'...")
    
    try:
        # Optimisation possible en chunks pour les gros datasets
        df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False, chunksize=10000)
        logging.info("Chargement en base de données réussi.")
        return True
    except Exception as e:
        logging.error(f"Erreur lors du chargement : {e}")
        return False

if __name__ == "__main__":
    pass
