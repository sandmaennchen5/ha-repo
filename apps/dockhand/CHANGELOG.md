# Changelog


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
