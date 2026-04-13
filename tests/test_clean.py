import pytest
import pandas as pd
from src.transformation.clean import clean_dvf_data

def test_clean_dvf_data_removes_nulls():
    # Arrange
    raw_data = pd.DataFrame({
        'valeur_fonciere': [150000, None, 200000, 500],
        'surface_reelle_bati': [50, 40, None, 10],
        'code_commune': ['75056', '75056', '75056', '75056'],
        'date_mutation': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
    })
    
    # Act
    cleaned_df = clean_dvf_data(raw_data)
    
    # Assert
    # On s'attend à garder seulement la 1ère ligne (150000€, 50m²)
    # - Ligne 2 : valeur_fonciere None -> Supprimée
    # - Ligne 3 : surface_reelle_bati None -> Supprimée
    # - Ligne 4 : valeur_fonciere < 1000 -> Supprimée
    assert len(cleaned_df) == 1
    assert cleaned_df.iloc[0]['valeur_fonciere'] == 150000

def test_clean_dvf_data_handles_commas():
    # Arrange
    raw_data = pd.DataFrame({
        'valeur_fonciere': ['150000,50', 200000],
        'surface_reelle_bati': [50, 100],
        'code_commune': ['75056', '75056'],
        'date_mutation': ['2023-01-01', '2023-01-02']
    })
    
    # Act
    cleaned_df = clean_dvf_data(raw_data)
    
    # Assert
    assert cleaned_df.iloc[0]['valeur_fonciere'] == 150000.50
    assert cleaned_df['valeur_fonciere'].dtype == float
