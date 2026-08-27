# Changelog

## 1.6.0.6

- Isolate server-side login sessions from the main Drydock database to prevent independent Loki stores overwriting each other.
- Persist session mutations before acknowledging login/logout, preserving valid remembered Ingress sessions across restarts.
- Existing lost sessions require one manual login after updating. Logout and session expiry still require authentication.


## [1.6.0.5] - 2026-08-27

### Manuelles Update

- Behebt die weiße Ingress-Seite durch angepasste Vue-Router-Basis, Assets und Live-Verbindungen.
- Wählbarer Speicherort in data/config/share mit nicht überschreibender Migration.
- Optionale, getrennte Ingress-Sitzungen pro HA-Benutzer; keine Passwortspeicherung.
- Basic-Auth-Hash und zusätzliche DD_-Einstellungen über die App-Konfiguration.
- Docker Hub image: `docker.io/codeswhat/drydock:1.6.0`
- Digest: `sha256:43d4807aba1e39944275ed027d08f6ce670a07efa8916ba06a1d257a2bcbf786`
- Aktualisiert auf Docker Hub: 2026-08-12
- Behebt den Startabbruch `EPERM: chmod '/data'` durch Initialisierung von `/data/drydock` mit Eigentümer `node`.
- Die Rechte von `/data` und `options.json` bleiben unverändert; der Upstream-Benutzerwechsel bleibt aktiv.
- Eine vorhandene `/data/dd.json` wird einmalig kopiert, nicht gelöscht oder über eine vorhandene Zieldatenbank geschrieben.
- Erste Home-Assistant-App für Drydock 1.6.0.
- Home Assistant Ingress, optionaler Direktport und persistenter Store unter `/data`.
- Zugriff auf die lokale Docker Engine über die Supervisor-Docker-API.
