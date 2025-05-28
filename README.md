# Gestione Esami PEF - Applicazione Web

Un'applicazione web sviluppata in Python Flask per la gestione degli esami del percorso PEF (Percorsi di formazione per l'acquisizione di 60 CFU) per classe di concorso, con particolare attenzione alle esigenze delle commissioni d'esame.

## Caratteristiche principali

### 🎯 Funzionalità
- **Gestione completa esami**: Creazione, modifica ed eliminazione degli esami PEF
- **Calendario attività**: Pianificazione di tutte le attività delle commissioni (definizione argomenti, prove scritte, lezioni simulate, ecc.)
- **Gestione commissioni**: Composizione dettagliata delle commissioni con ruoli e profili
- **Dashboard statistiche**: Visualizzazione in tempo reale dei dati sulle attività e commissioni
- **Export dati**: Esportazione di date e commissioni in formato Excel

### 📊 Statistiche e monitoraggio
- Numero di esami per modalità (online, in presenza, mista)
- Distribuzione dei membri di commissione per ruolo e profilo
- Ripartizione delle attività per tipologia (prove scritte, lezioni simulate, ecc.)
- Filtri avanzati per classe di concorso e modalità

### 🧩 Tipi di attività supportati
- Definizione argomento prova scritta
- Definizione argomento lezione simulata
- Definizione criteri e griglie di valutazione
- Prova scritta (in presenza)
- Prova scritta (consegna)
- Valutazione prova scritta
- Lezione simulata (in presenza)
- Altri tipi di attività personalizzabili

## Tecnologie utilizzate

### 🛠️ Stack tecnologico
- **Backend**: Python Flask
- **Database**: SQLite con SQLAlchemy ORM
- **Frontend**: Bootstrap con Material Design Icons
- **Forms**: Flask-WTF con validazione
- **Export**: openpyxl (Excel), icalendar (iCal)
- **Migrazioni DB**: Flask-Migrate (Alembic)

## Installazione e avvio

### Prerequisiti
- Python 3.8+
- pip

### Setup
```bash
# Clone del repository
git clone https://github.com/username/app-esami.git
cd app-esami

# Creazione ambiente virtuale
python3 -m venv venv

# Attivazione ambiente virtuale
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

# Installazione dipendenze
pip install -r requirements.txt

# Avvio applicazione (porta standard 5000)
python app.py
```

Oppure utilizzare lo script di avvio per la porta 5005:
```bash
# Permessi di esecuzione
chmod +x start_port5005.sh

# Avvio su porta 5005
./start_port5005.sh
```

L'applicazione sarà disponibile su `http://127.0.0.1:5000` (o porta 5005 se si utilizza lo script alternativo)

## Funzionalità principali

### 1. Dashboard con statistiche
- Panoramica completa degli esami programmati
- Statistiche in tempo reale sugli esami, commissioni e tipi di attività
- Filtri di ricerca avanzati

### 2. Gestione esami
- Creazione e modifica degli esami per classe di concorso
- Pianificazione date e orari
- Aggiunta di attività specifiche per ogni data (riunioni commissione, prove, lezioni simulate)

### 3. Commissioni d'esame
- Composizione dettagliata della commissione
- Supporto per titolari e supplenti
- Gestione dei profili dei membri (docenti interni, esterni, referenti USR, ecc.)

### 4. Export dati
- **Excel Date**: Esportazione di tutte le date degli esami con dettagli su attività
- **Excel Commissioni**: Esportazione dei membri delle commissioni con un record per classe di concorso
- **Calendario**: Download di file .ics per importazione in applicazioni calendario

## Classi di concorso supportate

L'applicazione supporta tutte le principali classi di concorso, tra cui:
- A001, A007, A008, A011, A012, A013, A017, A018, A019, A020
- A022, A023, A026, A027, A028, A029, A030, A037, A040, A042
- A045, A046, A050, A053, A054, A060, A061, A063, A064
- AA24, AB24, AC24, AL24, B015

## Manutenzione

### Backup
L'applicazione genera automaticamente backup del database durante le operazioni di migrazione.
I backup si trovano nella cartella `instance/` e seguono la convenzione:
```
esami_pef_backup_[tipo]_[data]_[ora].db
```

### Migrazioni
Quando viene modificata la struttura del database, viene generato un file di migrazione nella cartella `migrations/versions/`.

## Supporto e contributi

Per segnalazioni di bug o richieste di funzionalità, contattare gli amministratori del progetto.

## Licenza

Questo progetto è distribuito sotto licenza MIT.
