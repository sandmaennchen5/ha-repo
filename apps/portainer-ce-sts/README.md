# Portainer Home Assistant app

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Watchdog](https://img.shields.io/badge/watchdog-http%3A%2F%2F%5BHOST%5D%3A%5BPORT%3A9000%5D%2Fapi%2Fsystem%2Fstatus-green)
![Version](https://img.shields.io/badge/version-v2.44.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--30-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![AppArmor](https://img.shields.io/badge/apparmor-True-blue)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-65_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.44.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ce-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A5376fd96f0bae14be7285ceb24c5cf9470dc23f19cdde74ff4c65d11cbe96eb2-informational)
<!-- BADGES-END -->

Portainer CE/BE with LTS/STS selection, Home Assistant Ingress, per-user login retention, selectable storage, import/export and Watchdog support.

See [DOCS.md](DOCS.md) for configuration and migration details.

## Übersicht

Diese feste Variante verwendet **Portainer Community Edition im STS-Kanal**.
Sie bietet Home Assistant Ingress, Docker-Verwaltung, wählbaren Datenspeicher,
Import/Export, Watchdog und eine optionale benutzerbezogene Ingress-Sitzung.

## Voraussetzungen und erster Start

Wegen des Docker-API-Zugriffs muss der Schutzmodus deaktiviert sein. Öffnen Sie
nach dem Start innerhalb von fünf Minuten die Weboberfläche und legen Sie den
Administrator an. STS erhält neue Funktionen früher als LTS und kann häufiger
Änderungen enthalten. Details stehen in [DOCS.md](DOCS.md).

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