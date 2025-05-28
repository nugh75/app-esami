#!/bin/bash

# Script di avvio per l'applicazione Gestione Esami PEF
echo "🎓 Avvio Applicazione Gestione Esami PEF"
echo "========================================"

# Controllo se esiste l'ambiente virtuale
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtuale non trovato. Creazione in corso..."
    python3 -m venv venv
    echo "✅ Ambiente virtuale creato"
fi

# Attivazione ambiente virtuale
echo "🔧 Attivazione ambiente virtuale..."
source venv/bin/activate

# Installazione/aggiornamento dipendenze
echo "📦 Installazione dipendenze..."
pip install -r requirements.txt

# Controllo database
if [ ! -f "instance/esami_pef.db" ]; then
    echo "🗄️  Inizializzazione database..."
    python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database inizializzato!')"
fi

# Avvio applicazione
echo "🚀 Avvio dell'applicazione..."
echo "📱 L'applicazione sarà disponibile su: http://127.0.0.1:5000"
echo "🛑 Premi Ctrl+C per fermare l'applicazione"
echo ""

python app.py
