# Changelog


## [1.9.1.1] - 2026-09-01

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/olm@sha256:298062dacd9e27dd0283925efb52566e5f07eb4967f3581460c463c0910bebcb`
- Docker Hub: `docker.io/fosrl/olm@sha256:298062dacd9e27dd0283925efb52566e5f07eb4967f3581460c463c0910bebcb`
**Tag:** `1.9.1`


## What's Changed
* Fix normalize bare server IP before route setup by @totalolage in https://github.com/fosrl/olm/pull/140
* Fix separate out the dns handler so Swift does not double override
* Add immediate ping methods for websocket connection liveness checks
* Add connection management methods and tests for websocket client 

## New Contributors
* @totalolage made their first contribution in https://github.com/fosrl/olm/pull/140

**Full Changelog**: https://github.com/fosrl/olm/compare/1.9.0...1.9.1

Weitere Informationen: https://github.com/fosrl/olm/releases/latest

---

## [1.9.0.4] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/olm

---

## [1.9.0.3] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/olm

---

## [1.9.0.2] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/olm

---

## [1.9.0.1] - 2026-08-19

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/olm@sha256:9082c9cfccae6f977332ef996004e1b0f214de66292345e81fbf9d71f357427d`
- Docker Hub: `docker.io/fosrl/olm@sha256:9082c9cfccae6f977332ef996004e1b0f214de66292345e81fbf9d71f357427d`
**Tag:** `1.9.0`


## What's Changed
* Add exit node connections as a peer
* Add aliases pointing to exit node
* Fix attempt to reduce crashing on all platforms
* Fix create nm conf directory if missing by @Gurkinator1 in https://github.com/fosrl/olm/pull/137

## New Contributors
* @Gurkinator1 made their first contribution in https://github.com/fosrl/olm/pull/137

**Full Changelog**: https://github.com/fosrl/olm/compare/1.8.2...1.9.0

Weitere Informationen: https://github.com/fosrl/olm/releases/latest

---

## [1.8.2.2] - 2026-08-27

- Healthcheck ohne TCP-Port; entfernt den HTTP-Healthserver und die socat-Abhängigkeit.
- Verhindert Health-Port-Konflikte im Host-Netzwerk, auch bei parallelen App-Instanzen.
- Der Docker-Healthcheck prüft den App-Prozess direkt.


## [1.8.2.1] - 2026-08-03

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/olm@sha256:9a8486519830768cc365451cf2bf07d4717f9d9c85fd830f7a800d1f6ba417ef`
- Docker Hub: `docker.io/fosrl/olm@sha256:9a8486519830768cc365451cf2bf07d4717f9d9c85fd830f7a800d1f6ba417ef`
**Tag:** `1.8.2`


## What's Changed
* Fix some websocket disconnections by adding deadlines to websocket
* Fix local to relay flapping if there is an overlapping CIDR route with a site local address


**Full Changelog**: https://github.com/fosrl/olm/compare/1.8.1...1.8.2

Weitere Informationen: https://github.com/fosrl/olm/releases/latest

---

## [1.8.1.1] - 2026-07-31

- `BUILD_FROM` wird zentral und architekturspezifisch aus `build.json` übernommen.
- Doppelpflege des Basisimages im Dockerfile entfernt.
- Erste Home-Assistant-App auf Basis von Olm 1.8.1.
- Konfiguration für Pangolin-Zugang, WireGuard, DNS und Verbindungsoptionen ergänzt.
