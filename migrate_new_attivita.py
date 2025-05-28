#!/usr/bin/env python
"""
Script per migrare i tipi di attività esistenti ai nuovi tipi
Questo script aggiorna tutti i record esistenti nella tabella CalendarioEsame
per utilizzare i nuovi tipi di attività.
"""
from app import app, db, CalendarioEsame
import sys
import os
from datetime import datetime

# Mappatura dai vecchi tipi di attività ai nuovi
MAPPING_ATTIVITA = {
    'prova_scritta': 'prova_scritta_presenza',
    'prova_orale': 'lezione_simulata',
    'prova_pratica': 'lezione_simulata',
    'laboratorio': 'altro',
    'simulazione': 'lezione_simulata',
    'verifica_portfolio': 'altro',
    'presentazione_progetto': 'altro',
    'discussione_tesi': 'altro',
    'workshop': 'altro',
    'seminario': 'altro',
    'tirocinio': 'altro',
    'altro': 'altro'
}

def backup_database():
    """Crea un backup del database prima di procedere con la migrazione"""
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if db_path.startswith('/'):  # Path assoluto
        source_path = db_path
    else:  # Path relativo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        source_path = os.path.join(base_dir, db_path)
    
    # Rimuovi eventuali parametri dalla stringa di connessione
    if '?' in source_path:
        source_path = source_path.split('?')[0]
    
    if not os.path.exists(source_path):
        print(f"ERRORE: Database non trovato in {source_path}")
        return False
    
    # Crea backup con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = os.path.splitext(source_path)[0] + f"_backup_attivita_{timestamp}" + os.path.splitext(source_path)[1]
    
    # Copia il file
    try:
        import shutil
        shutil.copy2(source_path, backup_name)
        print(f"✅ Backup del database creato: {backup_name}")
        return True
    except Exception as e:
        print(f"❌ Errore durante il backup del database: {e}")
        return False

def migrate_attivita():
    """Aggiorna i tipi di attività esistenti in base alla mappatura"""
    # Conta le date da migrare
    total_records = CalendarioEsame.query.count()
    print(f"📊 Trovati {total_records} record nella tabella CalendarioEsame")
    
    # Statistiche iniziali
    stats_before = {}
    for old_type in MAPPING_ATTIVITA.keys():
        count = CalendarioEsame.query.filter_by(attivita=old_type).count()
        if count > 0:
            stats_before[old_type] = count
    
    if stats_before:
        print("\n🔍 Distribuzione attuale dei tipi di attività:")
        for tipo, count in stats_before.items():
            print(f"   {tipo}: {count}")
    else:
        print("\n⚠️ Nessuna attività trovata nel database.")
    
    # Esegui la migrazione
    for old_type, new_type in MAPPING_ATTIVITA.items():
        records = CalendarioEsame.query.filter_by(attivita=old_type).all()
        if records:
            print(f"\n🔄 Aggiornamento di {len(records)} record da '{old_type}' a '{new_type}'...")
            for record in records:
                record.attivita = new_type
    
    # Salva le modifiche
    try:
        db.session.commit()
        print("\n✅ Migrazione completata con successo!")
        
        # Statistiche finali
        stats_after = {}
        for new_type in set(MAPPING_ATTIVITA.values()):
            count = CalendarioEsame.query.filter_by(attivita=new_type).count()
            if count > 0:
                stats_after[new_type] = count
        
        if stats_after:
            print("\n📊 Nuova distribuzione dei tipi di attività:")
            for tipo, count in stats_after.items():
                print(f"   {tipo}: {count}")
        
        return True
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Errore durante la migrazione: {e}")
        return False

if __name__ == "__main__":
    with app.app_context():
        print("🚀 Inizio migrazione tipi di attività...")
        print("=" * 50)
        
        # Backup database
        if not backup_database():
            print("❌ Migrazione annullata: impossibile creare backup.")
            sys.exit(1)
        
        # Migrazione attività
        if migrate_attivita():
            print("\n🎉 La migrazione è stata completata con successo!\n")
        else:
            print("\n❌ La migrazione è fallita.\n")
            sys.exit(1)
