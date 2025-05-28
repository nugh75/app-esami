#!/usr/bin/env python3
"""
Script di migrazione per aggiungere il campo 'attivita' alla tabella DataAggiuntiva
"""

import sqlite3
import os
import sys

# Aggiungi il path dell'applicazione
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def migrate_add_attivita_field():
    """Aggiunge il campo attivita alla tabella data_aggiuntiva"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'esami_pef.db')
    
    if not os.path.exists(db_path):
        print(f"Database non trovato: {db_path}")
        print("Assicurati che l'applicazione sia stata eseguita almeno una volta per creare il database.")
        return False
    
    print(f"Connessione al database: {db_path}")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Verifica se la colonna esiste già
            cursor.execute("PRAGMA table_info(data_aggiuntiva)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'attivita' in columns:
                print("Il campo 'attivita' esiste già nella tabella data_aggiuntiva.")
                return True
            
            print("Aggiunta del campo 'attivita' alla tabella data_aggiuntiva...")
            
            # Aggiungi la colonna attivita con valore di default 'altro'
            cursor.execute("""
                ALTER TABLE data_aggiuntiva 
                ADD COLUMN attivita VARCHAR(50) NOT NULL DEFAULT 'altro'
            """)
            
            # Aggiorna tutti i record esistenti con il valore di default
            cursor.execute("""
                UPDATE data_aggiuntiva 
                SET attivita = 'altro' 
                WHERE attivita IS NULL OR attivita = ''
            """)
            
            conn.commit()
            
            # Verifica il risultato
            cursor.execute("SELECT COUNT(*) FROM data_aggiuntiva")
            count = cursor.fetchone()[0]
            
            print(f"✅ Migrazione completata con successo!")
            print(f"   Campo 'attivita' aggiunto a {count} record esistenti.")
            print(f"   Valore predefinito impostato su 'altro'.")
            
            return True
            
    except sqlite3.Error as e:
        print(f"❌ Errore durante la migrazione: {e}")
        return False
    except Exception as e:
        print(f"❌ Errore inaspettato: {e}")
        return False

def verify_migration():
    """Verifica che la migrazione sia stata applicata correttamente"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'esami_pef.db')
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Verifica la struttura della tabella
            cursor.execute("PRAGMA table_info(data_aggiuntiva)")
            columns = cursor.fetchall()
            
            print("\n📋 Struttura attuale della tabella data_aggiuntiva:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'} {f'DEFAULT {col[4]}' if col[4] else ''}")
            
            # Conta i record con attivita
            cursor.execute("SELECT attivita, COUNT(*) FROM data_aggiuntiva GROUP BY attivita")
            attivita_counts = cursor.fetchall()
            
            if attivita_counts:
                print("\n📊 Distribuzione tipi di attività:")
                for attivita, count in attivita_counts:
                    print(f"   - {attivita}: {count} record")
            else:
                print("\n📊 Nessun record di date aggiuntive presente nel database.")
            
            return True
            
    except Exception as e:
        print(f"❌ Errore durante la verifica: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Avvio migrazione database per campo 'attivita'...")
    print("="*60)
    
    success = migrate_add_attivita_field()
    
    if success:
        print("\n🔍 Verifica della migrazione...")
        verify_migration()
        print("\n✅ Migrazione completata! Il sistema è pronto per l'uso.")
        print("\nOra puoi:")
        print("1. Riavviare l'applicazione Flask")
        print("2. Aggiungere nuove date aggiuntive con tipo di attività")
        print("3. Le date esistenti avranno 'Altro' come tipo di attività")
    else:
        print("\n❌ Migrazione fallita. Verifica i log degli errori sopra.")
        sys.exit(1)
