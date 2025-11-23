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

## Presets

- **Home**: Initial position (servo 0-5 at 90°, gripper at 35°)
- **Rest**: Rest position
- **Reach**: Arm extended forward
- **Grab**: Position to grab objects

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
