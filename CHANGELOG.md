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

## [1.1.0] - 2025-11-28

### Added
- **Hardware Interpolation System**: Smooth movement interpolation implemented directly on Arduino
  - Configurable step size (INTERPOLATION_STEP parameter)
  - Configurable delay between steps (STEP_DELAY parameter)
  - Non-blocking implementation for responsive control
- **Position Management System**: Save, load, and delete custom arm positions
  - Persistent storage in JSON format
  - Web interface for position management
  - Position metadata with timestamps
- **Enhanced Servo Control**: Improved 7-servo support
  - Updated from 6 to 7 servos in all APIs
  - Better coupled servo handling (Arm A1/A2)
  - Improved debug logging with pin mapping
- **Documentation**: Comprehensive interpolation guide (INTERPOLATION_GUIDE.md)
  - Parameter tuning recommendations
  - Movement time calculations
  - Troubleshooting tips

### Changed
- **Movement System**: Replaced server-side interpolation with hardware interpolation
  - Smoother movements with reduced vibrations
  - Better precision and mechanical stability
  - Configurable speed vs smoothness trade-off
- **API Updates**: Updated all endpoints to support 7 servos
  - `/api/move` now handles servo 0-6
  - `/api/set_all` expects 7 angles
  - Improved validation and error messages
- **Preset Positions**: Updated all presets for 7-servo configuration
  - Home: [90, 90, 90, 90, 90, 90, 35]
  - Rest: [90, 30, 150, 90, 90, 90, 0]
  - Reach: [90, 120, 60, 60, 90, 90, 35]
  - Grab: [90, 90, 90, 90, 90, 90, 70]

### Fixed
- Servo count mismatch between Arduino (7) and Python (6)
- Coupled servo synchronization for Arm A1/A2
- Range validation for all servos including gripper

### Technical Details
- Default interpolation: 1° steps with 15ms delay
- Recommended range: 1-3° steps, 10-30ms delay
- Movement calculation: Time = (Angle_Diff / Step) × Delay
- Example: 90° movement = (90/1) × 15ms = 1.35 seconds

## [1.1.1] - 2025-11-28

### Fixed
- **Critical Interpolation Fix**: Resolved issue where servos remained mostly stationary
  - Changed servo write logic to only update during movement (prevents jitter)
  - Added delay when idle to prevent loop from running too fast
  - Improved stability and responsiveness of servo movements
- **Serial Debug**: Added debug output to monitor received values
  - Arduino now prints `RX: angle1,angle2,...` for troubleshooting
  - Helps identify communication issues between Python and Arduino

### Changed
- Optimized Arduino loop() to reduce unnecessary servo updates
- Improved servo stability by writing only when position changes

### Technical Details
- Servo write operations now conditional on `isMoving` flag
- Added 1ms delay when idle to prevent CPU overload
- Serial debug output format: `RX: 90,90,90,90,90,90,35`

## [Unreleased]

### Planned
- Configuration file for customizable settings
- Movement recording and playback
- Enhanced error recovery
- Unit tests
- Docker support
- WebSocket for real-time updates
- Trajectory planning with acceleration curves

