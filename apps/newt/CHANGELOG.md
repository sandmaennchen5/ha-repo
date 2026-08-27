# Changelog


## [1.16.0.2] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/newt

---

## [1.16.0.1] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/newt

---

## [1.16.0] - 2026-08-19

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/newt@sha256:345fdeb369be6608d82c41d70637636c78b2c04a6112ff6ec20fc21c48afc899`
- Docker Hub: `docker.io/fosrl/newt@sha256:345fdeb369be6608d82c41d70637636c78b2c04a6112ff6ec20fc21c48afc899`
**Tag:** `1.16.0`


## What's Changed
* Add fallback self signed cert so not locked out of http resources
* fix: preserve the pending WireGuard registration chain by @Serph91P in https://github.com/fosrl/newt/pull/424
* fix: preserve pending registration chain
* Add support for exit node connections in Olm

## New Contributors
* @Serph91P made their first contribution in https://github.com/fosrl/newt/pull/424

**Full Changelog**: https://github.com/fosrl/newt/compare/1.15.0...1.16.0

Weitere Informationen: https://github.com/fosrl/newt/releases/latest

---

## [1.15.0.3] - 2026-08-27

- Healthcheck ohne TCP-Port; entfernt den HTTP-Healthserver und die socat-Abhängigkeit.
- Verhindert Health-Port-Konflikte im Host-Netzwerk, auch bei parallelen App-Instanzen.
- Bestehende Prozess-, Statusdatei- und Endpoint-Prüfungen bleiben erhalten.


## [1.15.0.2] - 2026-08-04

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/newt

---

## [1.15.0.1] - 2026-07-31

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/newt

---

## [1.15.0] - 2026-07-19

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/newt@sha256:d69d047c816ca7721eae90d5f3cd3be53b615b3d498678be21488d666538ee5c`
- Docker Hub: `docker.io/fosrl/newt@sha256:d69d047c816ca7721eae90d5f3cd3be53b615b3d498678be21488d666538ee5c`
**Tag:** `1.15.0`


## What's Changed
- Add PKGBUILD
- Scrape and send local endpoints to accept local network connections from clients
- Add option to add metric to routes to make local routes the default


**Full Changelog**: https://github.com/fosrl/newt/compare/1.14.0...1.15.0

Weitere Informationen: https://github.com/fosrl/newt/releases/latest

---

