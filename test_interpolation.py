#!/usr/bin/env python3
"""
Test script per verificare l'interpolazione dei movimenti
Esegue una serie di movimenti di test per valutare la fluidità
"""

import requests
import time
import sys

API_BASE = "http://localhost:5001"

def check_connection():
    """Verifica che il server sia in esecuzione e Arduino connesso"""
    try:
        response = requests.get(f"{API_BASE}/api/status")
        data = response.json()
        if not data.get('connected'):
            print("❌ Arduino non connesso!")
            print("   Connetti l'Arduino dall'interfaccia web prima di eseguire i test")
            return False
        print("✅ Arduino connesso")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server non raggiungibile!")
        print("   Avvia il server con: python3 robot_arm_server.py")
        return False

def move_servo(servo_id, angle):
    """Muove un servo alla posizione specificata"""
    try:
        response = requests.post(
            f"{API_BASE}/api/move",
            json={"servo": servo_id, "angle": angle}
        )
        return response.json().get('success', False)
    except Exception as e:
        print(f"❌ Errore movimento: {e}")
        return False

def load_preset(preset_name):
    """Carica una posizione preset"""
    try:
        response = requests.post(f"{API_BASE}/api/preset/{preset_name}")
        return response.json().get('success', False)
    except Exception as e:
        print(f"❌ Errore caricamento preset: {e}")
        return False

def test_single_servo():
    """Test 1: Movimento singolo servo"""
    print("\n" + "="*60)
    print("TEST 1: Movimento Singolo Servo (Root)")
    print("="*60)
    print("Questo test muove il servo root da 0° a 180° e ritorno")
    print("Osserva la fluidità del movimento e l'assenza di vibrazioni")
    
    input("\nPremi INVIO per iniziare...")
    
    angles = [0, 45, 90, 135, 180, 135, 90, 45, 0]
    for angle in angles:
        print(f"  → Movimento a {angle}°...")
        if move_servo(0, angle):
            time.sleep(2)  # Attendi che il movimento si completi
        else:
            print("  ❌ Movimento fallito")
            return False
    
    print("✅ Test completato")
    return True

def test_multiple_servos():
    """Test 2: Movimento multiplo coordinato"""
    print("\n" + "="*60)
    print("TEST 2: Movimento Multiplo Coordinato")
    print("="*60)
    print("Questo test muove più servo contemporaneamente")
    print("Osserva come l'interpolazione gestisce movimenti simultanei")
    
    input("\nPremi INVIO per iniziare...")
    
    # Sequenza di movimenti coordinati
    movements = [
        (0, 45, "Root a 45°"),
        (1, 120, "Arm A1 a 120°"),
        (3, 60, "Arm B a 60°"),
        (4, 45, "Wrist A a 45°"),
    ]
    
    for servo_id, angle, description in movements:
        print(f"  → {description}...")
        if move_servo(servo_id, angle):
            time.sleep(1.5)
        else:
            print("  ❌ Movimento fallito")
            return False
    
    print("\n  → Ritorno alla posizione home...")
    load_preset("home")
    time.sleep(2)
    
    print("✅ Test completato")
    return True

def test_gripper():
    """Test 3: Test gripper"""
    print("\n" + "="*60)
    print("TEST 3: Test Gripper")
    print("="*60)
    print("Questo test apre e chiude il gripper gradualmente")
    
    input("\nPremi INVIO per iniziare...")
    
    print("  → Apertura completa (0°)...")
    move_servo(6, 0)
    time.sleep(2)
    
    print("  → Chiusura parziale (35°)...")
    move_servo(6, 35)
    time.sleep(2)
    
    print("  → Chiusura completa (70°)...")
    move_servo(6, 70)
    time.sleep(2)
    
    print("  → Ritorno a posizione intermedia (35°)...")
    move_servo(6, 35)
    time.sleep(2)
    
    print("✅ Test completato")
    return True

def test_presets():
    """Test 4: Test posizioni preset"""
    print("\n" + "="*60)
    print("TEST 4: Test Posizioni Preset")
    print("="*60)
    print("Questo test carica tutte le posizioni preset")
    print("Osserva la fluidità delle transizioni tra posizioni")
    
    input("\nPremi INVIO per iniziare...")
    
    presets = [
        ("home", "Home (posizione iniziale)"),
        ("rest", "Rest (riposo)"),
        ("reach", "Reach (estensione)"),
        ("grab", "Grab (afferrare)"),
        ("home", "Home (ritorno)")
    ]
    
    for preset_name, description in presets:
        print(f"  → Caricamento {description}...")
        if load_preset(preset_name):
            time.sleep(3)  # Più tempo per movimenti complessi
        else:
            print("  ❌ Caricamento fallito")
            return False
    
    print("✅ Test completato")
    return True

def test_stress():
    """Test 5: Test di stress (movimenti rapidi)"""
    print("\n" + "="*60)
    print("TEST 5: Test di Stress")
    print("="*60)
    print("Questo test esegue movimenti rapidi e ripetuti")
    print("Verifica la stabilità del sistema sotto carico")
    
    response = input("\nQuesto test è più intenso. Continuare? (s/n): ")
    if response.lower() != 's':
        print("Test saltato")
        return True
    
    print("\n  → Esecuzione 10 movimenti rapidi del root...")
    for i in range(10):
        angle = 45 if i % 2 == 0 else 135
        print(f"    Movimento {i+1}/10 a {angle}°")
        move_servo(0, angle)
        time.sleep(1)  # Tempo ridotto per stress test
    
    print("\n  → Ritorno alla posizione home...")
    load_preset("home")
    time.sleep(2)
    
    print("✅ Test completato")
    return True

def main():
    """Esegue tutti i test"""
    print("="*60)
    print("TEST INTERPOLAZIONE MOVIMENTI - RoboArm Studio")
    print("="*60)
    print("\nQuesto script testa il sistema di interpolazione dei movimenti")
    print("Assicurati che:")
    print("  1. Il server sia in esecuzione (python3 robot_arm_server.py)")
    print("  2. L'Arduino sia connesso")
    print("  3. Il braccio robotico sia in una posizione sicura")
    
    # Verifica connessione
    if not check_connection():
        sys.exit(1)
    
    # Menu test
    tests = [
        ("1", "Movimento Singolo Servo", test_single_servo),
        ("2", "Movimento Multiplo Coordinato", test_multiple_servos),
        ("3", "Test Gripper", test_gripper),
        ("4", "Test Posizioni Preset", test_presets),
        ("5", "Test di Stress", test_stress),
        ("A", "Esegui Tutti i Test", None),
    ]
    
    while True:
        print("\n" + "="*60)
        print("MENU TEST")
        print("="*60)
        for code, name, _ in tests:
            print(f"  [{code}] {name}")
        print("  [Q] Esci")
        
        choice = input("\nScegli un test: ").upper()
        
        if choice == 'Q':
            print("\n👋 Arrivederci!")
            break
        elif choice == 'A':
            print("\n🚀 Esecuzione di tutti i test...")
            for code, name, test_func in tests[:-1]:  # Escludi "Tutti i test"
                if not test_func():
                    print(f"\n❌ Test '{name}' fallito!")
                    break
            else:
                print("\n" + "="*60)
                print("✅ TUTTI I TEST COMPLETATI CON SUCCESSO!")
                print("="*60)
        else:
            # Trova e esegui il test selezionato
            for code, name, test_func in tests:
                if choice == code and test_func:
                    test_func()
                    break
            else:
                print("❌ Scelta non valida")
    
    # Ritorna alla home prima di uscire
    print("\n🏠 Ritorno alla posizione home...")
    load_preset("home")
    time.sleep(2)
    print("✅ Fatto!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrotto dall'utente")
        print("🏠 Ritorno alla posizione home...")
        load_preset("home")
        time.sleep(2)
        print("✅ Fatto!")


