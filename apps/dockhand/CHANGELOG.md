# Changelog


## [1.0.46.1] - 2026-09-02

### Upstream Release Notes

## What's new in v1.0.46

- ✨ restart a stack in depends_on order, keeping the same containers (#1480)
- ✨ allow secret-less git webhooks via the ALLOW_WEBHOOKS_WITHOUT_SECRET env var
- ✨ optional STACKS_DIR flat layout for local stacks (#514, #778, PR#1482, @xd003)
- 🐛 faster incremental backups when multiple stacks share one repository (#1494)
- 🐛 "disable build cache" no longer errors on deploy (#1479, PR#1020, @He-Is-HaZaRdOuS)
- 🐛 test connection on a saved environment without re-entering the token (#1483)
- 🐛 populate environment variables again finds the repo's .env file (#1495)
- 🐛 POST /api/stacks honors the target environment in the body (#1491)
- 🐛 large image scans no longer fail when the scanner log rotates (#1496)
- 🐛 Compose Validate no longer false-flags a valid env_file (#1497)
- 🐛 cache app icons in one request so the containers and stacks pages load faster
- 🐛 upgrade svelte to 5.56.10 (#1476, PR#1477, @ThanatosDi)
- 🐛 refresh the bundled docker-compose (5.5.0-r2)
- 🐛 stricter per-environment access and permission checks across the API
- 🐛 redact secret values from compose command output and restrict backup restore targets
- 🐛 local-path backup destinations now reject a host path that isn't a Dockhand bind mount (#1506)
- 🐛 escape $ in env values when generating a compose file from a container (#1507)
- 🐛 clearer git permission errors that match the credential type (token vs SSH key) (#1509)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.46
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

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
