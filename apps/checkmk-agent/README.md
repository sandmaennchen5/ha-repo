# Checkmk Agent für Home Assistant

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
<!-- BADGES-END -->

Stellt den offiziellen Checkmk-Agenten als Home-Assistant-App auf TCP-Port
`6556` bereit. Eine Checkmk-Site kann den Agenten abfragen und die innerhalb
des App-Containers sichtbaren Systeminformationen auswerten.

- Architekturen: `amd64`, `aarch64`
- Keine WebUI
- Keine App-Optionen erforderlich
- TCP-Watchdog und Container-Healthcheck
- Automatische Upstream-Aktualisierung; Checkmk `X.Y.ZpN` wird als App-Version `X.Y.Z.N.R` veröffentlicht

## Voraussetzungen

- eine erreichbare Checkmk-Site
- Netzwerkzugriff von der Checkmk-Site zur IP des Home-Assistant-Hosts
- eine Firewall-Regel für TCP-Port `6556` ausschließlich aus dem Monitoring-Netz

Weitere Hinweise stehen in [DOCS.md](DOCS.md).

## Installation

1. Dieses Repository in Home Assistant unter **Einstellungen → Apps → App-Store → Repositories** hinzufügen.
2. **Checkmk Agent** installieren und starten.
3. Prüfen, ob `6556/tcp` auf Port `6556` des Hosts veröffentlicht ist.
4. Den Home-Assistant-Host in Checkmk mit seiner IP-Adresse aufnehmen.
5. Agentenverbindung testen und anschließend die Service-Erkennung ausführen.

## Sicherheit und Umfang

Der klassische Agent liefert seine Ausgabe unverschlüsselt. Port `6556` darf
nicht ins Internet weitergeleitet werden; verwenden Sie Firewall, VPN oder eine
von Checkmk unterstützte verschlüsselte Verbindung. Da der Agent in einem
Container läuft, sieht er nicht automatisch sämtliche Prozesse und Dateien des
Home-Assistant-Hosts.

Details zu Verbindungstest, Versionierung und Einschränkungen stehen in
[DOCS.md](DOCS.md).

## Weitere Dokumentation

- [Vollständige App-Dokumentation](DOCS.md)
- [Versionsverlauf](CHANGELOG.md)
- [Allgemeine Speicherorte und Datenmigration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream-Projekt](https://checkmk.com/)
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