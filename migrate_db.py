#!/usr/bin/env python3
"""
Script per migrare il database dalla vecchia struttura alla nuova.
Aggiunge la colonna percorsi_pef e migra i dati da percorso_pef.
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    db_path = 'instance/esami_pef.db'
    
    if not os.path.exists(db_path):
        print("Database non trovato, nessuna migrazione necessaria.")
        return
    
    # Backup del database
    backup_path = f'instance/esami_pef_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"Backup creato: {backup_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verifica se la colonna percorsi_pef esiste già
        cursor.execute("PRAGMA table_info(esame)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'percorsi_pef' in columns:
            print("La colonna percorsi_pef esiste già.")
            return
        
        print("Migrazione del database in corso...")
        
        # 1. Aggiungi la nuova colonna percorsi_pef
        cursor.execute("ALTER TABLE esame ADD COLUMN percorsi_pef TEXT")
        print("Colonna percorsi_pef aggiunta.")
        
        # 2. Migra i dati dalla vecchia colonna alla nuova
        if 'percorso_pef' in columns:
            cursor.execute("UPDATE esame SET percorsi_pef = percorso_pef WHERE percorso_pef IS NOT NULL")
            print("Dati migrati da percorso_pef a percorsi_pef.")
            
            # 3. Imposta i valori NULL come stringa vuota
            cursor.execute("UPDATE esame SET percorsi_pef = '' WHERE percorsi_pef IS NULL")
            
            # 4. Rendi la colonna NOT NULL
            # SQLite non supporta ALTER COLUMN, quindi dobbiamo ricreare la tabella
            print("Ricreazione della tabella con la nuova struttura...")
            
            # Salva i dati esistenti
            cursor.execute("""
                CREATE TABLE esame_new (
                    id INTEGER PRIMARY KEY,
                    classe_concorso VARCHAR(10) NOT NULL,
                    percorsi_pef TEXT NOT NULL,
                    data_inizio DATETIME NOT NULL,
                    data_fine DATETIME NOT NULL,
                    modalita VARCHAR(20) NOT NULL,
                    sede VARCHAR(200),
                    note TEXT,
                    created_at DATETIME
                )
            """)
            
            # Copia i dati
            cursor.execute("""
                INSERT INTO esame_new (id, classe_concorso, percorsi_pef, data_inizio, data_fine, modalita, sede, note, created_at)
                SELECT id, classe_concorso, percorsi_pef, data_inizio, data_fine, modalita, sede, note, created_at
                FROM esame
            """)
            
            # Elimina la vecchia tabella e rinomina la nuova
            cursor.execute("DROP TABLE esame")
            cursor.execute("ALTER TABLE esame_new RENAME TO esame")
            
            print("Tabella ricreata con successo.")
        else:
            print("Colonna percorso_pef non trovata, impostazione valori di default...")
            cursor.execute("UPDATE esame SET percorsi_pef = '' WHERE percorsi_pef IS NULL")
        
        conn.commit()
        print("Migrazione completata con successo!")
        
    except Exception as e:
        print(f"Errore durante la migrazione: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
