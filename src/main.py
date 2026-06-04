import pandas as pd
from sqlalchemy import create_engine

# Connexion à la base PostgreSQL
DATABASE_URL = "postgresql://admin:password@localhost:5432/meteo_data"
engine = create_engine(DATABASE_URL)

def nettoyage_et_chargement():
    
    file_path_raw = "./data/raw/Q_01_avant-1949_RR-T-Vent.csv"
    print(f"📥 Lecture directe du fichier CSV : {file_path_raw}")
    
    # Lecture du fichier
    df = pd.read_csv(file_path_raw, sep=';', low_memory=False)
    df.columns = df.columns.str.strip()
    
    # Normalisation des colonnes de base
    if 'AAAAMMJJ' in df.columns:
        df['date'] = pd.to_datetime(df['AAAAMMJJ'].astype(str), format='%Y%m%d')
    if 'NUM_POSTE' in df.columns:
        df['code_departement'] = df['NUM_POSTE'].astype(str).str.zfill(8).str[:2]

    # Renommage Metabase
    rename_dict = {
        'NUM_POSTE': 'id_station',
        'NOM_USUEL': 'nom_station',
        'LON': 'longitude',
        'LAT': 'latitude',
        'ALTI': 'altitude_metres',
        'RR': 'precipitations_mm',
        'QRR': 'qualite_donnee_rr'
    }
    df = df.rename(columns={k: v for k, v in rename_dict.items() if k in df.columns})

    # Sélection des colonnes
    colonnes_utiles = [
        'id_station', 'nom_station', 'longitude', 'latitude', 
        'altitude_metres', 'precipitations_mm', 'qualite_donnee_rr', 
        'date', 'code_departement'
    ]
    # Conservation des colonnes sélectionnés
    df = df[[col for col in colonnes_utiles if col in df.columns]]

    # Sauvegarde dans /processed
    file_path_processed = "./data/processed/meteo_1949.csv"
    df.to_csv(file_path_processed, index=False)
    print(f"💾 Fichier nettoyé sauvegardé : {file_path_processed}")
    
    # Injection dans PostgreSQL
    table_name = "meteo_1949"
    print(f"🚀 Injection dans la table PostgreSQL : {table_name}...")
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    print(f"✅ Terminé ! {len(df)} lignes prêtes dans Postgres.")

if __name__ == "__main__":
    nettoyage_et_chargement()
