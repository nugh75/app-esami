#!/usr/bin/env python3
"""
Script per migrare il database aggiornando il modello Commissione.
Questa migrazione aggiunge: tipologia, profilo
e rimuove: titolo_accademico, affiliazione, is_esterno_usr_lazio
"""

import os
import shutil
import sqlite3
from datetime import datetime

def backup_database(db_path):
    """Crea un backup del database prima della migrazione"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = db_path.replace('.db', f'_backup_commissione_v2_{timestamp}.db')
    shutil.copy2(db_path, backup_path)
    print(f"✅ Backup creato: {backup_path}")
    return backup_path

def migrate_commissione_table(db_path):
    """Migra la tabella commissione aggiungendo i nuovi campi e rimuovendo quelli obsoleti"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Controlla se i nuovi campi esistono già
        cursor.execute("PRAGMA table_info(commissione)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Nuovi campi da aggiungere
        new_columns = [
            ('tipologia', "VARCHAR(10) DEFAULT 'T'"),  # 'T' = Titolare, 'S' = Supplente
            ('profilo', "VARCHAR(100) DEFAULT 'esterno_altro'")  # Profilo di default
        ]
        
        # Aggiungi le nuove colonne se non esistono
        for column_name, column_type in new_columns:
            if column_name not in columns:
                cursor.execute(f"ALTER TABLE commissione ADD COLUMN {column_name} {column_type}")
                print(f"✅ Aggiunta colonna: {column_name}")
            else:
                print(f"⚠️  Colonna {column_name} già esistente")
        
        # Migrazione dei dati: converti is_esterno_usr_lazio in profilo
        if 'is_esterno_usr_lazio' in columns and 'profilo' in columns:
            cursor.execute("""
                UPDATE commissione
                SET profilo = CASE
                    WHEN is_esterno_usr_lazio = 1 THEN 'referente_usr'
                    ELSE 'esterno_altro'
                END
                WHERE profilo = 'esterno_altro'
            """)
            print("✅ Migrati dati da is_esterno_usr_lazio a profilo")
        
        # Migrazione dei dati: assegna ruoli in base ai dati esistenti
        if 'ruolo' in columns:
            cursor.execute("""
                UPDATE commissione
                SET ruolo = CASE
                    WHEN ruolo = 'Presidente' THEN 'presidente'
                    WHEN ruolo = 'Membro' AND profilo = 'referente_usr' THEN 'referente_usr'
                    WHEN ruolo = 'Membro' AND profilo != 'referente_usr' THEN 'docente_interno'
                    ELSE ruolo
                END
            """)
            print("✅ Aggiornati i ruoli secondo il nuovo schema")
        
        conn.commit()
        print("✅ Migrazione completata con successo")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Errore durante la migrazione: {str(e)}")
    finally:
        conn.close()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'esami_pef.db')
    instance_db_path = os.path.join(script_dir, 'instance', 'esami_pef.db')
    
    # Usa il database nell'istanza se esiste, altrimenti usa quello nella directory principale
    db_to_use = instance_db_path if os.path.exists(instance_db_path) else db_path
    
    if not os.path.exists(db_to_use):
        print(f"❌ Database non trovato in: {db_to_use}")
        return
    
    print(f"🔍 Utilizzo database: {db_to_use}")
    backup_path = backup_database(db_to_use)
    migrate_commissione_table(db_to_use)
    
    print("\n🎉 Processo di migrazione completato!")
    print(f"📊 Database originale: {db_to_use}")
    print(f"📊 Database di backup: {backup_path}")

if __name__ == "__main__":
    main()
