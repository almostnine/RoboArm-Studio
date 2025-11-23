#!/usr/bin/env python3
"""
RoboArm Studio - Web Control Server
Professional web interface to control Arduino robotic arm
Compatible with Mac, Windows, Linux
"""

import os
from flask import Flask, render_template, request, jsonify
import serial
import serial.tools.list_ports
import threading
import time
import json

app = Flask(__name__)

# Configuration
DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5001))

# Global variables
arduino = None
current_angles = [90, 90, 90, 90, 90, 90, 35]  # Initial position (7 servos: 0-5 at 90°, gripper at 35°)
target_angles = [90, 90, 90, 90, 90, 90, 35]  # Target position for smooth movement
is_connected = False
arduino_lock = threading.Lock()
movement_lock = threading.Lock()  # Lock to prevent simultaneous movements
is_moving = False  # Flag to indicate if a movement is in progress

# Smooth movement parameters
MOVEMENT_STEP = 1  # Degrees per step (smaller = smoother)
MOVEMENT_DELAY = 0.02  # Delay between steps in seconds (larger = slower, default 0.02 = 20ms)

# Custom positions storage file
POSITIONS_FILE = 'saved_positions.json'

def load_saved_positions():
    """Load saved positions from file"""
    if os.path.exists(POSITIONS_FILE):
        try:
            with open(POSITIONS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading positions: {e}")
            return {}
    return {}

def save_positions(positions):
    """Save positions to file"""
    try:
        with open(POSITIONS_FILE, 'w') as f:
            json.dump(positions, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving positions: {e}")
        return False

def find_arduino_port():
    """Automatically find Arduino port"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # On Mac, Arduino ports are typically /dev/cu.usbmodem* or /dev/cu.usbserial*
        if 'usbmodem' in port.device or 'usbserial' in port.device or 'Arduino' in port.description:
            return port.device
    return None

def connect_arduino(port=None):
    """Connect to Arduino"""
    global arduino, is_connected
    
    try:
        if port is None:
            port = find_arduino_port()
            
        if port is None:
            print("Arduino not found. Available ports:")
            for p in serial.tools.list_ports.comports():
                print(f"  - {p.device}: {p.description}")
            return False
            
        arduino = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)  # Wait for Arduino to initialize
        is_connected = True
        print(f"Connected to Arduino on port: {port}")
        return True
        
    except Exception as e:
        print(f"Arduino connection error: {e}")
        is_connected = False
        return False

def send_angles(angles, immediate=False):
    """Send angles to Arduino"""
    global arduino, is_connected
    
    if not is_connected or arduino is None:
        return False
        
    try:
        with arduino_lock:
            # Ensure all angles are integers and in correct range
            angles_int = [int(round(a)) for a in angles]
            # Validate range: servo 0-5 have range 0-180, gripper (servo 6) has range 0-70
            for i in range(len(angles_int)):
                if i == 6:  # Gripper
                    angles_int[i] = max(0, min(70, angles_int[i]))
                else:  # Other servos
                    angles_int[i] = max(0, min(180, angles_int[i]))
            
            # Pin 3 and Pin 4 are coupled: when one moves, the other rotates in opposite direction
            # Servo 1 (Pin 3) and Servo 2 (Pin 4) must be opposite
            # If servo 1 is at X°, servo 2 must be at (180 - X)°
            if len(angles_int) >= 3:
                # Servo 1 (index 1, Pin 3) and Servo 2 (index 2, Pin 4) are coupled
                # When servo 1 changes, servo 2 must be its opposite
                angles_int[2] = 180 - angles_int[1]
            
            # Format command: 7 integers separated by spaces
            command = ' '.join(map(str, angles_int)) + '\n'
            
            # Debug only if not a smooth movement (to avoid cluttering console)
            if immediate and DEBUG_MODE:
                pinMapping = ['Pin 2', 'Pin 3', 'Pin 4', 'Pin 5', 'Pin 6', 'Pin 7', 'Pin 8']
                print(f"[DEBUG] Full command sent: {command.strip()}")
                print(f"[DEBUG] Mapping: Servo 0-6 → {pinMapping}")
                print(f"[DEBUG] Servo 1 (Pin 3): {angles_int[1]}° | Servo 2 (Pin 4) coupled: {angles_int[2]}°")
            
            arduino.write(command.encode())
            arduino.flush()
        return True
    except Exception as e:
        print(f"Error sending data: {e}")
        is_connected = False
        return False

def move_servo_smooth(target_angles_list):
    """Move servos smoothly from current position to target"""
    global current_angles, target_angles, is_moving
    
    # Prevent simultaneous movements
    if not movement_lock.acquire(blocking=False):
        if DEBUG_MODE:
            print("[DEBUG] Movement already in progress, command ignored")
        return False
    
    try:
        is_moving = True
        target_angles = target_angles_list.copy()
        
        # Ensure servo 1 and servo 2 are coupled
        if len(target_angles) >= 3:
            target_angles[2] = 180 - target_angles[1]
        
        # Validate all angles
        for i in range(len(target_angles)):
            if i == 6:  # Gripper
                target_angles[i] = max(0, min(70, target_angles[i]))
            else:  # Other servos
                target_angles[i] = max(0, min(180, target_angles[i]))
        
        # Use a local copy of current position to avoid concurrency issues
        with arduino_lock:
            start_angles = current_angles.copy()
        
        # Calculate number of steps needed (based on largest movement)
        max_diff = 0
        for i in range(7):
            diff = abs(target_angles[i] - start_angles[i])
            if diff > max_diff:
                max_diff = diff
        
        if max_diff == 0:
            is_moving = False
            return True
        
        num_steps = int(max_diff / MOVEMENT_STEP) + 1
        if DEBUG_MODE:
            print(f"[DEBUG] Smooth movement: {num_steps} steps from {start_angles} to {target_angles}")
        
        # Smooth movement
        for step in range(num_steps + 1):
            # Calculate intermediate angles
            intermediate_angles = []
            for i in range(7):
                start_angle = start_angles[i]
                end_angle = target_angles[i]
                diff = end_angle - start_angle
                
                # Linear interpolation
                if step == num_steps:
                    # Last step: reach exactly the target position
                    intermediate_angles.append(end_angle)
                else:
                    progress = step / num_steps
                    intermediate_angles.append(start_angle + diff * progress)
            
            # Ensure servo 1 and servo 2 are coupled even in intermediate steps
            if len(intermediate_angles) >= 3:
                intermediate_angles[2] = 180 - intermediate_angles[1]
            
            # Round and validate
            for i in range(7):
                intermediate_angles[i] = int(round(intermediate_angles[i]))
                if i == 6:  # Gripper
                    intermediate_angles[i] = max(0, min(70, intermediate_angles[i]))
                else:  # Other servos
                    intermediate_angles[i] = max(0, min(180, intermediate_angles[i]))
            
            # Send intermediate position
            send_angles(intermediate_angles, immediate=False)
            
            # Update current_angles in thread-safe manner
            with arduino_lock:
                current_angles = intermediate_angles.copy()
            
            # Delay between steps (except last)
            if step < num_steps:
                time.sleep(MOVEMENT_DELAY)
        
        if DEBUG_MODE:
            print(f"[DEBUG] Smooth movement completed")
        is_moving = False
        return True
        
    except Exception as e:
        print(f"Smooth movement error: {e}")
        is_moving = False
        return False
    finally:
        movement_lock.release()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/connect', methods=['POST'])
def api_connect():
    """Endpoint to connect to Arduino"""
    data = request.json
    port = data.get('port', None)
    
    success = connect_arduino(port)
    return jsonify({
        'success': success,
        'connected': is_connected,
        'message': 'Connected!' if success else 'Connection failed'
    })

@app.route('/api/disconnect', methods=['POST'])
def api_disconnect():
    """Endpoint to disconnect from Arduino"""
    global arduino, is_connected
    
    try:
        if arduino:
            arduino.close()
        is_connected = False
        return jsonify({'success': True, 'message': 'Disconnected'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/ports', methods=['GET'])
def api_ports():
    """List available serial ports"""
    ports = serial.tools.list_ports.comports()
    port_list = [{'device': p.device, 'description': p.description} for p in ports]
    return jsonify({'ports': port_list})

@app.route('/api/status', methods=['GET'])
def api_status():
    """Connection status"""
    return jsonify({
        'connected': is_connected,
        'angles': current_angles,
        'is_moving': is_moving
    })

@app.route('/api/move', methods=['POST'])
def api_move():
    """Move servos with smooth movement"""
    global current_angles, target_angles
    
    if not is_connected:
        return jsonify({'success': False, 'message': 'Arduino not connected'})
    
    data = request.json
    servo_id = data.get('servo')
    angle = data.get('angle')
    
    if servo_id is not None and angle is not None:
        # Convert angle to integer and ensure it's in correct range
        angle = int(round(float(angle)))
        
        # Validation: servo 0-5 have range 0-180, gripper (servo 6) has range 0-70
        if servo_id == 6:
            angle = max(0, min(70, angle))  # Clamp between 0 and 70 for gripper
        else:
            angle = max(0, min(180, angle))  # Clamp between 0 and 180 for other servos
        
        # Update target angle for specific servo
        if 0 <= servo_id < 7:
            servoNames = ['Root (Pin 2)', 'Arm A1 (Pin 3)', 'Arm A2 (Pin 4)', 'Arm B (Pin 5)', 'Wrist A (Pin 6)', 'Wrist B (Pin 7)', 'Gripper (Pin 8)']
            if DEBUG_MODE:
                print(f"[DEBUG] Smooth movement servo {servo_id} ({servoNames[servo_id]}) from {current_angles[servo_id]}° to {angle}°")
            
            # Create a copy of target angles
            new_target_angles = current_angles.copy()
            new_target_angles[servo_id] = angle
            
            # If moving servo 1 (Pin 3), also update servo 2 (Pin 4) in opposite direction
            if servo_id == 1:
                new_target_angles[2] = 180 - angle
                if DEBUG_MODE:
                    print(f"[DEBUG] Servo 2 (Pin 4) coupled updated to {new_target_angles[2]}° (opposite of {angle}°)")
            # If moving servo 2 (Pin 4), also update servo 1 (Pin 3) in opposite direction
            elif servo_id == 2:
                new_target_angles[1] = 180 - angle
                if DEBUG_MODE:
                    print(f"[DEBUG] Servo 1 (Pin 3) coupled updated to {new_target_angles[1]}° (opposite of {angle}°)")
            
            # Start smooth movement in separate thread to avoid blocking response
            def move_thread():
                move_servo_smooth(new_target_angles)
            
            movement_thread = threading.Thread(target=move_thread, daemon=True)
            movement_thread.start()
            
            # Return immediately with success (movement continues in background)
            return jsonify({
                'success': True,
                'angles': new_target_angles,
                'message': 'Smooth movement started'
            })
    
    return jsonify({'success': False, 'message': 'Invalid parameters'})

@app.route('/api/set_all', methods=['POST'])
def api_set_all():
    """Set all servos simultaneously with smooth movement"""
    global current_angles
    
    if not is_connected:
        return jsonify({'success': False, 'message': 'Arduino not connected'})
    
    data = request.json
    angles = data.get('angles')
    
    if angles and len(angles) == 7:
        # Verify all angles are valid
        # Validation: servo 0-5 have range 0-180, gripper (servo 6) has range 0-70
        angles_validated = []
        for i, a in enumerate(angles):
            if i == 6:  # Gripper
                angles_validated.append(max(0, min(70, int(round(float(a))))))
            else:  # Other servos
                angles_validated.append(max(0, min(180, int(round(float(a))))))
        
        # Ensure servo 1 and servo 2 are coupled (opposite)
        angles_validated[2] = 180 - angles_validated[1]
        
        if all(0 <= a <= 180 for a in angles_validated[:6]) and 0 <= angles_validated[6] <= 70:
            # Start smooth movement in separate thread
            def move_thread():
                move_servo_smooth(angles_validated)
            
            movement_thread = threading.Thread(target=move_thread, daemon=True)
            movement_thread.start()
            
            return jsonify({
                'success': True,
                'angles': angles_validated,
                'message': 'Smooth movement started'
            })
    
    return jsonify({'success': False, 'message': 'Invalid angles'})

@app.route('/api/positions', methods=['GET'])
def api_get_positions():
    """Get all saved positions"""
    positions = load_saved_positions()
    return jsonify({'success': True, 'positions': positions})

@app.route('/api/positions', methods=['POST'])
def api_save_position():
    """Save a new position based on current slider values"""
    global current_angles
    
    if not is_connected:
        return jsonify({'success': False, 'message': 'Arduino not connected'})
    
    data = request.json
    position_name = data.get('name', '').strip()
    angles = data.get('angles')
    
    if not position_name:
        return jsonify({'success': False, 'message': 'Nome posizione richiesto'})
    
    if angles and len(angles) == 7:
        # Validate angles
        angles_validated = []
        for i, a in enumerate(angles):
            if i == 6:  # Gripper
                angles_validated.append(max(0, min(70, int(round(float(a))))))
            else:  # Other servos
                angles_validated.append(max(0, min(180, int(round(float(a))))))
        
        # Ensure servo 1 and servo 2 are coupled
        angles_validated[2] = 180 - angles_validated[1]
        
        # Load existing positions
        positions = load_saved_positions()
        
        # Save new position
        positions[position_name] = {
            'angles': angles_validated,
            'created': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if save_positions(positions):
            return jsonify({
                'success': True,
                'message': f'Posizione "{position_name}" salvata!',
                'positions': positions
            })
        else:
            return jsonify({'success': False, 'message': 'Errore nel salvataggio'})
    
    return jsonify({'success': False, 'message': 'Angoli non validi'})

@app.route('/api/positions/<position_name>', methods=['POST'])
def api_load_position(position_name):
    """Load a saved position"""
    global current_angles
    
    if not is_connected:
        return jsonify({'success': False, 'message': 'Arduino not connected'})
    
    positions = load_saved_positions()
    
    if position_name not in positions:
        return jsonify({'success': False, 'message': 'Posizione non trovata'})
    
    preset_angles = positions[position_name]['angles'].copy()
    
    # Start smooth movement in separate thread
    def move_thread():
        move_servo_smooth(preset_angles)
    
    movement_thread = threading.Thread(target=move_thread, daemon=True)
    movement_thread.start()
    
    return jsonify({
        'success': True,
        'angles': preset_angles,
        'position': position_name,
        'message': 'Movimento avviato'
    })

@app.route('/api/positions/<position_name>', methods=['DELETE'])
def api_delete_position(position_name):
    """Delete a saved position"""
    positions = load_saved_positions()
    
    if position_name not in positions:
        return jsonify({'success': False, 'message': 'Posizione non trovata'})
    
    del positions[position_name]
    
    if save_positions(positions):
        return jsonify({
            'success': True,
            'message': f'Posizione "{position_name}" eliminata',
            'positions': positions
        })
    else:
        return jsonify({'success': False, 'message': 'Errore nell\'eliminazione'})

@app.route('/api/set_current', methods=['POST'])
def api_set_current():
    """Set current position based on slider values (useful when manually aligning)"""
    global current_angles
    
    if not is_connected:
        return jsonify({'success': False, 'message': 'Arduino not connected'})
    
    data = request.json
    angles = data.get('angles')
    
    if angles and len(angles) == 7:
        # Validate angles
        angles_validated = []
        for i, a in enumerate(angles):
            if i == 6:  # Gripper
                angles_validated.append(max(0, min(70, int(round(float(a))))))
            else:  # Other servos
                angles_validated.append(max(0, min(180, int(round(float(a))))))
        
        # Update current position (without moving the arm)
        with arduino_lock:
            current_angles = angles_validated.copy()
            # Ensure servo 1 and 2 are coupled
            if len(current_angles) >= 3:
                current_angles[2] = 180 - current_angles[1]
        
        return jsonify({
            'success': True,
            'angles': current_angles,
            'message': 'Posizione corrente aggiornata'
        })
    
    return jsonify({'success': False, 'message': 'Angoli non validi'})

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 RoboArm Studio - Web Control Server")
    print("=" * 50)
    print("\nTo use:")
    print("1. Connect Arduino via USB")
    print("2. Open browser at: http://localhost:{}".format(FLASK_PORT))
    print("3. Click 'Connect' to automatically find Arduino")
    print("\nDebug mode: {}".format("ON" if DEBUG_MODE else "OFF"))
    print("(Set FLASK_DEBUG=true environment variable to enable)")
    print("\n" + "=" * 50 + "\n")
    
    # Start Flask server (port 5001 to avoid conflict with AirPlay)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG_MODE)
