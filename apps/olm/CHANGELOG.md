# Changelog


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
