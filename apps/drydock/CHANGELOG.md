# Changelog

## 1.6.0.2

- Behebt den Startabbruch `EPERM: chmod '/data'` durch Initialisierung von `/data/drydock` mit Eigentümer `node`.
- Die Rechte von `/data` und `options.json` bleiben unverändert; der Upstream-Benutzerwechsel bleibt aktiv.
- Eine vorhandene `/data/dd.json` wird einmalig kopiert, nicht gelöscht oder über eine vorhandene Zieldatenbank geschrieben.

## 1.6.0.1

- Erste Home-Assistant-App für Drydock 1.6.0.
- Home Assistant Ingress, optionaler Direktport und persistenter Store unter `/data`.
- Zugriff auf die lokale Docker Engine über die Supervisor-Docker-API.
