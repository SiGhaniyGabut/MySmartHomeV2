# My SmartHome Project (V2)

This project is improvement of previous SmartHome project that uses PlatformIO with C++ language. On previous project, device controlled by Telegram Bot.

This project uses Micropython. Device controlled via WebSocket on dedicated server. Several improvements are made on this project, such as:
- Device controlled via WebSocket
- One Device One API Key. Device authenticated via API Key on Device Registration.
- Request-Response overhead reduced.
- Auto Reconnect on WebSocket connection lost.
- OTA auto update on next reboot.
- Connect and Go. Device will automatically configured based on configuration from Web UI.

## Devices
- ESP8266

## Configuration
- Rename `config.example.json` to `config.json`
- Fill `config.json` with your configuration
- Flash your device with firmware on `flash` folder
- Install PyMakr on your VSCode
- Connect, and upload this project to your device

## Depedencies
This project uses (fill later) project as backend. You can find it on (fill later). Install it on your server, or use paid service on (fill later).

## Development
This project use micropython ports to build custom firmware. Just follow instruction on micropython documentation to build custom firmware for your device.

## Contribution
Feel free to contribute on this project. Just fork this project, and create pull request. You can also create issue if you found any bug or have any idea to improve this project.
