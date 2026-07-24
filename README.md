# RoboArm Studio

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?logo=flask&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Mac%20%7C%20Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Arduino](https://img.shields.io/badge/Arduino-Compatible-orange?logo=arduino&logoColor=white)

Web interface to control an Arduino robotic arm via Flask. 7 servomotors controllable in real-time.

## Hardware

Based on [Emre Kalem](https://makerworld.com/en/models/1134)'s design, modified:
- Removed breadboard
- Added Sensor Shield on Arduino Uno R4

**Setup**: Arduino Uno R4 with Sensor Shield

## Setup

```bash
pip3 install -r requirements.txt
python3 robot_arm_server.py
```

Then open `http://localhost:5001` and connect the Arduino.

**Important**: Upload `RoboArm_Studio.ino` to Arduino before starting the server.

## Servo Mapping

| Servo | Function | Arduino Pin |
|-------|----------|-------------|
| 0 | Root (rotating base) | Pin 2 |
| 1 | Arm A1 (main arm) | Pin 3 |
| 2 | Arm A2 (coupled arm) | Pin 4 |
| 3 | Arm B (forearm) | Pin 5 |
| 4 | Wrist A | Pin 6 |
| 5 | Wrist B | Pin 7 |
| 6 | Gripper | Pin 8 |

**Note**: Arm A1 (Pin 3) and Arm A2 (Pin 4) are coupled and rotate in opposite directions. When A1 moves to X°, A2 automatically moves to (180-X)°.

## Movement Interpolation ✨

**NEW in v1.1.0**: Hardware interpolation for smooth, vibration-free movements!

```
Without Interpolation:     With Interpolation:
Position A → Position B    Position A → → → → → Position B
     ⚡ JUMP!                    🌊 SMOOTH FLOW
```

Instead of jumping directly to target positions, servos move gradually in small steps:

| Feature | Benefit |
|---------|---------|
| 🎯 **Reduced Vibrations** | Gradual movements reduce mechanical stress |
| 🌊 **Smooth Motion** | Natural, fluid transitions between positions |
| 📐 **Better Precision** | More controlled positioning |
| ⚙️ **Less Wear** | Extended servo and mechanical lifespan |
| 🎛️ **Configurable** | Adjust speed vs smoothness trade-off |

### Quick Start

1. **Upload the updated firmware** to Arduino
2. **Start the server**: `python3 robot_arm_server.py`
3. **Test interpolation**: `python3 test_interpolation.py`

### Configuration

Adjust interpolation in `RoboArm_Studio.ino`:

```cpp
const int INTERPOLATION_STEP = 1;  // Degrees per step (1-3 recommended)
const int STEP_DELAY = 15;         // Milliseconds between steps (10-30 recommended)
```

**Movement Time Calculation:**
```
Time (seconds) = (Angle Difference / INTERPOLATION_STEP) × STEP_DELAY / 1000

Example: 90° movement with default settings
Time = (90 / 1) × 15 / 1000 = 1.35 seconds
```

### Presets

| Preset | Speed | Smoothness | Use Case |
|--------|-------|------------|----------|
| **Ultra-Smooth** | STEP=1, DELAY=20 | ⭐⭐⭐⭐⭐ | Video recording, demos |
| **Balanced** (default) | STEP=1, DELAY=15 | ⭐⭐⭐⭐ | General use |
| **Fast** | STEP=2, DELAY=10 | ⭐⭐⭐ | Quick operations |
| **Heavy Load** | STEP=1, DELAY=25 | ⭐⭐⭐⭐⭐ | Carrying heavy objects |

📖 **See [INTERPOLATION_GUIDE.md](INTERPOLATION_GUIDE.md) for detailed configuration and tuning.**

## Positions Management 💾

### Built-in Presets

| Preset | Description | Angles |
|--------|-------------|--------|
| **Home** | Initial position | [90, 90, 90, 90, 90, 90, 35] |
| **Rest** | Rest position | [90, 30, 150, 90, 90, 90, 0] |
| **Reach** | Arm extended forward | [90, 120, 60, 60, 90, 90, 35] |
| **Grab** | Position to grab objects | [90, 90, 90, 90, 90, 90, 70] |

### Custom Positions

Save and load your own positions directly from the web interface:

1. **Position the arm** using sliders
2. **Click "Save Position"** and give it a name
3. **Load anytime** from the saved positions list
4. **Delete** positions you no longer need

Positions are automatically saved to `saved_positions.json` and persist between sessions.

## Network Access

To control from other devices on the same network:

```bash
ifconfig | grep "inet "
```

Then open `http://YOUR_IP:5001` from the remote device.

## Customization

### Change port

In `robot_arm_server.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Add preset

In `robot_arm_server.py`, `api_preset` function:
```python
presets = {
    'home': [90, 90, 90, 90, 90, 90, 35],
    'new_preset': [45, 120, 60, 90, 45, 180, 50],
}
```

Then add the button in `templates/index.html`.

## Troubleshooting

**Arduino not found**: Check it's connected and drivers are installed. On Mac: `ls /dev/cu.*`

**Port already in use**: Close Arduino IDE and serial monitor.

**Permission denied** (Mac):
```bash
sudo chmod 666 /dev/cu.usbmodem*
```

## Credits

- Original hardware design: [Emre Kalem](https://makerworld.com/en/models/1134)
- Hardware modifications: Breadboard removed, Sensor Shield added

## License

MIT - See [LICENSE](LICENSE) for details.
