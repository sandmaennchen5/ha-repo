### Home Assistant Repository – sandmaennchen5
## App - Newt Client für Pangolin-Reverse-Proxy-Tunnel

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
![Watchdog](https://img.shields.io/badge/watchdog-http%3A%2F%2F%5BHOST%5D%3A%5BPORT%3A8095%5D%2Fhealth-green)
![Version](https://img.shields.io/badge/version-v1.15.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--19-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN%7CSYS_MODULE-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Image Size](https://img.shields.io/badge/size-34_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.15.0-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Fnewt-informational)
![Commit](https://img.shields.io/badge/commit-15224904a0e0981245662a55a2e75fa2aa5a6619-informational)
<!-- BADGES-END -->

Newt ist ein Home Assistant Add-on für den Pangolin WireGuard-Tunnel-Client und TCP/UDP-Proxy. Es verbindet deinen Home Assistant Host sicher mit einem Pangolin-Server und ermöglicht Zugriff auf private Dienste über einen User-Space WireGuard-Tunnel.

## Übersicht

- Add-on für den Pangolin Newt-Client
- Nutzt `host_network` für direkten Host-Netzwerkzugriff
- Erfordert zusätzliche Berechtigungen: `NET_ADMIN`, `SYS_MODULE`
- Unterstützte Architekturen: `aarch64`, `amd64`

## Installation

[![Repository hinzufügen][repoadd-badge]][repoadd]

1. Öffne Home Assistant.
2. Gehe zu **Einstellungen → Apps → App instalieren**.
3. Klicke oben rechts auf die drei Punkte (** ⋮ →**).
4. Wähle **Repositories**.
5. Füge folgende Repository-URL hinzu:
```text
https://github.com/sandmaennchen5/ha-repo
```
6. Klicke auf **Hinzufügen**.
7. Aktualisiere den Apps-Store.
8. Installiere das Add-on **Newt**.
9. Konfiguriere die Add-on-Optionen.
10. Starte das Add-on.

> Aktiviere den Docker-Socket-Zugriff: **Schutzmodus** auf der Hauptseite des Add-ons deaktivieren.

## Add-on-Konfiguration

| Option | Typ | Beschreibung |
|--------|-----|--------------|
| `endpoint` | `str` | URL des Pangolin-Servers, z. B. `https://app.pangolin.net` |
| `id` | `str` | Newt-ID aus dem Pangolin-Dashboard |
| `secret` | `str` | Newt-Secret aus dem Pangolin-Dashboard |
| `extras.log_level` | `str` | `trace`, `debug`, `info`, `warn`, `error` (Standard: `info`) |

## Wo finde ich `id` und `secret`?

1. Öffne das Pangolin-Dashboard.
2. Wähle die gewünschte Site aus oder lege eine neue an.
3. Kopiere die generierte `id` und das `secret` aus den Site-Anmeldeinformationen.

## Voraussetzungen

- Ein laufender Pangolin-Server oder eine verwaltete Pangolin-Instanz
- Eine in Pangolin registrierte Site mit Newt-ID und Secret

## Hinweise

- Das Add-on nutzt `host_network`, damit der Tunnel direkt über das Host-Netzwerk betrieben werden kann.
- Nach Änderungen an der Konfiguration muss das Add-on neu gestartet werden.

## Weitere Dokumentation

- Siehe [DOCS.md](DOCS.md) für vollständige Add-on-Dokumentation und Troubleshooting.
- Siehe [CHANGELOG.md](CHANGELOG.md) für den upstream Release-Überblick.

## Links

- [Pangolin Dokumentation][upstream-doc]
- [Newt GitHub Repository][upstream-repo]

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

[upstream-doc]: https://docs.pangolin.net
[upstream-repo]: https://github.com/fosrl/newt
