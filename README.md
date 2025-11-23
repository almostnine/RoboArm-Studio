# 🤖 RoboArm Studio

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?logo=flask&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Mac%20%7C%20Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Arduino](https://img.shields.io/badge/Arduino-Compatible-orange?logo=arduino&logoColor=white)

**The ultimate web-based control studio for your Arduino robotic arm.** Modern, intuitive, and powerful - control your robotic arm from any device, anywhere.

Perfect for students, makers, and robotics enthusiasts who want professional-grade control with a beautiful interface.

## 🎯 Hardware Base

**This software project is based on the hardware design of the robotic arm by [Emre Kalem](https://makerworld.com/en/models/1134).**

The original hardware design has been modified for this project:
- **Removed**: Breadboard
- **Added**: Sensor Shield mounted directly on top of Arduino Uno R4

This project uses **Arduino Uno R4 with Sensor Shield** as the hardware platform, providing a cleaner and more integrated setup compared to the original breadboard-based design.

## 📋 Features

✅ **Cross-platform**: Works on Mac, Windows and Linux  
✅ **Modern web interface**: Dark and professional design  
✅ **Real-time control**: 7 controllable servos with sliders  
✅ **Predefined positions**: Home, Rest, Reach, Grab  
✅ **Auto-detect Arduino**: Automatically finds USB port  
✅ **Gripper control**: Quick actions to open/close  

## 🔧 Installation

### Prerequisites

1. **Python 3.7 or higher**
   - Mac: `python3 --version`
   - Should already be installed on macOS

2. **Arduino Uno R4 with Sensor Shield**
   - **Hardware**: Arduino Uno R4 with Sensor Shield attached on top
   - Upload the code `RoboArm_Studio.ino` to Arduino before starting
   - Connect Arduino via USB to your computer

### Installation on Mac

1. **Open Terminal** (Cmd + Space, type "Terminal")

2. **Navigate to project folder**:
   ```bash
   cd ~/Desktop/robot_arm_control
   ```

3. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

   If you have problems, use:
   ```bash
   python3 -m pip install Flask pyserial
   ```

4. **Give execution permissions**:
   ```bash
   chmod +x robot_arm_server.py
   ```

## 🚀 Starting

### Method 1: From Terminal

```bash
python3 robot_arm_server.py
```

### Method 2: Quick start script

Create a `start.command` file with this content:

```bash
#!/bin/bash
cd "$(dirname "$0")"
python3 robot_arm_server.py
```

Then:
```bash
chmod +x start.command
```

Now you can double-click `start.command` to start the server!

## 📱 Usage

1. **Start the server** (see above)

2. **Open browser** and go to:
   ```
   http://localhost:5001
   ```

3. **Connect Arduino**:
   - Click "Connect Arduino"
   - The system will automatically find the Arduino
   - If it doesn't work, manually select the port from the dropdown menu

4. **Control the arm**:
   - Use sliders to move servos
   - Use presets for predefined positions
   - Use quick actions for gripper

## 🎮 Servo Mapping

**Hardware**: Arduino Uno R4 with Sensor Shield

| Servo | Function | Arduino Pin |
|-------|----------|-------------|
| Servo 0 | Root (Rotating base) | Pin 2 |
| Servo 1 | Arm A1 (Main arm) | Pin 3 |
| Servo 2 | Arm A2 (Coupled arm) | Pin 4 |
| Servo 3 | Arm B (Forearm) | Pin 5 |
| Servo 4 | Wrist A (Wrist A) | Pin 6 |
| Servo 5 | Wrist B (Wrist B) | Pin 7 |
| Servo 6 | Gripper (Claw) | Pin 8 |

**Note**: Arm A1 (Pin 3) and Arm A2 (Pin 4) are coupled and rotate in opposite directions. When Arm A1 moves to X°, Arm A2 automatically moves to (180-X)°.

## 📍 Predefined Positions

- **🏠 Home**: Initial position (servo 0-5 at 90°, gripper at 35°)
- **😴 Rest**: Rest position (base and closed gripper)
- **🎯 Reach**: Arm extended forward
- **✊ Grab**: Position to grab objects

## 🔍 Troubleshooting

### Arduino not found

1. Verify Arduino is connected via USB
2. Check that driver is installed:
   ```bash
   ls /dev/cu.*
   ```
   You should see something like `/dev/cu.usbmodem...`

3. If necessary, install CH340/CP2102 drivers for your Arduino clone

### Port already in use

Make sure Arduino IDE is closed and serial monitor is not active.

### Permission denied

On Mac, you might need to give permissions:
```bash
sudo chmod 666 /dev/cu.usbmodem*
```

### Server won't start

Verify dependencies are installed:
```bash
pip3 list | grep -E "Flask|pyserial"
```

## 🌐 Access from Other Devices

To control the arm from another computer/tablet on the same network:

1. Find your IP address:
   ```bash
   ifconfig | grep "inet "
   ```

2. On remote device, go to:
   ```
   http://YOUR_IP:5001
   ```
   For example: `http://192.168.1.100:5001`

## 🛠️ Customization

### Change server port

In `robot_arm_server.py`, at the end:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```
Change `5001` to desired port.

### Enable debug mode

Set environment variable:
```bash
export FLASK_DEBUG=true
python3 robot_arm_server.py
```

Or on Windows:
```cmd
set FLASK_DEBUG=true
python robot_arm_server.py
```

### Add new presets

In `robot_arm_server.py`, in the `api_preset` function:
```python
presets = {
    'home': [90, 90, 90, 90, 90, 90, 35],
    'your_preset': [45, 120, 60, 90, 45, 180, 50],  # Add here
}
```

Then add the button in `templates/index.html`.

## 📦 Project Structure

```
robot_arm_control/
├── robot_arm_server.py       # Flask server
├── requirements.txt           # Python dependencies
├── LICENSE                    # License file
├── CHANGELOG.md              # Version history
├── .gitignore                # Git ignore file
├── templates/
│   └── index.html            # Web interface
├── static/
│   ├── css/
│   │   └── style.css         # Styles
│   └── js/
│       └── app.js            # Frontend logic
└── README.md                 # This file
```

## 🤝 Credits

### Hardware Design Base
- **Original Robotic Arm Design**: [Emre Kalem](https://makerworld.com/en/models/1134) (Eskisehir, Turkiye, 2025)
  - Original 3D printable robotic arm design
  - STL files and assembly instructions available on [MakerWorld](https://makerworld.com/en/models/1134)
  - **Hardware Modification**: This project uses a modified version of the hardware design:
    - Removed breadboard
    - Added Sensor Shield mounted on top of Arduino Uno R4
    - This provides a cleaner, more integrated setup

### Software & Web Interface
- **Code & Web Interface**: Developed for cross-platform compatibility
- This software provides a modern web-based control system for the robotic arm
- All code in this repository was written to interface with the modified hardware setup based on Emre Kalem's robotic arm design

## 📝 License

This project is provided "as is" for educational and learning purposes.

See [LICENSE](LICENSE) file for details.

## 🆘 Support

For problems or questions:
1. Check the "Troubleshooting" section
2. Verify Arduino is programmed correctly
3. Check server logs in terminal

---

**Start building amazing things with RoboArm Studio! 🦾✨**
