#!/bin/bash

# Robot Arm Control - Avvio Rapido per Mac
# Fai doppio click per avviare!

echo "================================================"
echo "   🤖 RoboArm Studio"
echo "================================================"
echo ""

# Trova la directory dello script
cd "$(dirname "$0")"

# Controlla se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato!"
    echo "Installa Python da: https://www.python.org/downloads/"
    read -p "Premi INVIO per uscire..."
    exit 1
fi

echo "✅ Python trovato: $(python3 --version)"
echo ""

# Crea virtual environment se non esiste
if [ ! -d "venv" ]; then
    echo "📦 Creazione virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment creato"
fi

# Attiva il virtual environment
echo "🔧 Attivazione virtual environment..."
source venv/bin/activate

# Controlla e installa le dipendenze
echo "📦 Controllo dipendenze..."
if ! python -c "import flask" 2>/dev/null || ! python -c "import serial" 2>/dev/null; then
    echo "⚙️  Installazione dipendenze..."
    pip install -q -r requirements.txt
    echo "✅ Dipendenze installate"
else
    echo "✅ Dipendenze OK"
fi

echo ""

# Controlla se Arduino è collegato
echo "🔍 Ricerca Arduino..."
if ls /dev/cu.usbmodem* 1> /dev/null 2>&1 || ls /dev/cu.usbserial* 1> /dev/null 2>&1; then
    echo "✅ Arduino trovato!"
else
    echo "⚠️  Arduino non rilevato. Collegalo via USB prima di connetterti."
fi
echo ""

# Avvia il server
echo "🚀 Avvio server..."
echo "📱 Apri il browser su: http://localhost:5001"
echo ""
echo "Premi Ctrl+C per fermare il server"
echo "================================================"
echo ""

python robot_arm_server.py
