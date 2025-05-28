#!/bin/bash

# Script personalizzato per avviare l'applicazione Gestione Esami PEF sulla porta 5005
echo "🎓 Avvio Applicazione Gestione Esami PEF"
echo "========================================"

# Attivazione ambiente virtuale
echo "🔧 Attivazione ambiente virtuale..."
source venv/bin/activate

# Avvio applicazione sulla porta 5005
echo "🚀 Avvio dell'applicazione..."
echo "📱 L'applicazione sarà disponibile su: http://127.0.0.1:5005"
echo "🛑 Premi Ctrl+C per fermare l'applicazione"
echo ""

python -c "from app import app; app.run(port=5005, debug=True)"
