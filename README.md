# Gestione Esami PEF - Applicazione Web

Un'applicazione web sviluppata in Python Flask con Material Design per la gestione degli esami del percorso PEF (Percorsi di formazione per l'acquisizione di 60, 30 o 36 CFU) per classe di concorso.

## Caratteristiche

### 🎯 Funzionalità Principali
- **Gestione Completa Esami**: Creazione, modifica ed eliminazione degli esami PEF
- **Classi di Concorso**: Supporto per tutte le classi di concorso (A001, A007, A008, ecc.)
- **Percorsi PEF**: Gestione di tutti i percorsi formativi DPCM 4 agosto 2023
- **Date Multiple**: Possibilità di aggiungere date aggiuntive per ogni esame
- **Modalità Flessibili**: Supporto per esami online e in presenza
- **Commissioni**: Gestione membri commissione con evidenziazione esterni USR Lazio

### 🔍 Ricerca e Filtri
- Ricerca testuale per classe, sede, note
- Filtri per classe di concorso, percorso PEF, modalità
- Dashboard con statistiche in tempo reale

### 📊 Export e Download
- **Calendario iCal**: Download di calendario compatibile con Google Calendar, Outlook
- **File Excel**: Export completo di tutti i dati in formato xlsx
- **API JSON**: Endpoint per integrazione con altre applicazioni

### 🎨 Interfaccia Utente
- **Material Design**: Interfaccia moderna e responsiva
- **Bootstrap**: Layout professionale e mobile-friendly
- **Icone Material Design**: Set completo di icone intuitive

## Struttura Tecnica

### 🛠️ Tecnologie
- **Backend**: Python Flask
- **Database**: SQLite con SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap, Material Design
- **Forms**: Flask-WTF con validazione
- **Export**: openpyxl (Excel), icalendar (iCal)

### 📁 Struttura Progetto
```
app-esami/
├── app.py                 # Applicazione Flask principale
├── config.py             # Configurazioni ambiente
├── requirements.txt      # Dipendenze Python
├── instance/
│   └── esami_pef.db      # Database SQLite
├── templates/            # Template HTML
│   ├── base.html
│   ├── index.html
│   ├── nuovo_esame.html
│   ├── dettaglio_esame.html
│   └── modifica_esame.html
└── venv/                 # Ambiente virtuale Python
```

## Installazione e Avvio

### Prerequisiti
- Python 3.8+
- pip

### Setup
```bash
# Clone del repository
cd /path/to/project

# Creazione ambiente virtuale
python3 -m venv venv

# Attivazione ambiente virtuale
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

# Installazione dipendenze
pip install -r requirements.txt

# Avvio applicazione
python app.py
```

L'applicazione sarà disponibile su `http://127.0.0.1:5000`

## Utilizzo

### 1. Dashboard Principale
- Visualizzazione di tutti gli esami programmati
- Statistiche in tempo reale (totale esami, online/presenza, commissioni)
- Filtri di ricerca avanzati

### 2. Creazione Nuovo Esame
- Selezione classe di concorso dal menu a tendina
- Scelta del percorso PEF appropriato
- Impostazione data/ora inizio e fine
- Definizione modalità (online/presenza) e sede

### 3. Gestione Commissioni
- Aggiunta membri commissione
- Definizione ruoli
- Marcatura membri esterni USR Regione Lazio

### 4. Date Aggiuntive
- Possibilità di programmare sessioni multiple per lo stesso esame
- Modalità diverse per ogni sessione

### 5. Export Dati
- **Calendario**: Download file .ics importabile in qualsiasi calendario
- **Excel**: Export completo con tutti i dettagli in formato .xlsx

## Classi di Concorso Supportate

L'applicazione supporta tutte le classi di concorso incluse nel bando PEF:

**Classe A (Scuola Secondaria)**
- A001 – Arte e immagine nella scuola secondaria di I grado
- A007 – Discipline audiovisive
- A008 – Discipline geometriche, architettura, design d'arredamento e scenotecnica
- A011 – Discipline letterarie e latino
- A012 – Discipline letterarie negli istituti di istruzione secondaria di II grado
- A013 – Discipline letterarie, latino e greco
- A017 – Disegno e storia dell'arte
- A018 – Filosofia e scienze umane
- A019 – Filosofia e storia
- A020 – Fisica
- A022 – Italiano, storia, geografia nella scuola secondaria di I grado
- A023 – Lingua italiana per discenti di lingua straniera (alloglotti)
- A026 – Matematica
- A027 – Matematica e fisica
- A028 – Matematica e scienze
- A029 – Musica negli istituti di istruzione secondaria di II grado
- A030 – Musica nella scuola secondaria di I grado
- A037 – Scienze e tecnologie delle costruzioni, tecnologie e tecniche di rappresentazione grafica
- A040 – Tecnologie elettriche elettroniche
- A042 – Scienze e tecnologie meccaniche
- A045 – Scienze economico-aziendali
- A046 – Scienze giuridico-economiche
- A050 – Scienze naturali, chimiche e biologiche
- A053 – Storia della musica
- A054 – Storia dell'arte
- A060 – Tecnologia nella scuola secondaria di I grado
- A061 – Tecnologie e tecniche delle comunicazioni multimediali
- A063 – Tecnologie musicali
- A064 – Teoria, analisi e composizione

**Lingue Straniere**
- AA24 – Lingua e cultura straniera (francese)
- AB24 – Lingua e cultura straniera (inglese)
- AC24 – Lingua e cultura straniera (spagnolo)
- AL24 – Lingua e cultura straniera (arabo)

**Classe B (Laboratori)**
- B015 – Laboratori di scienze e tecnologie elettriche ed elettroniche

## Percorsi PEF

- **PeF 60 CFU All. 1** - DPCM 4 ago 2023
- **PeF 30 CFU All. 2** - DPCM 4 ago 2023
- **PeF 36 CFU All. 5** - DPCM 4 ago 2023
- **PeF 30 CFU Art. 13** - DPCM 4 ago 2023

## API Endpoints

L'applicazione espone API REST per integrazione:

- `GET /api/classi-concorso` - Lista classi di concorso
- `GET /api/percorsi-pef` - Lista percorsi PEF
- `GET /api/esami` - Lista completa esami in JSON

## Configurazione

Il file `config.py` permette di configurare:
- Chiavi segrete
- Database URI
- Limiti upload file
- Durata sessioni
- Configurazioni ambiente (development/production/testing)

## Sicurezza

- Validazione form con Flask-WTF
- Protezione CSRF
- Sanitizzazione input utente
- Configurazioni separate per ambienti

## Supporto e Contributi

Per segnalazioni di bug o richieste di funzionalità, aprire una issue nel repository.

## Licenza

Questo progetto è distribuito sotto licenza MIT.
