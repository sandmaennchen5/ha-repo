# Olm – Pangolin Client

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
![Version](https://img.shields.io/badge/version-v1.9.0.4-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--19-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN%7CSYS_MODULE-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Image Size](https://img.shields.io/badge/size-27_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.9.0-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Folm-informational)
![Commit](https://img.shields.io/badge/commit-8c1db4bada7e7425a2500ea5d76df8b85f407a91-informational)
<!-- BADGES-END -->

Olm verbindet Home Assistant OS über einen verschlüsselten WireGuard-Tunnel mit
Pangolin- und Newt-Standorten. Die App eignet sich für erweiterte
Remote-Access-Szenarien, in denen Home Assistant auf entfernte private Netze
zugreifen soll.

> Olm wird upstream zugunsten der **Pangolin CLI** schrittweise abgelöst. Für
> neue Installationen wird deshalb die App **Pangolin CLI Client** empfohlen.

## Übersicht

- Verbindung zu Pangolin Cloud oder einer selbst gehosteten Pangolin-Instanz
- konfigurierbare WireGuard-Schnittstelle, MTU und DNS-Auflösung
- Optionen für Hole-Punching, Relay und lokale Routen
- interner HTTP-Healthcheck mit Home-Assistant-Watchdog
- unterstützt `aarch64` und `amd64`

## Voraussetzungen

- ein in Pangolin angelegter Olm-Client mit ID und Secret
- ein vom Home-Assistant-Host erreichbarer Pangolin-Endpunkt
- deaktivierter Schutzmodus, da `/dev/net/tun`, `NET_ADMIN`, `SYS_MODULE` und
  Host-Netzwerkzugriff benötigt werden

## Installation

1. Dieses Repository in Home Assistant unter **Einstellungen → Apps → App-Store → Repositories** hinzufügen.
2. **Olm – Pangolin Client** installieren.
3. `endpoint`, `id` und `secret` aus Pangolin eintragen.
4. Schutzmodus deaktivieren, Konfiguration speichern und die App starten.
5. Im Protokoll prüfen, ob Tunnel, DNS und Routen erfolgreich eingerichtet wurden.

## Wichtige Optionen

| Option | Standard | Beschreibung |
|---|---:|---|
| `endpoint` | `https://app.pangolin.net` | URL der Pangolin-Instanz |
| `id` | – | Client-ID aus Pangolin |
| `secret` | – | geheimer Clientschlüssel |
| `network.mtu` | `1280` | MTU der WireGuard-Schnittstelle |
| `network.dns` | `8.8.8.8` | DNS-Server im Tunnel |
| `network.interface` | `olm` | Name der Netzwerkschnittstelle |
| `extras.log_level` | `INFO` | Protokollstufe von `DEBUG` bis `FATAL` |

Alle Optionen und eine vollständige Beispielkonfiguration stehen in
[DOCS.md](DOCS.md).

## Sicherheit

ID und Secret gehören ausschließlich in die App-Konfiguration. Die App erhält
weitreichende Netzwerkrechte; installieren Sie sie daher nur auf einem
vertrauenswürdigen Home-Assistant-System. Der Healthcheck benötigt keinen TCP-Port.

## Weitere Dokumentation

- [Vollständige App-Dokumentation](DOCS.md)
- [Versionsverlauf](CHANGELOG.md)
- [Allgemeine Speicherorte und Datenmigration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream-Projekt](https://github.com/fosrl/olm)
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
