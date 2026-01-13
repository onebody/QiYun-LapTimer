# QiYun LapTimer

This project is split into two parts:

*   **[lpt_node/](./lpt_node/)**: ESP32 firmware code (PlatformIO project). Handles RSSI reading, RX5808 control, and data streaming.
*   **[lpt_web/](./lpt_web/)**: Host application web interface. Connects to the firmware via WebSocket/HTTP API.

## Getting Started

### Firmware (lpt_node)
1. Go to `lpt_node/` directory.
2. Open with PlatformIO.
3. Build and flash to your ESP32.
4. Upload filesystem (contains minimal management UI).

### Web App (lpt_web)
1. Go to `lpt_web/` directory.
2. Serve the static files (e.g., using `python3 -m http.server`).
3. Open in browser.
