# Portainer Agent Home Assistant app

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
![Watchdog](https://img.shields.io/badge/watchdog-tcp%3A%2F%2F%5BHOST%5D%3A%5BPORT%3A9001%5D-green)
![Version](https://img.shields.io/badge/version-v2.39.5.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--13-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![AppArmor](https://img.shields.io/badge/apparmor-True-blue)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-35_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.39.5-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fagent-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Aec9223788fe62872bc78d23ad4f4a5558ff560500d2602f378ea191f560f491e-informational)
<!-- BADGES-END -->

Portainer Agent with LTS/STS selection, environment options and Watchdog support. It intentionally has no Web UI, storage migration, import or export.

See [DOCS.md](DOCS.md).

## Übersicht

Diese feste Variante stellt den offiziellen **Portainer Agent im LTS-Kanal**
auf TCP-Port `9001` bereit. Sie besitzt keine Weboberfläche und speichert keine
Anwendungsdaten.

## Einrichtung und Sicherheit

Schutzmodus deaktivieren, App starten und in Portainer eine Docker-Umgebung mit
`<HOME-ASSISTANT-IP>:9001` anlegen. Ein konfiguriertes `agent_secret` muss auf
Server und Agent identisch sein. Port `9001` ausschließlich für den
Portainer-Server freigeben. Weitere Optionen stehen in [DOCS.md](DOCS.md).

## Installation

1. Dieses Repository in Home Assistant unter **Einstellungen → Apps → App-Store → Repositories** hinzufügen.
2. Die gewünschte App installieren und ihre Konfiguration speichern.
3. Die App starten und das Protokoll auf Fehler prüfen.

## Weitere Dokumentation

- [Vollständige App-Dokumentation](DOCS.md)
- [Versionsverlauf](CHANGELOG.md)
- [Allgemeine Speicherorte und Datenmigration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream-Projekt](https://docs.portainer.io/admin/environments/add/docker/agent)
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