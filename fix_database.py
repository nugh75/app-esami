import os
import sqlite3

# Percorso del database
db_path = 'esami_pef.db'

# Connessione al database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verifica se la tabella esame_new esiste già
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='esame_new'")
if cursor.fetchone() is None:
    # Creazione della nuova tabella con le colonne corrette
    cursor.execute('''
    CREATE TABLE esame_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        classe_concorso TEXT NOT NULL,
        percorsi_pef TEXT NOT NULL,
        modalita TEXT NOT NULL,
        sede TEXT,
        note TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_inizio TIMESTAMP,
        data_fine TIMESTAMP
    )
    ''')
else:
    print("La tabella 'esame_new' esiste già. Non verrà creata di nuovo.")

# Verifica se la tabella esame esiste
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='esame'")
if cursor.fetchone() is not None:
    # Copia dei dati dalla tabella esame alla nuova tabella esame_new
    cursor.execute('''
    INSERT INTO esame_new (id, classe_concorso, percorsi_pef, modalita, sede, note, created_at, data_inizio, data_fine)
    SELECT id, classe_concorso, percorsi_pef, modalita, sede, note, created_at, data_inizio, data_fine FROM esame
    ''')
else:
    print("La tabella 'esame' non esiste. Non ci sono dati da copiare.")

# Verifica se la tabella esame esiste prima di tentare di eliminarla
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='esame'")
if cursor.fetchone() is not None:
    cursor.execute('DROP TABLE esame')
else:
    print("La tabella 'esame' non esiste. Non verrà eliminata.")

# Rinomina della nuova tabella
cursor.execute('ALTER TABLE esame_new RENAME TO esame')

# Commit delle modifiche e chiusura della connessione
conn.commit()
conn.close()

print("Migrazione completata con successo!")
