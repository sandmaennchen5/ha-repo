# Changelog


## [1.0.44.3] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/Finsys/dockhand

---

## 1.0.44.2

- Ingress-Proxy mit Unterpfad-Unterstützung für Assets, Navigation, API, SSE und WebSockets.
- Speicherwahl zwischen `/data/dockhand`, `/config/dockhand` und einem Unterordner von `/share`; sichere Übernahme in leere Ziele.
- Optionale, je Home-Assistant-Benutzer getrennte Speicherung der Dockhand-Sitzung ohne Passwortspeicherung. Ablauf und Abmeldung bleiben wirksam.
- Direkter Zugriff bleibt auf Port 3000 verfügbar und verwendet keine gespeicherten Ingress-Sitzungen.

## 1.0.44.1

- Erste Home-Assistant-App für Dockhand 1.0.44.
- Home Assistant Ingress, optionaler Direktport und persistente Daten unter `/data`.
- Lokale Docker- und Compose-Verwaltung über die Supervisor-Docker-API.
