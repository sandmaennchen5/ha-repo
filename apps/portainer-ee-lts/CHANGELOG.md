# Changelog

## [2.39.5.1] - 2026-08-02

- Die benutzerbezogene Ingress-Anmeldung bleibt mit einem automatisch erzeugten Portainer Access Token auch nach App-Neustarts erhalten.
- Das Portainer-Passwort wird nicht gespeichert.
- Rebuilt the app family from the functional archived Portainer proxy design.
- Added CE/BE and LTS/STS selection, documented server options and optional environment variables.
- Added Ingress with optional per-Home-Assistant-user login retention.
- Added `/data`, `/config` and `/share` storage migration plus controlled import/export.
- Added direct HTTP/HTTPS/tunnel ports and a Watchdog health endpoint.

### Docker Hub

- Docker Hub image: `docker.io/portainer/portainer-ee:2.39.5-alpine`
- Digest: `sha256:7f7408b8336701055b87446e87978f26d5ead271de64ffad07b2173acf3165d8`
- Aktualisiert auf Docker Hub: 2026-07-13

Weitere Informationen: https://docker.io/portainer/portainer-ee
