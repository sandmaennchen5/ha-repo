# Changelog


## [0.16.0.2] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/cli

---

## [0.16.0.1] - 2026-08-21

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/cli@sha256:a25a6d81b1f6c20f9f4c47fda4c82e61ec5a7cf72f6465174db552b0fe616434`
- Docker Hub: `docker.io/fosrl/pangolin-cli@sha256:a25a6d81b1f6c20f9f4c47fda4c82e61ec5a7cf72f6465174db552b0fe616434`
**Tag:** `0.16.0`


## What's Changed
* Add support for Pangolin (>= 1.22.0) AI Gateway private resources
* Add support for configuring common AI clients to connect to Pangolin AI Gateway resources

**Full Changelog**: https://github.com/fosrl/cli/compare/0.15.1...0.16.0

Weitere Informationen: https://github.com/fosrl/cli/releases/latest

---

## [0.15.1.2] - 2026-08-27

- Healthcheck ohne TCP-Port; entfernt den HTTP-Healthserver und die socat-Abhängigkeit.
- Verhindert Health-Port-Konflikte im Host-Netzwerk, auch bei parallelen App-Instanzen.
- Der Docker-Healthcheck prüft den App-Prozess direkt.


## [0.15.1.1] - 2026-08-03

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/cli@sha256:18575106ba5c2e705df293396d7edeca36fab39fa551fe4ccfb0977f644cc82a`
- Docker Hub: `docker.io/fosrl/pangolin-cli@sha256:18575106ba5c2e705df293396d7edeca36fab39fa551fe4ccfb0977f644cc82a`
**Tag:** `0.15.1`


## What's Changed
* Fix some websocket disconnections by adding deadlines to websocket
* Fix local to relay flapping if there is an overlapping CIDR route with a site local address
* Support -i in the native Pangolin ssh command


**Full Changelog**: https://github.com/fosrl/cli/compare/0.15.0...0.15.1

Weitere Informationen: https://github.com/fosrl/cli/releases/latest

---

## [0.15.0.1] - 2026-07-31

- `BUILD_FROM` wird zentral und architekturspezifisch aus `build.json` übernommen.
- Doppelpflege des Basisimages im Dockerfile entfernt.
- Erste Home-Assistant-App auf Basis der Pangolin CLI 0.15.0.
- Dauerhafter Machine-Client-Modus mit Pangolin-Endpunkt und Zugangsdaten.
