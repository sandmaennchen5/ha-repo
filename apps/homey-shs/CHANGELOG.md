# Changelog


## [13.4.0] - 2026-07-28

### GitHub Container Registry

Core
- Improves stability and performance of fetching system info.
- Updates translations.
Energy
- Fixes the dynamic-price "cheapest/expensive hours" Flow condition so it evaluates correctly when the time window crosses midnight.
Matter
- Increases the maximum subscription intervals for more stable device reporting.
- Adds the ability to override the default subscription intervals for a Matter device in its device settings, for finer control over how often it reports.
- Fixes the robot vacuum "mapping" mode and related issues.
BLE
- Adds support for subscribing to BLE advertisements for sensors without a constant - connection, improving battery life and reliability.
- Fixes an issue with ‘le-connection-abort-by-local’ error.
- Fixes an issue where BLE sensors would stop updating.
- Fixes an issue where BLE advertisements stopped coming.
- Fixes an issue with ‘No peripheral found’ error.
- Fixes a race condition that could cause a "device unavailable" error.
- Fixes an issue that could cause BLE discovery and connection to fail.
Z-Wave
- Fixes an issue that causes devices to get the wrong device class after pairing.
Apps
- Fixes an issue that could cause a Python app to crash when changing app settings.

Release Notes: https://homey.app/en-us/wiki/homey-shs-changelog/

Weitere Informationen: https://ghcr.io/athombv/homey-shs

---

## [13.3.1] - 2026-07-24

### GitHub Container Registry

- Fixed an issue where reboot would not work.

Release Notes: https://homey.app/en-us/wiki/homey-shs-changelog/

Weitere Informationen: https://ghcr.io/athombv/homey-shs

---

## 13.2.1

- Offizielles Homey-SHS-Image auf Version 13.2.1 aktualisiert
- Fehlerhafte mehrstufige `BUILD_FROM`-Konstruktion entfernt
- Laufzeit-Entrypoint für persistente Daten unter `/data` hinzugefügt
- `rrdcached`-Basispfad auf das persistente Datenverzeichnis umgeleitet

