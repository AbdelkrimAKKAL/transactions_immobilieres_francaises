import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_dvf_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données brutes DVF:
    - Supprime les doublons
    - Gère les valeurs nulles (prix, surface, localisation)
    - Convertit les types (dates, floats, catégories)
    - Filtre les transactions aberrantes (prix < 1000€, surface < 5m²)
    """
    initial_rows = len(df)
    logging.info(f"Début du nettoyage - Lignes initiales : {initial_rows}")

    # 1. Suppression des doublons
    df = df.drop_duplicates()
    
    # 2. Gestion des valeurs nulles essentielles
    # On supprime les lignes où la valeur foncière ou la surface n'existe pas
    columns_to_check = ['valeur_fonciere', 'surface_reelle_bati', 'code_commune']
    df = df.dropna(subset=columns_to_check)
    
    # Remplacer les virgules par des points pour la valeur foncière et convertir en float
    if df['valeur_fonciere'].dtype == object:
        df['valeur_fonciere'] = df['valeur_fonciere'].astype(str).str.replace(',', '.').astype(float)
        
    df['surface_reelle_bati'] = df['surface_reelle_bati'].astype(float)

    # 3. Filtrage des valeurs aberrantes
    # On garde que les transactions pertinentes (prix >= 1000€ et surface >= 5m²)
    # Ce qui enlève beaucoup de petites dépendances/caves achetées séparément, etc.
    df = df[(df['valeur_fonciere'] >= 1000) & (df['surface_reelle_bati'] >= 5)]
    
    # 4. Conversion des types
    df['date_mutation'] = pd.to_datetime(df['date_mutation'], format='%Y-%m-%d', errors='coerce')
    df = df.dropna(subset=['date_mutation'])
    
    # 5. Calcul des logs
    final_rows = len(df)
    conservation_rate = (final_rows / initial_rows) * 100
    logging.info(f"Nettoyage terminé - Lignes conservées : {final_rows} ({conservation_rate:.2f}%)")
    
    return df

if __name__ == "__main__":
    pass
