import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

import streamlit as st


load_dotenv()


try:
    DB_URL = st.secrets.get("DB_URL")
except Exception:
    DB_URL = None

if not DB_URL:
    DB_URL = os.getenv("DB_URL")

if not DB_URL:
    DB_URL = "sqlite:///data/dvf_data.db"

if DB_URL.startswith("sqlite"):
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=False)
else:
    engine = create_engine(DB_URL, echo=False)

# Créateur de "sessions" pour parler à la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base que tous nos modèles (tables) vont utiliser
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
