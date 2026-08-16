# Changelog


## [2.39.6.1] - 2026-08-12

### Docker Hub

- Docker Hub image: `docker.io/portainer/portainer-ce:2.39.6-alpine`
- Digest: `sha256:f35a74e590973d9c77fa2c4930c64c1a05626eedf64462b3d2eebef5a7c710e3`
- Aktualisiert auf Docker Hub: 2026-08-12

Weitere Informationen: https://docker.io/portainer/portainer-ce

---

## [2.39.5.1] - 2026-08-02

- Die benutzerbezogene Ingress-Anmeldung bleibt mit einem automatisch erzeugten Portainer Access Token auch nach App-Neustarts erhalten.
- Das Portainer-Passwort wird nicht gespeichert.
- Rebuilt the app family from the functional archived Portainer proxy design.
- Added CE/BE and LTS/STS selection, documented server options and optional environment variables.
- Added Ingress with optional per-Home-Assistant-user login retention.
- Added `/data`, `/config` and `/share` storage migration plus controlled import/export.
- Added direct HTTP/HTTPS/tunnel ports and a Watchdog health endpoint.

### Docker Hub

- Docker Hub image: `docker.io/portainer/portainer-ce:2.39.5-alpine`
- Digest: `sha256:d9771805f1757233d706b5995ec4418d5d4310299c383822ae3bdafb54e753df`
- Aktualisiert auf Docker Hub: 2026-07-13

Weitere Informationen: https://docker.io/portainer/portainer-ce
