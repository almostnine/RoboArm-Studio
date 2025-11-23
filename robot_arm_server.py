#!/usr/bin/env python3
"""
Robot Arm Web Control Server
Interfaccia web per controllare il braccio robotico Arduino
Compatible with Mac, Windows, Linux
"""

from flask import Flask, render_template, request, jsonify
import serial
import serial.tools.list_ports
import threading
import time

app = Flask(__name__)

# Variabili globali
arduino = None
current_angles = [90, 90, 90, 90, 90, 35]  # Posizione iniziale (servo 0-4 a 90°, gripper a 35°)
is_connected = False
arduino_lock = threading.Lock()

def find_arduino_port():
    """Trova automaticamente la porta dell'Arduino"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Su Mac, le porte Arduino sono tipicamente /dev/cu.usbmodem* o /dev/cu.usbserial*
        if 'usbmodem' in port.device or 'usbserial' in port.device or 'Arduino' in port.description:
            return port.device
    return None

def connect_arduino(port=None):
    """Connette all'Arduino"""
    global arduino, is_connected
    
    try:
        if port is None:
            port = find_arduino_port()
            
        if port is None:
            print("Arduino non trovato. Porta disponibili:")
            for p in serial.tools.list_ports.comports():
                print(f"  - {p.device}: {p.description}")
            return False
            
        arduino = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)  # Aspetta che Arduino si inizializzi
        is_connected = True
        print(f"Connesso ad Arduino su porta: {port}")
        return True
        
    except Exception as e:
        print(f"Errore connessione Arduino: {e}")
        is_connected = False
        return False

def send_angles(angles):
    """Invia gli angoli all'Arduino"""
    global arduino, is_connected
    
    if not is_connected or arduino is None:
        return False
        
    try:
        with arduino_lock:
            # Assicuriamoci che tutti gli angoli siano interi e nel range corretto
            angles_int = [int(round(a)) for a in angles]
            # Verifica range: servo 0-4 hanno range 0-180, gripper (servo 5) ha range 0-70
            for i in range(len(angles_int)):
                if i == 5:  # Gripper
                    angles_int[i] = max(0, min(70, angles_int[i]))
                else:  # Altri servo
                    angles_int[i] = max(0, min(180, angles_int[i]))
            
            # Formatta il comando: 6 numeri interi separati da spazi
            command = ' '.join(map(str, angles_int)) + '\n'
            
            # Debug: stampa il comando completo inviato con mappatura pin
            pinMapping = ['Pin 3', 'Pin 4', 'Pin 6', 'Pin 9', 'Pin 10', 'Pin 11']
            print(f"[DEBUG] Comando completo inviato: {command.strip()}")
            print(f"[DEBUG] Mappatura: Servo 0-5 → {pinMapping}")
            print(f"[DEBUG] Valore Pin 9 (Servo 3): {angles_int[3]}°")
            
            arduino.write(command.encode())
            arduino.flush()
        return True
    except Exception as e:
        print(f"Errore invio dati: {e}")
        is_connected = False
        return False

@app.route('/')
def index():
    """Pagina principale"""
    return render_template('index.html')

@app.route('/api/connect', methods=['POST'])
def api_connect():
    """Endpoint per connettere all'Arduino"""
    data = request.json
    port = data.get('port', None)
    
    success = connect_arduino(port)
    return jsonify({
        'success': success,
        'connected': is_connected,
        'message': 'Connesso!' if success else 'Connessione fallita'
    })

@app.route('/api/disconnect', methods=['POST'])
def api_disconnect():
    """Endpoint per disconnettere dall'Arduino"""
    global arduino, is_connected
    
    try:
        if arduino:
            arduino.close()
        is_connected = False
        return jsonify({'success': True, 'message': 'Disconnesso'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/ports', methods=['GET'])
def api_ports():
    """Lista le porte seriali disponibili"""
    ports = serial.tools.list_ports.comports()
    port_list = [{'device': p.device, 'description': p.description} for p in ports]
    return jsonify({'ports': port_list})

@app.route('/api/status', methods=['GET'])
def api_status():
    """Stato della connessione"""
    return jsonify({
        'connected': is_connected,
        'angles': current_angles
    })

@app.route('/api/move', methods=['POST'])
def api_move():
    """Muove i servo"""
    global current_angles
    
    if not is_connected:
        return jsonify({'success': False, 'message': 'Arduino non connesso'})
    
    data = request.json
    servo_id = data.get('servo')
    angle = data.get('angle')
    
    if servo_id is not None and angle is not None:
        # Converti angle in intero e assicurati che sia nel range corretto
        angle = int(round(float(angle)))
        
        # Validazione: servo 0-4 hanno range 0-180, gripper (servo 5) ha range 0-70
        if servo_id == 5:
            angle = max(0, min(70, angle))  # Clamp tra 0 e 70 per gripper
        else:
            angle = max(0, min(180, angle))  # Clamp tra 0 e 180 per altri servo
        
        # Aggiorna l'angolo del servo specifico
        if 0 <= servo_id < 6:
            servoNames = ['Root (Pin 3)', 'Arm A1 (Pin 4)', 'Arm B (Pin 6)', 'Wrist A (Pin 9)', 'Wrist B (Pin 10)', 'Gripper (Pin 11)']
            print(f"[DEBUG] Movimento servo {servo_id} ({servoNames[servo_id]}) a {angle}°")
            current_angles[servo_id] = angle
            print(f"[DEBUG] Angoli attuali prima invio: {current_angles}")
            success = send_angles(current_angles)
            if servo_id == 3:  # Pin 9 - Wrist A
                print(f"[DEBUG] ⚠️ ATTENZIONE: Comando inviato per Pin 9 (Servo 3) = {angle}°")
            return jsonify({
                'success': success,
                'angles': current_angles
            })
    
    return jsonify({'success': False, 'message': 'Parametri non validi'})

@app.route('/api/set_all', methods=['POST'])
def api_set_all():
    """Imposta tutti i servo contemporaneamente"""
    global current_angles
    
    if not is_connected:
        return jsonify({'success': False, 'message': 'Arduino non connesso'})
    
    data = request.json
    angles = data.get('angles')
    
    if angles and len(angles) == 6:
        # Verifica che tutti gli angoli siano validi
        # Validazione: servo 0-4 hanno range 0-180, gripper (servo 5) ha range 0-70
        angles_validated = []
        for i, a in enumerate(angles):
            if i == 5:  # Gripper
                angles_validated.append(max(0, min(70, int(round(float(a))))))
            else:  # Altri servo
                angles_validated.append(max(0, min(180, int(round(float(a))))))
        
        if all(0 <= a <= 180 for a in angles_validated[:5]) and 0 <= angles_validated[5] <= 70:
            current_angles = angles_validated
            success = send_angles(current_angles)
            return jsonify({
                'success': success,
                'angles': current_angles
            })
    
    return jsonify({'success': False, 'message': 'Angoli non validi'})

@app.route('/api/preset/<preset_name>', methods=['POST'])
def api_preset(preset_name):
    """Carica posizioni predefinite"""
    global current_angles
    
    presets = {
        'home': [90, 90, 90, 90, 90, 35],  # Posizione iniziale (servo 0-4 a 90°, gripper a 35°)
        'rest': [90, 30, 30, 90, 90, 0],  # Posizione di riposo (gripper aperto a 0°)
        'reach': [90, 120, 120, 60, 90, 35],  # Posizione di estensione (gripper semi-aperto)
        'grab': [90, 90, 90, 90, 90, 70]  # Posizione per afferrare (gripper chiuso a 70°)
    }
    
    if preset_name in presets:
        current_angles = presets[preset_name]
        success = send_angles(current_angles)
        return jsonify({
            'success': success,
            'angles': current_angles,
            'preset': preset_name
        })
    
    return jsonify({'success': False, 'message': 'Preset non trovato'})

if __name__ == '__main__':
    print("=" * 50)
    print("Robot Arm Web Control Server")
    print("=" * 50)
    print("\nPer utilizzare:")
    print("1. Collega l'Arduino via USB")
    print("2. Apri il browser su: http://localhost:5001")
    print("3. Clicca 'Connetti' per trovare automaticamente Arduino")
    print("\n" + "=" * 50 + "\n")
    
    # Avvia il server Flask (porta 5001 per evitare conflitto con AirPlay)
    app.run(host='0.0.0.0', port=5001, debug=True)
