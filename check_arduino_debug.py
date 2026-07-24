#!/usr/bin/env python3
"""
Script per verificare se Arduino sta ricevendo i comandi
e se il firmware aggiornato è stato caricato correttamente
"""

import serial
import time
import sys

PORT = '/dev/cu.usbmodemB43A453577942'
BAUD_RATE = 9600

print("=" * 60)
print("🔍 VERIFICA DEBUG ARDUINO")
print("=" * 60)
print()
print("Questo script verifica se:")
print("  1. Arduino riceve i comandi dal Python")
print("  2. Il firmware aggiornato è caricato (con debug seriale)")
print()
print(f"Porta: {PORT}")
print(f"Baud Rate: {BAUD_RATE}")
print()

try:
    # Chiudi eventuali connessioni esistenti
    print("⏳ Connessione ad Arduino...")
    ser = serial.Serial(PORT, BAUD_RATE, timeout=2)
    time.sleep(2)  # Attendi inizializzazione Arduino
    print("✅ Connesso!")
    print()
    
    # Svuota buffer
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    print("📤 Invio comando test: 45 90 90 90 90 90 35")
    command = "45 90 90 90 90 90 35\n"
    ser.write(command.encode())
    ser.flush()
    print("✅ Comando inviato")
    print()
    
    print("📥 Ascolto risposta da Arduino (5 secondi)...")
    print("   Se vedi 'RX: 45,90,90,90,90,90,35' → Firmware aggiornato OK!")
    print("   Se non vedi nulla → Firmware NON aggiornato")
    print()
    print("-" * 60)
    
    start_time = time.time()
    received_data = False
    
    while time.time() - start_time < 5:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Arduino: {line}")
                received_data = True
        time.sleep(0.1)
    
    print("-" * 60)
    print()
    
    if received_data:
        print("✅ SUCCESSO!")
        print("   Arduino sta rispondendo con debug seriale")
        print("   Il firmware aggiornato è stato caricato correttamente!")
        print()
        print("   Se i servo non si muovono, controlla:")
        print("   - Alimentazione esterna dei servo")
        print("   - Connessioni fisiche")
        print("   - Che i servo non siano bloccati meccanicamente")
    else:
        print("❌ PROBLEMA!")
        print("   Arduino NON sta inviando debug seriale")
        print()
        print("   Possibili cause:")
        print("   1. Firmware NON aggiornato (più probabile)")
        print("   2. Baud rate errato")
        print("   3. Problema di comunicazione seriale")
        print()
        print("   SOLUZIONE:")
        print("   1. Disconnetti dal server web")
        print("   2. Apri Arduino IDE")
        print("   3. Carica RoboArm_Studio.ino")
        print("   4. Attendi 'Done uploading'")
        print("   5. Riconnetti dal server web")
    
    ser.close()
    print()
    
except serial.SerialException as e:
    print(f"❌ ERRORE: Impossibile connettersi ad Arduino")
    print(f"   {e}")
    print()
    print("   Possibili cause:")
    print("   - Il server web sta usando la porta")
    print("   - Arduino non collegato")
    print("   - Porta errata")
    print()
    print("   SOLUZIONE:")
    print("   1. Disconnetti dal server web (http://localhost:5001)")
    print("   2. Riprova questo script")
    sys.exit(1)

except KeyboardInterrupt:
    print()
    print("⚠️  Interrotto dall'utente")
    if 'ser' in locals():
        ser.close()
    sys.exit(0)

print("=" * 60)


