import os
import requests
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/"
RAW_DATA_DIR = Path("data/raw")

def download_dvf_data(year=2023):
    """
    Télécharge les données DVF complètes pour une année donnée
    depuis data.gouv.fr et les sauvegarde dans le dossier raw/.
    """
    url = f"{BASE_URL}{year}/full.csv.gz"
    
    # Créer le répertoire s'il n'existe pas
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    target_path = RAW_DATA_DIR / f"dvf_{year}.csv.gz"
    
    logging.info(f"Début du téléchargement DVF pour l'année {year}...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(target_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        logging.info(f"Téléchargement terminé : {target_path} - Taille: {os.path.getsize(target_path) / (1024 * 1024):.2f} MB")
        return target_path
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors du téléchargement : {e}")
        return None

if __name__ == "__main__":
    download_dvf_data(2023)
