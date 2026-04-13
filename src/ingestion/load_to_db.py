import pandas as pd
import logging
import time
import sys
import os
from pathlib import Path

# Ajouter le dossier racine au chemin pour permettre d'importer le dossier src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importer la connexion centralisée (MySQL/SQLite)
from src.database.connection import engine, DB_URL

def ensure_data_dir():
    """Assure que le dossier pour la base SQLite existe si nécessaire."""
    if DB_URL.startswith("sqlite:///"):
        # Extraire le chemin du fichier (ex: data/dvf_data.db)
        db_path = DB_URL.replace("sqlite:///", "")
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            logging.info(f"Dossier de base de données vérifié : {db_dir}")

# Importer votre script de nettoyage
from src.transformation.clean import clean_dvf_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

FILE_PATH = "data/dvf_2023.csv"
CHUNK_SIZE = 100000  # On lit 100 000 lignes à la fois pour ne pas faire exploser la RAM

def clean_and_load_data():
    ensure_data_dir()
    
    if not Path(FILE_PATH).exists():
        logging.error(f"Fichier introuvable : {FILE_PATH}. Avez-vous lancé download.py ?")
        return

    logging.info(f"Début de l'ingestion vers {DB_URL}...")
    start_time = time.time()
    
    # 1. On ne sélectionne QUE les colonnes qui nous intéressent (pour aller plus vite)
    cols_to_use = [
        'id_mutation', 'date_mutation', 'nature_mutation', 'valeur_fonciere',
        'code_postal', 'code_commune', 'nom_commune', 'code_departement', 
        'type_local', 'surface_reelle_bati', 'nombre_pieces_principales',
        'longitude', 'latitude'
    ]

    total_inserted = 0

    # 2. Lecture en continu de gros morceaux du fichier (100k par tranche)
    # pandas.read_csv permet de le lire directement ! (compression='infer' détecte automatiquement si c'est .csv ou .gz)
    for chunk in pd.read_csv(FILE_PATH, compression='infer', sep=',', usecols=cols_to_use, chunksize=CHUNK_SIZE, low_memory=False):
        
        # --- PHASE DE NETTOYAGE (TRANSFORM) ---
        
        # Garder seulement les Ventes (souvent on ne veut que ça, excluant les Echanges)
        chunk = chunk[chunk['nature_mutation'] == 'Vente']
        chunk = chunk.drop(columns=['nature_mutation'])
        
        # Appliquer VOTRE fonction de nettoyage (clean.py)
        chunk = clean_dvf_data(chunk)
        
        # --- PHASE D'INJECTION (LOAD) ---
        
        # L'avantage incroyable de pandas, c'est la fonction .to_sql
        # Ça prend notre bloc nettoyé et ça l'injecte d'un coup dans la table 'transactions' MySQL
        chunk.to_sql(name='transactions', con=engine, if_exists='append', index=False)
        
        total_inserted += len(chunk)
        logging.info(f"-> {total_inserted} ventes immobilières propres injectées...")
        
    logging.info(f"✅ Terminé ! Un total de {total_inserted} transactions chargées en {int(time.time() - start_time)} secondes.")

if __name__ == "__main__":
    clean_and_load_data()
