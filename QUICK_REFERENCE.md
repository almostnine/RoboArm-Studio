# Quick Reference - RoboArm Studio Interpolation

## 🚀 Quick Start

### 1. Upload Firmware
```bash
# Open Arduino IDE → Load RoboArm_Studio.ino → Upload
```

### 2. Start Server
```bash
python3 robot_arm_server.py
# Open http://localhost:5001
```

### 3. Test
```bash
python3 test_interpolation.py
```

## ⚙️ Configuration Presets

Copy-paste into `RoboArm_Studio.ino` (lines 22-23):

### 🎬 Video/Demo (Ultra Smooth)
```cpp
const int INTERPOLATION_STEP = 1;
const int STEP_DELAY = 25;
```
**Time for 90°:** 2.25s | **Best for:** Recording, presentations

### 🎯 Default (Balanced)
```cpp
const int INTERPOLATION_STEP = 1;
const int STEP_DELAY = 15;
```
**Time for 90°:** 1.35s | **Best for:** General use

### ⚡ Fast
```cpp
const int INTERPOLATION_STEP = 2;
const int STEP_DELAY = 10;
```
**Time for 90°:** 0.45s | **Best for:** Quick operations

### 🏋️ Heavy Load
```cpp
const int INTERPOLATION_STEP = 1;
const int STEP_DELAY = 30;
```
**Time for 90°:** 2.70s | **Best for:** Carrying heavy objects

### 🔧 Pick-and-Place
```cpp
const int INTERPOLATION_STEP = 2;
const int STEP_DELAY = 12;
```
**Time for 90°:** 0.54s | **Best for:** Repetitive cycles

## 📊 Parameter Effects

### INTERPOLATION_STEP (degrees per step)
```
1° → Smoothest, slowest
2° → Balanced
3° → Faster, less smooth
```

### STEP_DELAY (milliseconds between steps)
```
10ms → Fastest
15ms → Balanced
20ms → Smooth
30ms → Slowest, most stable
```

## 🎛️ Tuning Guide

### Too Slow?
```cpp
// Increase step OR decrease delay
const int INTERPOLATION_STEP = 2;  // was 1
const int STEP_DELAY = 10;         // was 15
```

### Too Jerky?
```cpp
// Decrease step OR increase delay
const int INTERPOLATION_STEP = 1;  // was 2
const int STEP_DELAY = 20;         // was 15
```

### Vibrations?
```cpp
// Increase delay
const int STEP_DELAY = 25;         // was 15
```

## 📐 Time Calculator

```
Time (seconds) = (Angle Difference ÷ STEP) × DELAY ÷ 1000

Examples with STEP=1, DELAY=15:
45° → (45 ÷ 1) × 15 ÷ 1000 = 0.68s
90° → (90 ÷ 1) × 15 ÷ 1000 = 1.35s
180° → (180 ÷ 1) × 15 ÷ 1000 = 2.70s
```

## 🔌 API Endpoints

### Basic Control
```bash
# Move single servo
POST /api/move
{"servo": 0, "angle": 90}

# Move all servos
POST /api/set_all
{"angles": [90, 90, 90, 90, 90, 90, 35]}

# Load preset
POST /api/preset/home
```

### Position Management
```bash
# Get saved positions
GET /api/positions

# Save position
POST /api/positions
{"name": "my_position", "angles": [90, 90, 90, 90, 90, 90, 35]}

# Load position
POST /api/positions/my_position

# Delete position
DELETE /api/positions/my_position
```

## 🎯 Servo Mapping

| Servo | Pin | Function | Range |
|-------|-----|----------|-------|
| 0 | 2 | Root | 0-180° |
| 1 | 3 | Arm A1 | 0-180° |
| 2 | 4 | Arm A2 (coupled) | 0-180° |
| 3 | 5 | Arm B | 0-180° |
| 4 | 6 | Wrist A | 0-180° |
| 5 | 7 | Wrist B | 0-180° |
| 6 | 8 | Gripper | 0-70° |

**Note:** Servos 1 & 2 are coupled (opposite rotation)

## 🎨 Built-in Presets

```python
home  = [90, 90, 90, 90, 90, 90, 35]  # Initial position
rest  = [90, 30, 150, 90, 90, 90, 0]  # Rest position
reach = [90, 120, 60, 60, 90, 90, 35] # Extended forward
grab  = [90, 90, 90, 90, 90, 90, 70]  # Grab position
```

## 🐛 Troubleshooting

### Arduino Not Found
```bash
# Mac
ls /dev/cu.*

# Linux
ls /dev/ttyUSB* /dev/ttyACM*

# Windows
# Check Device Manager → Ports (COM & LPT)
```

### Port Already in Use
```bash
# Close Arduino IDE Serial Monitor
# Kill process using port 5001:
lsof -ti:5001 | xargs kill -9
```

### Servo Not Moving
1. Check power supply (5V, adequate current)
2. Verify servo connections
3. Check serial monitor for errors
4. Test with default config first

### Movements Too Fast/Slow
See "Tuning Guide" section above

## 📚 Documentation

- 📖 **Full Guide:** [INTERPOLATION_GUIDE.md](INTERPOLATION_GUIDE.md)
- 🔧 **Advanced:** [ADVANCED_CONFIG.md](ADVANCED_CONFIG.md)
- 📝 **General:** [README.md](README.md)
- 📋 **Changes:** [CHANGELOG.md](CHANGELOG.md)
- 📊 **Summary:** [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)

## 💡 Tips

1. ✅ Always start with default config
2. ✅ Test after each change
3. ✅ Save working configs
4. ✅ Monitor servo temperature
5. ✅ Use stable power supply

## 🆘 Quick Help

```bash
# Test interpolation
python3 test_interpolation.py

# Check server status
curl http://localhost:5001/api/status

# View logs
# Server logs appear in terminal where you ran robot_arm_server.py
```

## 📞 Support

- 🐛 Report issues on GitHub
- 📖 Read full documentation
- 💬 Check discussions

---

**Print this page for quick reference! 📄**


