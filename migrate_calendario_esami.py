#!/usr/bin/env python3
"""
Script per migrare il database da "data esame principale + date aggiuntive" 
a "calendario esami" e aggiornare il modello Commissione.

Modifiche:
1. Rimuove data_inizio e data_fine dal modello Esame
2. Sposta le date principali degli esami esistenti come prime date nel calendario
3. Rinomina data_aggiuntiva → calendario_esami 
4. Aggiorna modello Commissione: rimuove campi non necessari, aggiunge profilo
"""

import os
import shutil
import sqlite3
from datetime import datetime

def backup_database(db_path):
    """Crea un backup del database prima della migrazione"""
    if not os.path.exists(db_path):
        print(f"❌ Database non trovato: {db_path}")
        return None
        
    backup_path = f'instance/esami_pef_backup_calendario_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creato: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Errore durante il backup: {e}")
        return None

def migrate_to_calendario_esami(db_path):
    """Migra da data esame principale a calendario esami"""
    print("🔄 Inizio migrazione a calendario esami...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Verifica struttura attuale
        cursor.execute("PRAGMA table_info(esame)")
        esame_columns = [col[1] for col in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(data_aggiuntiva)")
        data_aggiuntiva_columns = [col[1] for col in cursor.fetchall()]
        
        print(f"📋 Colonne esame attuali: {esame_columns}")
        print(f"📋 Colonne data_aggiuntiva attuali: {data_aggiuntiva_columns}")
        
        # 2. Sposta le date principali degli esami come prime date del calendario
        if 'data_inizio' in esame_columns and 'data_fine' in esame_columns:
            print("📅 Spostamento date principali nel calendario...")
            
            # Ottieni tutti gli esami con le loro date principali
            cursor.execute("""
                SELECT id, data_inizio, data_fine, modalita, sede 
                FROM esame 
                WHERE data_inizio IS NOT NULL AND data_fine IS NOT NULL
            """)
            esami_con_date = cursor.fetchall()
            
            # Inserisci le date principali come prime voci del calendario
            for esame_id, data_inizio, data_fine, modalita, sede in esami_con_date:
                cursor.execute("""
                    INSERT INTO data_aggiuntiva (esame_id, data_inizio, data_fine, modalita, sede, attivita)
                    VALUES (?, ?, ?, ?, ?, 'altro')
                """, (esame_id, data_inizio, data_fine, modalita, sede or ''))
            
            print(f"✅ Spostate {len(esami_con_date)} date principali nel calendario")
        
        # 3. Rinomina tabella data_aggiuntiva → calendario_esami
        print("🔄 Rinomino tabella data_aggiuntiva → calendario_esami...")
        cursor.execute("ALTER TABLE data_aggiuntiva RENAME TO calendario_esami")
        print("✅ Tabella rinominata")
        
        # 4. Crea nuova tabella esame senza date principali
        print("🔄 Ricreo tabella esame senza date principali...")
        cursor.execute("""
            CREATE TABLE esame_new (
                id INTEGER PRIMARY KEY,
                classe_concorso VARCHAR(10) NOT NULL,
                percorsi_pef TEXT NOT NULL,
                modalita VARCHAR(20) NOT NULL,
                sede VARCHAR(200),
                note TEXT,
                created_at DATETIME
            )
        """)
        
        # Copia i dati (escludendo data_inizio e data_fine)
        cursor.execute("""
            INSERT INTO esame_new (id, classe_concorso, percorsi_pef, modalita, sede, note, created_at)
            SELECT id, classe_concorso, percorsi_pef, modalita, sede, note, created_at
            FROM esame
        """)
        
        # Sostituisci la tabella
        cursor.execute("DROP TABLE esame")
        cursor.execute("ALTER TABLE esame_new RENAME TO esame")
        print("✅ Tabella esame aggiornata")
        
        # 5. Aggiorna foreign key nella tabella calendario_esami
        print("🔄 Aggiorno relazioni...")
        cursor.execute("PRAGMA foreign_keys=off")
        cursor.execute("""
            CREATE TABLE calendario_esami_new (
                id INTEGER PRIMARY KEY,
                esame_id INTEGER NOT NULL,
                data_inizio DATETIME NOT NULL,
                data_fine DATETIME NOT NULL,
                modalita VARCHAR(20) NOT NULL,
                sede VARCHAR(200),
                attivita VARCHAR(50) NOT NULL DEFAULT 'altro',
                FOREIGN KEY (esame_id) REFERENCES esame(id)
            )
        """)
        
        cursor.execute("""
            INSERT INTO calendario_esami_new
            SELECT * FROM calendario_esami
        """)
        
        cursor.execute("DROP TABLE calendario_esami")
        cursor.execute("ALTER TABLE calendario_esami_new RENAME TO calendario_esami")
        cursor.execute("PRAGMA foreign_keys=on")
        print("✅ Relazioni aggiornate")
        
        conn.commit()
        print("✅ Migrazione calendario esami completata!")
        
    except Exception as e:
        print(f"❌ Errore durante migrazione calendario: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def migrate_commissione_model(db_path):
    """Aggiorna il modello Commissione"""
    print("🔄 Inizio migrazione modello Commissione...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verifica struttura attuale
        cursor.execute("PRAGMA table_info(commissione)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"📋 Colonne commissione attuali: {columns}")
        
        # Crea nuova tabella commissione con il campo profilo
        print("🔄 Ricreo tabella commissione...")
        cursor.execute("""
            CREATE TABLE commissione_new (
                id INTEGER PRIMARY KEY,
                esame_id INTEGER NOT NULL,
                nome_membro VARCHAR(100) NOT NULL,
                cognome_membro VARCHAR(100) NOT NULL,
                ruolo VARCHAR(50) NOT NULL,
                profilo VARCHAR(100) NOT NULL DEFAULT 'esterno_altro',
                email VARCHAR(120),
                telefono VARCHAR(20),
                note TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (esame_id) REFERENCES esame(id)
            )
        """)
        
        # Migra i dati esistenti, mappando i vecchi campi al nuovo profilo
        if 'profilo' not in columns:
            print("🔄 Migrazione dati commissione con mappatura profilo...")
            cursor.execute("""
                INSERT INTO commissione_new 
                (id, esame_id, nome_membro, cognome_membro, ruolo, profilo, email, telefono, note, created_at)
                SELECT 
                    id, 
                    esame_id, 
                    nome_membro, 
                    COALESCE(cognome_membro, '') as cognome_membro,
                    ruolo,
                    CASE 
                        WHEN is_esterno_usr_lazio = 1 THEN 'referente_usr'
                        WHEN ruolo = 'tutor_coordinatore' THEN 'tutor_coordinatore'
                        WHEN ruolo = 'presidente' THEN 'prof_ricercatore_roma3'
                        WHEN ruolo = 'docente' THEN 'docente_contratto'
                        ELSE 'esterno_altro'
                    END as profilo,
                    email,
                    telefono,
                    note,
                    created_at
                FROM commissione
            """)
        else:
            # Se profilo esiste già, copia direttamente
            cursor.execute("""
                INSERT INTO commissione_new 
                SELECT id, esame_id, nome_membro, cognome_membro, ruolo, profilo, email, telefono, note, created_at
                FROM commissione
            """)
        
        # Sostituisci la tabella
        cursor.execute("DROP TABLE commissione")
        cursor.execute("ALTER TABLE commissione_new RENAME TO commissione")
        print("✅ Tabella commissione aggiornata")
        
        conn.commit()
        print("✅ Migrazione commissione completata!")
        
    except Exception as e:
        print(f"❌ Errore durante migrazione commissione: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def main():
    """Funzione principale per eseguire la migrazione completa"""
    db_path = 'instance/esami_pef.db'
    
    print("🚀 Inizio migrazione completa a Calendario Esami")
    print("=" * 60)
    
    # 1. Backup
    backup_path = backup_database(db_path)
    if not backup_path:
        return 1
    
    try:
        # 2. Migrazione calendario esami
        migrate_to_calendario_esami(db_path)
        
        # 3. Migrazione commissione
        migrate_commissione_model(db_path)
        
        print("=" * 60)
        print("🎉 MIGRAZIONE COMPLETATA CON SUCCESSO!")
        print(f"📁 Backup disponibile in: {backup_path}")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print("=" * 60)
        print(f"❌ MIGRAZIONE FALLITA: {e}")
        print(f"🔄 Ripristina il backup da: {backup_path}")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
