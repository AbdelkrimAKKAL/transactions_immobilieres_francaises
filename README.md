# 🏢 DVF Market Intelligence (Data Engineering & Analytics) — Immobilier Français

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/ETL-Pandas-green.svg)](https://pandas.pydata.org/)

## ![Summary](https://img.shields.io/badge/-Résumé_Exécutif-333?style=for-the-badge&logo=readme&logoColor=white)

Ce projet déploie un pipeline de **Data Engineering** de bout en bout pour traiter et analyser les données massives des transactions immobilières françaises (DVF). Le système assure l'extraction de plus de **3 millions de données brutes**, leur nettoyage automatisé et leur stockage dans une base **SQLite optimisée** pour le Cloud. Un dashboard interactif permet d'explorer les prix au m² et les volumes de ventes à travers toute la France avec une fluidité totale.

---

## ![Business](https://img.shields.io/badge/-Problématique_Business-333?style=for-the-badge&logo=target&logoColor=white)

L'accès aux données immobilières en France est public (data.gouv.fr), mais leur exploitation brute est complexe en raison de leur volume et de leur hétérogénéité. L'enjeu de ce projet est triple :
1.  **Industrialisation des données** : Transformer des fichiers CSV massifs en une base de données relationnelle structurée.
2.  **Transparence du Marché** : Permettre une analyse précise du prix au m² par département et par type de bien (Maison vs Appartement).
3.  **Portabilité & Cloud** : Migrer d'une architecture lourde (MySQL) vers une solution **SQLite légère** pour un hébergement gratuit et performant sur Streamlit Cloud.

---

## ![Impact](https://img.shields.io/badge/-Résultats_&_Impact-333?style=for-the-badge&logo=chart-line&logoColor=white)

Le pipeline ETL a permis de raffiner le dataset pour ne garder que la donnée à haute valeur ajoutée :

| Métrique | Données Brutes | Données Nettoyées (Prod) | Impact |
| :--- | :---: | :---: | :---: |
| **Volume de lignes** | 3 140 000 | **1 029 498** | -67% de bruit supprimé |
| **Temps de chargement** | Plusieurs minutes | **< 2 secondes** | Dashboard instantané |
| **Taille Base de Données** | ~600 Mo (CSV) | **99.8 Mo (SQLite)** | Stockage optimisé Cloud |

**Insights Clés :**
* **Qualité des données** : Suppression automatique des transactions aberrantes (prix < 1000€ ou surface < 5m²).
* **Expertise Métier** : Calcul dynamique du prix au m² pondéré par le type de local et le nombre de pièces.
* **Accessibilité** : Dashboard public accessible 24/7 avec une architecture "Zero-Server".

---

## ![Pipeline](https://img.shields.io/badge/-Méthodologie_&_Pipeline-333?style=for-the-badge&logo=git&logoColor=white)

1.  **Ingestion par Chunks** : Lecture du fichier CSV par blocs de 100 000 lignes avec **Pandas** pour éviter la saturation de la RAM.
2.  **ETL & Nettoyage** : 
    * Normalisation des types de données et gestion des valeurs manquantes.
    * Filtrage strict pour ne conserver que les ventes immobilières réelles (exclusion des échanges et donations).
3.  **Stockage & Migration** : Transition réussie de MySQL vers **SQLite** pour une portabilité totale du projet sur GitHub.
4.  **Visualisation** : Développement d'une UI premium sur **Streamlit** exploitant Plotly pour des graphiques multidimensionnels.

---

## ![Stack](https://img.shields.io/badge/-Skills_&_Stack_Technique-333?style=for-the-badge&logo=python&logoColor=white)

* **Langages & Libs** : Python (Pandas, Numpy, SQLAlchemy).
* **Base de données** : **SQLite** (Architecture portable).
* **Data Viz** : Streamlit

---

## ![Next](https://img.shields.io/badge/-Prochaines_Étapes_&_Limites-333?style=for-the-badge&logo=rocket&logoColor=white)

* **Géolocalisation** : Intégration de cartes Mapbox détaillées à l'échelle de la rue.
* **Machine Learning** : Prédire l'évolution des prix au m² pour 2026 via des modèles de séries temporelles.
* **Limites** : Le dataset dépend de la fréquence de mise à jour de data.gouv.fr (tous les 6 mois).

---

## ![Install](https://img.shields.io/badge/-Installation_et_Utilisation-333?style=for-the-badge&logo=terminal&logoColor=white)

```bash
# Installation
git clone https://github.com/AbdelkrimAKKAL/transactions_immobilieres_francaises.git
cd transactions_immobilieres_francaises
pip install -r requirements.txt

# Lancer le Dashboard localement
streamlit run dashboard/app.py
```
