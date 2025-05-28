import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db

def check_columns_exist(cursor, table, columns):
    """Verifica se le colonne esistono nella tabella"""
    cursor.execute(f"PRAGMA table_info({table})")
    existing_columns = [row[1] for row in cursor.fetchall()]
    return all(column in existing_columns for column in columns)

def add_columns():
    """Aggiunge le colonne data_inizio e data_fine alla tabella esame se non esistono"""
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    
    # Se è un percorso relativo, gestiscilo correttamente
    if not os.path.isabs(db_path):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Controlla se le colonne esistono già
    columns_to_add = ['data_inizio', 'data_fine']
    if not check_columns_exist(cursor, 'esame', columns_to_add):
        print("Aggiunta colonne data_inizio e data_fine alla tabella esame...")
        
        # Aggiungi le colonne
        cursor.execute("ALTER TABLE esame ADD COLUMN data_inizio TIMESTAMP")
        cursor.execute("ALTER TABLE esame ADD COLUMN data_fine TIMESTAMP")
        
        # Commit delle modifiche
        conn.commit()
        print("Colonne aggiunte con successo!")
    else:
        print("Le colonne data_inizio e data_fine esistono già nella tabella esame.")
    
    conn.close()

if __name__ == "__main__":
    with app.app_context():
        add_columns()
        print("Migrazione completata!")
