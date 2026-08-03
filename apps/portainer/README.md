# Portainer Home Assistant app

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2026.8.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--31-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-201_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.44.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ce-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A5376fd96f0bae14be7285ceb24c5cf9470dc23f19cdde74ff4c65d11cbe96eb2-informational)
<!-- BADGES-END -->

Portainer CE/BE with LTS/STS selection, Home Assistant Ingress, per-user login retention, selectable storage, import/export and Watchdog support.

See [DOCS.md](DOCS.md) for configuration and migration details.

## Übersicht

- Portainer CE oder BE sowie LTS- oder STS-Kanal auswählbar
- Weboberfläche über Home Assistant Ingress
- Verwaltung der lokalen Docker-Umgebung über die Home-Assistant-Docker-API
- wählbarer Datenspeicher unter `/data`, `/config` oder `/share`
- geprüfter Import und Export von Portainer-Daten
- optionale, je Home-Assistant-Benutzer getrennte Ingress-Anmeldung

## Voraussetzungen und Sicherheit

Die App benötigt Docker-API-Zugriff und läuft deshalb mit deaktiviertem
Schutzmodus. Portainer kann Container, Images, Netzwerke und Volumes des Hosts
verwalten; der Zugriff ist ausschließlich vertrauenswürdigen Administratoren
zu gewähren. Die direkte Weboberfläche auf `9000` oder `9443` muss für Ingress
nicht veröffentlicht werden.

## Erste Schritte

Nach dem ersten Start **Weboberfläche öffnen** und innerhalb von fünf Minuten
den Administrator anlegen. Alternativ kann `advanced.admin_password` vor dem
ersten Start gesetzt werden. Danach Speicherort und optionale Import-/Export-
Einstellungen festlegen. Alle Optionen sind in [DOCS.md](DOCS.md) beschrieben.

## Installation

1. Dieses Repository in Home Assistant unter **Einstellungen → Apps → App-Store → Repositories** hinzufügen.
2. Die gewünschte App installieren und ihre Konfiguration speichern.
3. Die App starten und das Protokoll auf Fehler prüfen.

## Weitere Dokumentation

- [Vollständige App-Dokumentation](DOCS.md)
- [Versionsverlauf](CHANGELOG.md)
- [Allgemeine Speicherorte und Datenmigration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream-Projekt](https://docs.portainer.io/)
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