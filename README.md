A multiplayer laser tag system using Raspberry Pi Pico W microcontrollers with WiFi-based hit detection and tracking.

## Overview

This system implements a client-server architecture where laser guns act as WiFi-enabled clients that communicate with a central server to track shots and hits in real-time. The server uses timestamp matching to determine successful hits between players.

![Circuit Diagram](images/circuit_diagram.png)
*System circuit diagram*

![Laser Tag System](images/laser_gun_system.png)
*Assembled laser gun system*

### Communication Protocol

**Client → Server Messages:**
- `Shot [player_id] [HH:MM:SS]` - When trigger is pressed
- `Got [player_id] [HH:MM:SS]` - When light sensor detects hit

**Hit Detection Algorithm:**
1. Server maintains two queues: `fires[]` and `takes[]`
2. On receiving a "Shot" message, server searches for matching timestamp in `takes[]`
3. If match found: registers hit, otherwise adds to `fires[]` queue
4. Reverse process for "Got" messages
5. Matched pairs indicate successful hits: Player A → Player B

## Setup Instructions

### Hardware Setup (Pin Configuration)

| Component | Pin | Type |
|-----------|-----|------|
| Laser Diode | GPIO 5 | Digital Out (HIGH_POWER) |
| Light Sensor | GPIO 26 (ADC0) | Analog In |
| Trigger Button | GPIO 2 | Digital In (PULL_UP) |

### Software Setup

**1. Install MicroPython on Pico W**
```bash
# Download firmware from https://micropython.org/download/rp2-pico-w/
# Flash to Pico W using Thonny
```

**2. Configure Pico W (main.py)**
```python
# Update WiFi credentials (line 11)
wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')

# Update server IP (line 21)
clientSocket.connect(('YOUR_PC_IP', 1000))
```

**3. Run Server**
```bash
python server.py
```

**4. Deploy to Pico W**
- Upload `main.py` to each Pico W
- Each device will auto-connect and start operating

## Features

- **Real-time Hit Detection** - Timestamp-based matching algorithm
- **Multi-threaded Server** - Supports multiple concurrent players
- **Unique Player IDs** - Automatic ID assignment via `machine.unique_id()`
- **Light-based Communication** - Uses laser beam itself as identifier (novel approach)

## Network Configuration

- **Protocol:** TCP sockets
- **Port:** 1000
- **Server:** Localhost (127.0.0.1) - change to LAN IP for network play
- **Connection:** Each Pico W maintains persistent connection to server

## Calibration

Adjust light sensor threshold in `main.py` line 40:
```python
if l > 0.8:  # Increase/decrease based on ambient light
```

## Limitations

- Requires game master to monitor server output
- No feedback sent to clients (display-less operation)
- Vest sensors wired to gun unit (not wireless)

## Future Enhancements

- MPU-6050 integration for holstering detection (Western showdown mode)
- Client feedback LEDs/displays
- Wireless vest sensors
- Mobile app for game monitoring

## Technologies Used

- **MicroPython** - Embedded Python for Pico W
- **Python 3** - Server implementation
- **TCP/IP Sockets** - Network communication
- **Multi-threading** - Concurrent client handling