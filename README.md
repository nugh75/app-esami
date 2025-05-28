# Gestione Esami PEF

Applicazione web sviluppata in Python Flask per la pianificazione e la gestione completa degli esami PEF (Percorsi di formazione per l'acquisizione di 60 CFU), con supporto al calendario delle attività, alle commissioni d’esame e all’esportazione dei dati.

---

## Funzionalità principali

1. Dashboard e ricerca
   - Vista tabellare di tutti gli esami con filtri per classe di concorso, modalità e testo libero
   - Statistiche in tempo reale: totale esami, suddivisione per modalità, esami con commissione
   - Grafici e numeri sui ruoli e profili dei membri di commissione
   - Statistiche sui tipi di attività (prova scritta, lezione simulata, definizione criteri, ecc.)

2. Gestione Esami
   - Creazione, lettura, modifica e cancellazione (CRUD) degli esami
   - Pianificazione delle date principali e delle attività aggiuntive (calendario esami)
   - Dettaglio esame con elenco delle date e delle attività collegate

3. Gestione Commissioni d’esame
   - Aggiunta di membri alla commissione per ogni esame (titolari e supplenti)
   - Modifica ed eliminazione delle commissioni associate a un esame
   - Pagina dedicata `/membri_commissioni` per visualizzare tutti i membri e le statistiche sui loro ruoli

4. Gestione Membri di Commissione
   - Anagrafica membri (nome, cognome, profilo, contatti, note)
   - Associazione di uno stesso membro a commissioni diverse, con ruoli distinti
   - Pagine CRUD per i membri (`/nuovo_membro_commissione`, `/membro_commissione/<id>`)

5. Esportazioni e download
   - **Calendario iCal** (`/scarica_calendario`): file `.ics` con tutte le date e attività
   - **Excel Esami** (`/scarica_excel`): elenco completo degli esami
   - **Excel Date** (`/scarica_excel_date`): esportazione di tutte le date con attività e modalità
   - **Excel Commissioni** (`/scarica_excel_commissioni`): elenco dei membri di commissione per ciascun esame

6. Backup del database
   - **Backup manuale**: pulsante “Backup Database” in navbar (route POST `/backup_database`)
   - **Backup giornaliero automatico**: scheduler integrato (lancia il backup ogni giorno alle 02:00 e mantiene i file in `backups/` con pulizia automatica oltre i 30 giorni)

7. Docker & persistenza dati
   - Immagine Docker basata su `python:3.9-slim`
   - `docker-compose.yml` espone la porta **5555** e monta volumi:
     - `./instance:/app/instance` per il database SQLite
     - `./backups:/app/backups` per i backup
     - `./:/app` per lo sviluppo live

---

## Tecnologie e Dipendenze

- **Flask** – microframework web Python
- **Flask-SQLAlchemy** – ORM per SQLite
- **Flask-Migrate / Alembic** – migrazioni del database
- **Flask-WTF / WTForms** – gestione e validazione dei form
- **openpyxl** – esportazione Excel
- **icalendar** – generazione di file iCal
- **schedule** – scheduler per backup automatici

---

## Installazione e Avvio

### Ambiente locale
```bash
git clone <repo-url>
cd app-esami
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Avvio in sviluppo (porta 5000)
export FLASK_APP=app.py
flask run
# Oppure su porta 5005 (script incluso)
chmod +x start_port5005.sh
./start_port5005.sh
```

### Con Docker
```bash
docker-compose build
docker-compose up -d
```
L’app sarà raggiungibile su **http://localhost:5555**

Per spegnere o rimuovere i container:
```bash
docker-compose down
```

---

## Struttura delle Route (endpoints)

- **`GET /`** – dashboard principale
- **`GET /calendario`** – vista calendario interattivo
- **Esami CRUD**:
  - `GET /nuovo_esame`, `POST /nuovo_esame`
  - `GET /esame/<id>`, `GET|POST /esame/<id>/modifica`, `POST /esame/<id>/elimina`
- **Date aggiuntive**:
  - `POST /esame/<id>/aggiungi_data`, `POST /data_aggiuntiva/<id>/elimina`
- **Commissioni**:
  - `POST /esame/<id>/aggiungi_commissione`
  - `GET|POST /commissione/<id>/modifica`, `POST /commissione/<id>/elimina`
- **Membri commissione**:
  - `GET /membri_commissioni`
  - `GET|POST /nuovo_membro_commissione`
  - `GET /membro_commissione/<id>`, `GET|POST /membro_commissione/<id>/modifica`, `POST /membro_commissione/<id>/elimina`, `POST /membro_commissione/<id>/aggiungi_commissioni`
- **Esportazioni**:
  - `GET /scarica_calendario`, `/scarica_excel`, `/scarica_excel_date`, `/scarica_excel_commissioni`
- **Backup**:
  - `POST /backup_database`

---

## Licenza

GPLv3 © [Daniele Dragoni] 2025
