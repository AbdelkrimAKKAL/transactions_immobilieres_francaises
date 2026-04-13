from sqlalchemy import Column, Integer, String, Float, Date
from .connection import Base, engine

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    id_mutation = Column(String(255), index=True)
    date_mutation = Column(Date)
    valeur_fonciere = Column(Float)
    code_postal = Column(String(10), index=True)
    code_commune = Column(String(10))
    nom_commune = Column(String(255))
    code_departement = Column(String(5), index=True)
    type_local = Column(String(50))
    surface_reelle_bati = Column(Float)
    nombre_pieces_principales = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)

if __name__ == "__main__":
    print("Création de la table 'transactions' dans MySQL...")
    Base.metadata.create_all(bind=engine)
    print("Table créée avec succès ! 🎉")
