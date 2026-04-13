import pandas as pd
import numpy as np

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute de nouvelles variables (Feature Engineering) :
    - prix_m2 = valeur_fonciere / surface_reelle_bati
    - annee, mois = extrait de date_mutation
    - categorie_bien = Appartement / Maison / Terrain
    - region = mapping code_departement → région
    - price_segment = Bas / Moyen / Haut / Luxe (quartiles)
    """
    # 1. Calcul du prix au m²
    df['prix_m2'] = df['valeur_fonciere'] / df['surface_reelle_bati']
    
    # 2. Date extraction
    df['annee'] = df['date_mutation'].dt.year
    df['mois'] = df['date_mutation'].dt.month
    
    # 3. Catégorie de bien (simplification)
    # Dans les données DVF, il y a 'type_local'
    if 'type_local' in df.columns:
        df['categorie_bien'] = df['type_local'].fillna('Autre')
    else:
        df['categorie_bien'] = 'Inconnu'
        
    # 4. Région via mapping de code département
    # (Mapping très simplifié à titre d'exemple)
    idf_deps = ['75', '77', '78', '91', '92', '93', '94', '95']
    
    def map_region(dept):
        dept_str = str(dept).zfill(2)
        if dept_str in idf_deps:
            return 'Île-de-France'
        return 'Province'
        
    df['code_departement'] = df['code_departement'].astype(str).str.zfill(2)
    df['region'] = df['code_departement'].apply(map_region)
    
    # 5. Price segments (quartiles par année ou par région) national
    quartiles = df['prix_m2'].quantile([0.25, 0.5, 0.75])
    
    def price_segment(prix):
        if prix <= quartiles[0.25]: return 'Bas'
        elif prix <= quartiles[0.5]: return 'Moyen'
        elif prix <= quartiles[0.75]: return 'Haut'
        else: return 'Luxe'
        
    df['price_segment'] = df['prix_m2'].apply(price_segment)
    
    return df
