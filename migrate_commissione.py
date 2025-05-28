#!/usr/bin/env python3
"""
Script per migrare il database aggiungendo i nuovi campi al modello Commissione.
Questa migrazione aggiunge: cognome_membro, titolo_accademico, affiliazione, email, telefono, note, created_at
"""

import os
import shutil
import sqlite3
from datetime import datetime

def backup_database(db_path):
    """Crea un backup del database prima della migrazione"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = db_path.replace('.db', f'_backup_commissione_{timestamp}.db')
    shutil.copy2(db_path, backup_path)
    print(f"✅ Backup creato: {backup_path}")
    return backup_path

def migrate_commissione_table(db_path):
    """Migra la tabella commissione aggiungendo i nuovi campi"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Controlla se i nuovi campi esistono già
        cursor.execute("PRAGMA table_info(commissione)")
        columns = [column[1] for column in cursor.fetchall()]
        
        new_columns = [
            ('cognome_membro', 'VARCHAR(100)'),
            ('titolo_accademico', 'VARCHAR(100)'),
            ('affiliazione', 'VARCHAR(200)'),
            ('email', 'VARCHAR(120)'),
            ('telefono', 'VARCHAR(20)'),
            ('note', 'TEXT'),
            ('created_at', 'DATETIME')
        ]
        
        # Aggiungi le nuove colonne se non esistono
        for column_name, column_type in new_columns:
            if column_name not in columns:
                if column_name == 'cognome_membro':
                    # Per cognome_membro, impostiamo un valore di default vuoto
                    cursor.execute(f"ALTER TABLE commissione ADD COLUMN {column_name} {column_type} DEFAULT ''")
                elif column_name == 'created_at':
                    # Per created_at, impostiamo la data corrente come default
                    current_time = datetime.now().isoformat()
                    cursor.execute(f"ALTER TABLE commissione ADD COLUMN {column_name} {column_type} DEFAULT '{current_time}'")
                else:
                    cursor.execute(f"ALTER TABLE commissione ADD COLUMN {column_name} {column_type}")
                print(f"✅ Aggiunta colonna: {column_name}")
            else:
                print(f"⚠️  Colonna {column_name} già esistente")
        
        # Aggiorna il campo ruolo per renderlo NOT NULL se non lo è già
        cursor.execute("PRAGMA table_info(commissione)")
        table_info = cursor.fetchall()
        ruolo_info = next((col for col in table_info if col[1] == 'ruolo'), None)
        
        if ruolo_info and ruolo_info[3] == 0:  # Se ruolo non è NOT NULL
            print("🔄 Aggiornamento campo ruolo per renderlo NOT NULL...")
            
            # Prima impostiamo un valore di default per i record esistenti con ruolo NULL
            cursor.execute("UPDATE commissione SET ruolo = 'docente' WHERE ruolo IS NULL OR ruolo = ''")
            
            # Creiamo una nuova tabella con la struttura corretta
            cursor.execute("""
                CREATE TABLE commissione_new (
                    id INTEGER PRIMARY KEY,
                    esame_id INTEGER NOT NULL,
                    nome_membro VARCHAR(100) NOT NULL,
                    cognome_membro VARCHAR(100) NOT NULL DEFAULT '',
                    ruolo VARCHAR(50) NOT NULL,
                    is_esterno_usr_lazio BOOLEAN DEFAULT 0,
                    titolo_accademico VARCHAR(100),
                    affiliazione VARCHAR(200),
                    email VARCHAR(120),
                    telefono VARCHAR(20),
                    note TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (esame_id) REFERENCES esame(id)
                )
            """)
            
            # Copiamo i dati dalla vecchia tabella alla nuova
            cursor.execute("""
                INSERT INTO commissione_new 
                (id, esame_id, nome_membro, cognome_membro, ruolo, is_esterno_usr_lazio, 
                 titolo_accademico, affiliazione, email, telefono, note, created_at)
                SELECT id, esame_id, nome_membro, 
                       COALESCE(cognome_membro, '') as cognome_membro,
                       ruolo, is_esterno_usr_lazio,
                       titolo_accademico, affiliazione, email, telefono, note,
                       COALESCE(created_at, datetime('now')) as created_at
                FROM commissione
            """)
            
            # Eliminiamo la vecchia tabella e rinominiamo la nuova
            cursor.execute("DROP TABLE commissione")
            cursor.execute("ALTER TABLE commissione_new RENAME TO commissione")
            
            print("✅ Tabella commissione ricreata con vincoli corretti")
        
        conn.commit()
        print("✅ Migrazione della tabella commissione completata con successo!")
        
        # Verifica finale
        cursor.execute("SELECT COUNT(*) FROM commissione")
        count = cursor.fetchone()[0]
        print(f"📊 Totale membri commissione nel database: {count}")
        
    except Exception as e:
        print(f"❌ Errore durante la migrazione: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

def main():
    """Funzione principale per eseguire la migrazione"""
    print("🚀 Inizio migrazione database commissione...")
    
    # Percorso del database
    db_path = os.path.join('instance', 'esami_pef.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database non trovato: {db_path}")
        return
    
    # Crea backup
    backup_path = backup_database(db_path)
    
    try:
        # Esegui migrazione
        migrate_commissione_table(db_path)
        print("🎉 Migrazione completata con successo!")
        print(f"💾 Backup disponibile in: {backup_path}")
        
    except Exception as e:
        print(f"❌ Migrazione fallita: {str(e)}")
        print(f"🔄 Ripristinare il backup da: {backup_path}")
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
