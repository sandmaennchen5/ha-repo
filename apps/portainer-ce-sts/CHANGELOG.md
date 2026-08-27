# Changelog


## [2.45.0.1] - 2026-08-27

### Docker Hub

- Docker Hub image: `docker.io/portainer/portainer-ce:2.45.0-alpine`
- Digest: `sha256:e6b0225f4bbc989e398c85062f7426f8cf4b61f8aca6f40bf44789d1dada1949`
- Aktualisiert auf Docker Hub: 2026-08-27

Weitere Informationen: https://docker.io/portainer/portainer-ce

---

## [2.44.0.1] - 2026-08-02

- Die benutzerbezogene Ingress-Anmeldung bleibt mit einem automatisch erzeugten Portainer Access Token auch nach App-Neustarts erhalten.
- Das Portainer-Passwort wird nicht gespeichert.
- Rebuilt the app family from the functional archived Portainer proxy design.
- Added CE/BE and LTS/STS selection, documented server options and optional environment variables.
- Added Ingress with optional per-Home-Assistant-user login retention.
- Added `/data`, `/config` and `/share` storage migration plus controlled import/export.
- Added direct HTTP/HTTPS/tunnel ports and a Watchdog health endpoint.

### Docker Hub

- Docker Hub image: `docker.io/portainer/portainer-ce:2.44.0-alpine`
- Digest: `sha256:5376fd96f0bae14be7285ceb24c5cf9470dc23f19cdde74ff4c65d11cbe96eb2`
- Aktualisiert auf Docker Hub: 2026-07-30

Weitere Informationen: https://docker.io/portainer/portainer-ce

