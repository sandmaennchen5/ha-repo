# Changelog

## [0.18.1.3] - 2026-10-05

- Dual-Modus für gleichzeitigen Machine Client und Site Connector.
- Zwei getrennte s6-Dienste mit unabhängigen Neustarts; Healthcheck prüft beide aktiven Prozesse.
- Unterschiedliche Standard-Interfaces und getrennte zusätzliche Argumente je Rolle.
- Optionale Client-Interface- und HTTP-API-Einstellungen.

## [0.18.1.2] - 2026-10-05

- Wählbarer Client- und Site-Modus mit SITE_ID und SITE_SECRET.
- Site-ENV-Optionen einschließlich Provisioning, Metriken, mTLS, Blueprints und nativen Interfaces.
- Persistente Site-Konfiguration unter /data und Zugriff auf das App-Konfigurationsverzeichnis.
- Bestehende Machine-Client-Konfigurationen bleiben kompatibel.


## [0.18.1.1] - 2026-10-01

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/cli@sha256:c64847e840302eab60cb3ec6fec0ee57e6a3534c23bff80621ad0c4b5e1dee27`
- Docker Hub: `docker.io/fosrl/pangolin-cli@sha256:c64847e840302eab60cb3ec6fec0ee57e6a3534c23bff80621ad0c4b5e1dee27`
**Tag:** `0.18.1`

## What's Changed

- Fix replace excluded routes if interface is removed
- Fix add exclude routes for websocket endpoint

**Full Changelog**: https://github.com/fosrl/cli/compare/0.18.0...0.18.1

Weitere Informationen: https://github.com/fosrl/cli/releases/latest

---

## [0.18.0.1] - 2026-09-29

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/cli@sha256:a3607f2aa23d830eef07f161cb342c3e2a442beda150c7bac013412f63e022ff`
- Docker Hub: `docker.io/fosrl/pangolin-cli@sha256:a3607f2aa23d830eef07f161cb342c3e2a442beda150c7bac013412f63e022ff`
**Tag:** `0.18.0`

## What's Changed
* Add support for exit nodes
* Add support for subnet routing
* Add ManagedBy build flag to disable auto-updates whne nessicary by @ToBinio in https://github.com/fosrl/cli/pull/117
* Add `--config-file` support to site service by @itsjxck in https://github.com/fosrl/cli/pull/149

## New Contributors
* @ToBinio made their first contribution in https://github.com/fosrl/cli/pull/117
* @itsjxck made their first contribution in https://github.com/fosrl/cli/pull/149

**Full Changelog**: https://github.com/fosrl/cli/compare/0.17.0...0.18.0

Weitere Informationen: https://github.com/fosrl/cli/releases/latest

---

## [0.17.0.1] - 2026-09-15

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/cli@sha256:cb9b46cb0e14966c50d49676e43b7206c77267fd0ec490a3d48b86faa419bc37`
- Docker Hub: `docker.io/fosrl/pangolin-cli@sha256:cb9b46cb0e14966c50d49676e43b7206c77267fd0ec490a3d48b86faa419bc37`
**Tag:** `0.17.0`

## What's Changed
* Add site support with `pangolin up site`
* Support machine client use on Windows
* Add service management support on Windows, Linux, MacOS for sites and clients `pangolin service install site/client`
* Improve login command when already logged in  
* Update dependencies

**Full Changelog**: https://github.com/fosrl/cli/compare/0.16.0...0.17.0

Weitere Informationen: https://github.com/fosrl/cli/releases/latest

---

## [0.16.0.3] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/cli

---

## [0.16.0.2] - 2026-08-27

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/fosrl/cli

---

## [0.16.0.1] - 2026-08-21

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/cli@sha256:a25a6d81b1f6c20f9f4c47fda4c82e61ec5a7cf72f6465174db552b0fe616434`
- Docker Hub: `docker.io/fosrl/pangolin-cli@sha256:a25a6d81b1f6c20f9f4c47fda4c82e61ec5a7cf72f6465174db552b0fe616434`
**Tag:** `0.16.0`


## What's Changed
* Add support for Pangolin (>= 1.22.0) AI Gateway private resources
* Add support for configuring common AI clients to connect to Pangolin AI Gateway resources

**Full Changelog**: https://github.com/fosrl/cli/compare/0.15.1...0.16.0

Weitere Informationen: https://github.com/fosrl/cli/releases/latest

---

## [0.15.1.2] - 2026-08-27

- Healthcheck ohne TCP-Port; entfernt den HTTP-Healthserver und die socat-Abhängigkeit.
- Verhindert Health-Port-Konflikte im Host-Netzwerk, auch bei parallelen App-Instanzen.
- Der Docker-Healthcheck prüft den App-Prozess direkt.


## [0.15.1.1] - 2026-08-03

### Upstream Release Notes

## Container Images
- GHCR: `ghcr.io/fosrl/cli@sha256:18575106ba5c2e705df293396d7edeca36fab39fa551fe4ccfb0977f644cc82a`
- Docker Hub: `docker.io/fosrl/pangolin-cli@sha256:18575106ba5c2e705df293396d7edeca36fab39fa551fe4ccfb0977f644cc82a`
**Tag:** `0.15.1`


## What's Changed
* Fix some websocket disconnections by adding deadlines to websocket
* Fix local to relay flapping if there is an overlapping CIDR route with a site local address
* Support -i in the native Pangolin ssh command


**Full Changelog**: https://github.com/fosrl/cli/compare/0.15.0...0.15.1

Weitere Informationen: https://github.com/fosrl/cli/releases/latest

---

## [0.15.0.1] - 2026-07-31

- `BUILD_FROM` wird zentral und architekturspezifisch aus `build.json` übernommen.
- Doppelpflege des Basisimages im Dockerfile entfernt.
- Erste Home-Assistant-App auf Basis der Pangolin CLI 0.15.0.
- Dauerhafter Machine-Client-Modus mit Pangolin-Endpunkt und Zugangsdaten.
