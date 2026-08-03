# ADS-B Multi-Portal Feeder

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
<!-- BADGES-END -->

Docker-Image für dump1090-fa, fr24feed, FlightAware, adsbexchange, Plane Finder, OpenskyNetwork, adsb.fi, ADSBHub und Radarbox.

## Über

Add-on zur Übertragung von ADS-B-Daten von einem kostengünstigen USB-ADS-B-Stick (z. B. Nooelec NESDR Mini) an FlightRadar24, FlightAware, ADSBexchange und Plane Finder auf Basis von dump1090.

Dieses Add-on basiert auf dem Docker-Image [docker-fr24feed-piaware-dump1090](https://github.com/Thom-x/docker-fr24feed-piaware-dump1090) von Thom-x

[Lesen Sie die vollständige Add-on-Dokumentation][docs]

## Übersicht

- verarbeitet ADS-B-Daten eines lokalen RTL-SDR-Empfängers mit dump1090-fa
- kann Daten unter anderem an FlightAware, Flightradar24, ADS-B Exchange,
  adsb.fi, Plane Finder, OpenSky, RadarBox und ADSBHub weitergeben
- integrierte Dump1090-Weboberfläche über Home Assistant Ingress
- optionale TCP-Ausgaben in Raw-, BaseStation- und Beast-Formaten
- übernimmt auf Wunsch Standortdaten aus Home Assistant
- unterstützt `aarch64` und `amd64`

## Voraussetzungen

- kompatibler RTL-SDR-Dongle, sofern kein Netzwerkempfänger verwendet wird
- Antenne mit geeignetem Standort und Empfang für 1090 MHz
- Zugangsdaten oder Freigabeschlüssel der gewünschten Feeder-Portale
- Internetzugang zu den aktivierten Portalen

## Installation

1. Dieses Repository unter **Einstellungen → Apps → App-Store → Repositories** hinzufügen.
2. **ADS-B Multi-Portal Feeder** installieren und den RTL-SDR-Dongle anschließen.
3. Standort, aktivierte Dienste und deren Zugangsdaten konfigurieren.
4. Konfiguration speichern und die App starten.
5. Protokoll auf USB-, Empfänger- und Anmeldefehler prüfen.
6. Die Weboberfläche öffnen und kontrollieren, ob Flugzeuge empfangen werden.

## Grundkonfiguration

| Option | Standard | Beschreibung |
|---|---:|---|
| `SERVICE_ENABLE_DUMP1090` | `true` | lokalen ADS-B-Empfänger aktivieren |
| `SERVICE_ENABLE_PIAWARE` | `true` | FlightAware-Feeder aktivieren |
| `SERVICE_ENABLE_FR24FEED` | `true` | Flightradar24-Feeder aktivieren |
| `SERVICE_ENABLE_HTTP` | `true` | Dump1090-Weboberfläche aktivieren |
| `HTML_SITE_LAT` / `HTML_SITE_LON` | HA-Standort | Position der Empfangsstation |
| `HTML_SITE_ALT` | HA-Höhe | Stationshöhe über dem Meeresspiegel |
| `DUMP1090_ADDITIONAL_ARGS` | leer | zusätzliche dump1090-Argumente |

Feeder ohne gültige Kennung oder Zugangsdaten sollten deaktiviert werden. Die
vollständige Optionsliste mit portalspezifischer Einrichtung steht in
[DOCS.md](DOCS.md).

## Netzwerk und Sicherheit

Ingress benötigt keine zusätzliche Portfreigabe. Die Ports `30001` bis
`30005` sowie die Statusports `8080`, `8754` und `30053` sollten nur dann dem
Host zugeordnet werden, wenn ein externer Empfänger oder Client sie benötigt.
Veröffentlichen Sie Rohdaten und Statusseiten nicht ungeschützt im Internet.

## Support

Erstellen Sie ein Issue auf GitHub.

## Danksagungen

- Ein großes Dankeschön und ❤️ geht an [Thom-x](https://github.com/Thom-x) für seine Arbeit an [docker-fr24feed-piaware-dump1090](https://github.com/Thom-x/docker-fr24feed-piaware-dump1090)

[docs]: DOCS.md

## Weitere Dokumentation

- [Vollständige App-Dokumentation](DOCS.md)
- [Versionsverlauf](CHANGELOG.md)
- [Allgemeine Speicherorte und Datenmigration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream-Projekt](https://github.com/sandmaennchen5/ha-repo)
- [Repository-Support](https://github.com/sandmaennchen5/ha-repo/issues)

<!-- LINKS -->
[builder-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/hasos-app.yaml?logo=buildkite&label=Builder
[builder-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/hasos-app.yaml
[lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-badge.yaml?logo=lintcode&label=Lint
[lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-badge.yaml
[docker-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-docker.yaml?logo=Docker&label=DockerLint
[docker-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-docker.yaml
[yaml-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-yaml.yaml?logo=yaml&label=YamlLint
[yaml-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-yaml.yaml
[codefactor-badge]: https://img.shields.io/codefactor/grade/github/sandmaennchen5/ha-repo?logo=codefactor
[codefactor-url]: https://www.codefactor.io/repository/github/sandmaennchen5/ha-repo/branches
[paypal-badge]: https://img.shields.io/badge/PayPal-Spenden-blue?logo=paypal
[paypal-link]: https://www.paypal.me/sandmaennchen5
[repoadd-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repo]: https://github.com/sandmaennchen5/ha-repo
[repoadd]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo
[repodev]: https://github.com/sandmaennchen5/ha-repo#dev
[repoadddev]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo%23dev
[repoissues]: https://github.com/sandmaennchen5/ha-repo/issues
[repodashboard]: https://sandmaennchen5.github.io/ha-repo/