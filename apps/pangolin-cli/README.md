# Pangolin CLI Client

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
![Version](https://img.shields.io/badge/version-v0.15.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--20-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Image Size](https://img.shields.io/badge/size-23_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v0.15.0-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Fcli-informational)
![Commit](https://img.shields.io/badge/commit-91aed8f6aef125aa7e20d259c94167cd92d2ebd9-informational)
<!-- BADGES-END -->

Die offizielle Pangolin CLI verbindet Home Assistant OS als WireGuard-VPN-Client
mit Pangolin Cloud oder einer selbst gehosteten Pangolin-Instanz. Sie ist die
empfohlene Nachfolgerin von Olm für neue Client-Installationen.

## Übersicht

- dauerhafte Verbindung über `pangolin-cli up --attach`
- Zugriff auf entfernte Pangolin-Ressourcen über WireGuard
- Host-Netzwerkzugriff für direkt nutzbare Routen
- optionaler Admin- und Prometheus-Endpunkt auf Port `2112`
- interner Healthcheck auf Port `8097`
- unterstützt `aarch64` und `amd64`

## Voraussetzungen

- Pangolin Cloud oder eine selbst gehostete Pangolin-Instanz
- ein in Pangolin angelegter Machine Client
- Client-ID und Client-Secret dieses Machine Clients
- deaktivierter Schutzmodus für `/dev/net/tun` und `NET_ADMIN`

## Installation

1. Dieses Repository in Home Assistant unter **Einstellungen → Apps → App-Store → Repositories** hinzufügen.
2. **Pangolin CLI Client** installieren.
3. `endpoint`, `client_id` und `client_secret` eintragen.
4. Schutzmodus deaktivieren, Konfiguration speichern und die App starten.
5. Im Protokoll prüfen, ob die Anmeldung und der Tunnelaufbau erfolgreich waren.

## Konfiguration

| Option | Standard | Beschreibung |
|---|---:|---|
| `endpoint` | `https://app.pangolin.net` | URL der Pangolin-Instanz |
| `client_id` | – | ID des Machine Clients |
| `client_secret` | – | Secret des Machine Clients |
| `extras.log_level` | `info` | `trace`, `debug`, `info`, `warn` oder `error` |
| `extras.additional_args` | leer | zusätzliche, von der installierten CLI unterstützte Argumente |

Zugangsdaten dürfen nicht in `additional_args` eingetragen werden. Ausführliche
Hinweise und Fehlerhilfe stehen in [DOCS.md](DOCS.md).

## Sicherheit

Die App verwaltet mit `NET_ADMIN` Routen und ein WireGuard-Interface im
Host-Netzwerk. Veröffentlichen Sie die Ports `2112` und `8097` nur, wenn dies
wirklich benötigt wird, und beschränken Sie den Zugriff auf vertrauenswürdige
Netze.

## Weitere Dokumentation

- [Vollständige App-Dokumentation](DOCS.md)
- [Versionsverlauf](CHANGELOG.md)
- [Allgemeine Speicherorte und Datenmigration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream-Projekt](https://github.com/fosrl/cli)
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