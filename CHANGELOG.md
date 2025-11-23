# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added
- Initial release of Robot Arm Web Control Panel
- Web interface for controlling 7-servo robotic arm via Arduino
- Cross-platform support (Mac, Windows, Linux)
- Auto-detect Arduino port functionality
- Smooth servo movement with interpolation
- Predefined positions (Home, Rest, Reach, Grab)
- Real-time angle display and servo control sliders
- Coupled servo control for Arm A1/A2 (opposite rotation)
- Gripper control with limited range (0-70°)
- Quick actions for gripper (open, close, reset)
- Modern dark theme UI with responsive design
- Connection status indicator
- Port selection dropdown with refresh
- Error handling and user notifications

### Technical Details
- Flask 3.0.0 web server
- pyserial 3.5 for Arduino communication
- Thread-safe servo movement control
- Gradual movement interpolation (1° steps, 20ms delay)
- Range validation for all servos (0-180° standard, 0-70° gripper)

### Hardware
- Compatible with Arduino-based robotic arms
- Supports 7 servos (6 standard + 1 gripper)
- Serial communication at 9600 baud

---

## [Unreleased]

### Planned
- Configuration file for customizable settings
- Save/load custom preset positions
- Movement recording and playback
- Enhanced error recovery
- Unit tests
- Docker support
- WebSocket for real-time updates

