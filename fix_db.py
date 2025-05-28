import sqlite3

def add_missing_columns():
    """Aggiunge le colonne data_inizio e data_fine alla tabella esame nel database instance/esami_pef.db"""
    print("Aggiunta colonne mancanti al database...")
    
    conn = sqlite3.connect('instance/esami_pef.db')
    cursor = conn.cursor()
    
    # Controllo se le colonne esistono già
    cursor.execute("PRAGMA table_info(esame)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Aggiungo le colonne solo se non esistono
    if 'data_inizio' not in columns:
        print("Aggiunta colonna data_inizio...")
        cursor.execute("ALTER TABLE esame ADD COLUMN data_inizio DATETIME")
    
    if 'data_fine' not in columns:
        print("Aggiunta colonna data_fine...")
        cursor.execute("ALTER TABLE esame ADD COLUMN data_fine DATETIME")
    
    # Commit e chiusura della connessione
    conn.commit()
    conn.close()
    
    print("Database aggiornato con successo!")

if __name__ == "__main__":
    add_missing_columns()
