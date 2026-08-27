# Changelog


## [1.0.45.1] - 2026-08-27

### Upstream Release Notes

## ⚠️This is important security upgrade with a number of API hardenings. 

## What's new in v1.0.45

- 🐛 security hardening across the API
- ✨ KeePassXC as a secret provider - pull secrets from a .kdbx via keepassxc-cli, bulk or inline refs (#1460)
- ✨ compose generated from a container now captures network config and resource limits (#1464)
- ✨ compose validate flags a service with no healthcheck and a defined-but-unused named volume
- ✨ optional Webhook column on the stacks list with a git stack's webhook id and copy-URL button (#845)
- ✨ sort by Disk I/O and Net I/O - the header cycles read/write and down/up (#1111)
- ✨ option to disable the session timeout (#1302)
- 🐛 pausing or resuming a backup schedule no longer clears the retention policy (#1462)
- 🐛 emergency script to relocate stack paths after moving DATA_DIR (#651, #904)
- 🐛 git stacks can now set a custom icon (#1473)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.45
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.44.6] - 2026-08-27

- Ingress-Menülinks laden Seiten serverseitig, damit der für `/` gebaute Client-Router keine HA-Ingress-Unterpfade als unbekannte Routen behandelt.
- Gilt auch für dynamisch eingefügte Links; Direktzugriff auf Port 3000 bleibt unverändert.
- Seitenwechsel laden die Oberfläche neu. Gespeicherte Anmeldungen bleiben unverändert.
- App-Revision für einen vollständigen Neuaufbau um eins erhöht.
- Ingress-Proxy mit Unterpfad-Unterstützung für Assets, Navigation, API, SSE und WebSockets.
- Speicherwahl zwischen `/data/dockhand`, `/config/dockhand` und einem Unterordner von `/share`; sichere Übernahme in leere Ziele.
- Optionale, je Home-Assistant-Benutzer getrennte Speicherung der Dockhand-Sitzung ohne Passwortspeicherung. Ablauf und Abmeldung bleiben wirksam.
- Direkter Zugriff bleibt auf Port 3000 verfügbar und verwendet keine gespeicherten Ingress-Sitzungen.
- Erste Home-Assistant-App für Dockhand 1.0.44.
- Home Assistant Ingress, optionaler Direktport und persistente Daten unter `/data`.
- Lokale Docker- und Compose-Verwaltung über die Supervisor-Docker-API.
