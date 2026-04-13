# 🏢 DVF Market Intelligence - Data Engineering Pipeline

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite%20%2F%20MySQL-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-ETL-green.svg)

## 📌 Présentation du Projet
Ce projet est un pipeline de bout-en-bout conçu pour traiter les données massives de l'immobilier français (**Demande de Valeur Foncière**). Il démontre une architecture complète allant de l'extraction brute jusqu'à la visualisation interactive.

**Objectif** : Transformer un fichier CSV massif en une application analytique performante capable d'agréger plus de **1 million de transactions** en temps réel.

---

## 🏗️ Architecture Technique & Pipeline ETL

Le projet est structuré en plusieurs modules techniques pour une séparation claire des responsabilités :

### 1. Ingestion & Nettoyage (ETL)
- **Extraction** : Scripts automatisés pour récupérer les données DVF.
- **Transformation** : Utilisation de `Pandas` avec lecture par **Chunks** (blocs de 100k lignes). Cette approche permet de traiter des fichiers de plusieurs Go sur une machine standard sans saturer la RAM.
- **Data Quality** : Filtrage des transactions aberrantes, gestion des valeurs nulles, et normalisation des types (dates, surfaces).

### 2. Stockage Multi-Environnement
- **Développement (Local)** : Utilisation de **MySQL** pour une gestion robuste des relations et des performances SQL.
- **Production (Hébergement)** : Migration vers **SQLite** pour une portabilité totale sur Streamlit Cloud. Un script d'export automatisé permet de synchroniser les données entre les deux environnements.

### 3. Analyse & Visualisation
- **Dashboard Streamlit** : Interface utilisateur premium avec injection CSS personnalisée.
- **Visualisation dynamique** : Graphiques interactifs avec **Plotly** (Cartographie, Saisonnalité, Top Communes).
- **Optimisation** : Agrégations réalisées directement par le moteur SQL pour minimiser le transfert de données vers l'application.

---

## 📂 Structure du Repository (Simplifiée)

```bash
├── dashboard/          # Point d'entrée de l'application Streamlit
├── data/               # Base de données SQLite (dvf_data.db)
├── scripts/            # Utilitaires (Migration, Exports)
├── src/                # Code source du pipeline technique
│   ├── ingestion/      # Scripts de chargement MySQL
│   ├── transformation/ # Logique de nettoyage des données
│   ├── database/       # Gestion des connexions (Dual MySQL/SQLite)
│   └── analysis/       # Requêtes SQL analytiques
└── requirements.txt    # Dépendances du projet
```

---

## 🚀 Installation et Utilisation

### 1. Prérequis
- Python 3.9+
- Pip

### 2. Installation
```bash
# Cloner le projet
git clone <votre-repo>
cd dvm_imi_pipeline

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Lancer le Dashboard
Le projet est configuré pour utiliser automatiquement la base de données SQLite fournie par défaut.
```bash
streamlit run dashboard/app.py
```

---

## 💡 Concepts présentés lors des entretiens
- **Gestion de la Mémoire** : Traitement par Chunks avec Pandas.
- **Architecture ORM** : Utilisation de SQLAlchemy pour une flexibilité MySQL/SQLite.
- **Déploiement Cloud** : Stratégie de portabilité de base de données pour l'hébergement public.
- **Design UI/UX** : Création d'un dashboard analytique intuitif et épuré.
