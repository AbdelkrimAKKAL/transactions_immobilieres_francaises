import pandas as pd
from src.database.connection import engine

def get_prix_moyen_dept():
    """
    Calcule le prix moyen au m² et le volume des ventes par département.
    """
    query = """
        SELECT 
            code_departement, 
            AVG(valeur_fonciere / NULLIF(surface_reelle_bati, 0)) as prix_moyen_m2, 
            COUNT(*) as volume_ventes
        FROM transactions
        WHERE surface_reelle_bati > 0
        GROUP BY code_departement
        ORDER BY prix_moyen_m2 DESC;
    """
    df = pd.read_sql(query, engine)
    
    # Très important : transformer '1' en '01' pour que le graphique le lise comme une catégorie (texte) et pas comme un nombre
    df['code_departement'] = df['code_departement'].astype(str).str.zfill(2)
    return df

def get_ventes_mensuelles():
    """
    Saisonnalité : Calcule le volume de transactions par mois.
    Compatible MySQL et SQLite.
    """
    # Détection du dialecte
    dialect = engine.dialect.name
    
    if dialect == 'sqlite':
        # SQLite stocke les dates en string, on utilise strftime
        month_func = "CAST(strftime('%m', date_mutation) AS INTEGER)"
    else:
        # MySQL utilise MONTH()
        month_func = "MONTH(date_mutation)"

    query = f"""
        SELECT 
            {month_func} as mois, 
            COUNT(*) as volume_ventes
        FROM transactions
        GROUP BY {month_func}
        ORDER BY mois ASC;
    """
    df = pd.read_sql(query, engine)
    
    # Mapping stylisé des mois pour le dashboard
    mois_map = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin', 
                7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
    df['mois_nom'] = df['mois'].map(mois_map)
    
    return df

def get_top_communes():
    """
    Récupère le top 20 des communes les plus chères.
    """
    query = """
        SELECT 
            nom_commune as commune, 
            AVG(valeur_fonciere / NULLIF(surface_reelle_bati, 0)) as prix_moyen_m2
        FROM transactions
        WHERE surface_reelle_bati > 0
        GROUP BY nom_commune
        HAVING COUNT(*) > 50
        ORDER BY prix_moyen_m2 DESC
        LIMIT 20;
    """
    return pd.read_sql(query, engine)

def get_repartition_type_bien():
    """
    Récupère la répartition du volume des ventes par type de bien (Maison, Appartement, etc.).
    """
    query = """
        SELECT 
            COALESCE(NULLIF(type_local, ''), 'Autre') as type_bien,
            COUNT(*) as volume_ventes
        FROM transactions
        GROUP BY type_local
        ORDER BY volume_ventes DESC;
    """
    return pd.read_sql(query, engine)

def get_analyse_pieces():
    """
    Analyse les ventes par nombre de pièces principales (de 1 à 8 pièces max pour éviter les outliers).
    """
    query = """
        SELECT 
            nombre_pieces_principales,
            COUNT(*) as volume_ventes,
            AVG(valeur_fonciere / NULLIF(surface_reelle_bati, 0)) as prix_moyen_m2
        FROM transactions
        WHERE nombre_pieces_principales BETWEEN 1 AND 8
        AND surface_reelle_bati > 0
        GROUP BY nombre_pieces_principales
        ORDER BY nombre_pieces_principales ASC;
    """
    df = pd.read_sql(query, engine)
    # Conversion stylistique pour le graphique
    
    # Remplacer '1.0' par '1' etc si c'est un float venant de Pandas
    df['nombre_pieces_principales'] = df['nombre_pieces_principales'].astype(int).astype(str)
    
    # Ajouter un label propre
    df['label_pieces'] = df['nombre_pieces_principales'] + " Pièces"
    # Exception pour 1 pièce -> Studio/T1
    df.loc[df['nombre_pieces_principales'] == '1', 'label_pieces'] = 'Studio / T1'
    
    return df

