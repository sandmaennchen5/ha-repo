# Changelog


## [2.45.0.1] - 2026-08-27

### Docker Hub

- Docker Hub image: `docker.io/portainer/portainer-ee:2.45.0-alpine`
- Digest: `sha256:379f8ca470e9d442f4742f33a50449638810c82e572b670354db5dbef32ed090`
- Aktualisiert auf Docker Hub: 2026-08-27

Weitere Informationen: https://docker.io/portainer/portainer-ee

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

- Docker Hub image: `docker.io/portainer/portainer-ee:2.44.0-alpine`
- Digest: `sha256:dbb2ae19e5e690105b087201c12f78b7f0c7e8a4694094258105fe040cc18b32`
- Aktualisiert auf Docker Hub: 2026-07-30

Weitere Informationen: https://docker.io/portainer/portainer-ee
