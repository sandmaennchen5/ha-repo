# Changelog

## 1.0.44.5 - 2026-08-27

- Setzt die SvelteKit-Router-Basis in der HTML-Startkonfiguration vor dem Import der Client-Module auf den Ingress-Pfad.
- Interne Routennamen und Hydrierungsdaten bleiben unverändert; das bisherige pauschale Umschreiben konnte Unterseiten beim Start als unbekannte Routen behandeln.
- Regressionstest für direkten Unterseitenaufruf unter HTTP/HTTPS, relative/absolute Basis und dynamische Routen.
- Keine Änderungen an Pangolin/Newt, Speicher oder Anmeldungen.

## 1.0.44.4 - 2026-08-27

- Ingress-Menülinks laden Seiten serverseitig, damit der für `/` gebaute Client-Router keine HA-Ingress-Unterpfade als unbekannte Routen behandelt.
- Gilt auch für dynamisch eingefügte Links; Direktzugriff auf Port 3000 bleibt unverändert.
- Seitenwechsel laden die Oberfläche neu. Gespeicherte Anmeldungen bleiben unverändert.


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
