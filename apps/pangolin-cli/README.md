### Home Assistant Repository – sandmaennchen5
## App - Pangolin CLI Client and Site

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
![Version](https://img.shields.io/badge/version-v0.18.1.4-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--05-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-29_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v0.18.1-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Fcli-informational)
![Commit](https://img.shields.io/badge/commit-8f52452891eb9315af9e9cd31cbaa725d3ccb70d-informational)
<!-- BADGES-END -->

Die offizielle Pangolin CLI verbindet Home Assistant OS als WireGuard-VPN-Client
oder Site Connector mit Pangolin Cloud oder einer selbst gehosteten Instanz.
Der Client-Modus ersetzt Olm, der Site-Modus übernimmt die Funktionen von Newt.

## Übersicht

- dauerhafte Verbindung über `pangolin-cli up --attach`
- Zugriff auf entfernte Pangolin-Ressourcen über WireGuard
- Host-Netzwerkzugriff für direkt nutzbare Routen
- optionaler Admin- und Prometheus-Endpunkt auf Port `2112`
- lokaler Prozess-Healthcheck ohne TCP-Port
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
| `mode` | `client` | `client`, `site` oder `dual` |
| `site_id` | leer | Site-ID (nur Site-Modus) |
| `site_secret` | leer | Site-Secret (nur Site-Modus) |
| `site` | lokaler Docker-Socket | optionale Site-Einstellungen, siehe unten |
| `client_id` | – | ID des Machine Clients |
| `client_secret` | – | Secret des Machine Clients |
| `extras.log_level` | `info` | `trace`, `debug`, `info`, `warn` oder `error` |
| `extras.additional_args` | leer | zusätzliche, von der installierten CLI unterstützte Argumente |

Zugangsdaten dürfen nicht in `additional_args` eingetragen werden. Ausführliche
Hinweise und Fehlerhilfe stehen in [DOCS.md](DOCS.md).

## Sicherheit

Die App verwaltet mit `NET_ADMIN` Routen und ein WireGuard-Interface im
Host-Netzwerk. Aktivieren Sie den optionalen Endpunkt auf Port `2112` nur, wenn dies
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

## Site-Modus (Newt-Nachfolger)

Mit `mode: site` startet die App `pangolin-cli up site`. Client-Zugangsdaten
werden in diesem Modus nicht benötigt. Bestehende Konfigurationen ohne `mode`
starten weiterhin als Machine Client.

```yaml
mode: site
endpoint: https://pangolin.example.com
site_id: DEINE-NEWT-ID
site_secret: DEIN-NEWT-SECRET
site:
  disable_clients: false
  disable_ssh: false
  metrics: true
  metrics_admin_addr: 127.0.0.1:2112
extras:
  log_level: info
  additional_args: ""
```

Für die Migration von Pangolin Newt dessen `id` und `secret` als `site_id` und
`site_secret` übernehmen. Die alte Newt-App vor dem Start stoppen, damit dieselbe
Site nicht doppelt verbunden wird. Erweiterte Newt-Optionen stehen unter `site`.

Alternativ `site.provisioning_key` verwenden und beide Site-Zugangsdaten leer
lassen. Die erhaltenen Zugangsdaten werden standardmäßig in
`/data/pangolin-site.json` gespeichert und mit der App gesichert. Ein vorhandenes
JSON kann mit `site.config_file` geladen werden. Eigene Dateien wie Blueprints,
Zertifikate und Skripte können unter `/config` (App-Konfigurationsverzeichnis)
abgelegt werden; Pfade beziehen sich immer auf den App-Container.


[Alle Site-Optionen](DOCS.md#site-modus-newt-nachfolger)

## Dual-Modus: Client und Site gleichzeitig

Mit `mode: dual` laufen Machine Client und Site Connector gleichzeitig als zwei
getrennte s6-Dienste. Beide werden unabhängig neu gestartet, wenn ihr Prozess
endet. Der Prozess-Healthcheck prüft im Dual-Modus beide CLI-Prozesse.

```yaml
mode: dual
endpoint: https://pangolin.example.com
client_id: DEINE-CLIENT-ID
client_secret: DEIN-CLIENT-SECRET
site_id: DEINE-SITE-ID
site_secret: DEIN-SITE-SECRET
site: {}
extras:
  log_level: info
  additional_args: ""
  client_additional_args: ""
  site_additional_args: ""
```

Die IDs und Secrets gehören jeweils zum Machine Client bzw. zur Site. Beide
verwenden denselben `endpoint`. Für die Site funktionieren weiterhin Provisioning
und eine gespeicherte JSON-Konfiguration als Alternative zu ID und Secret.
Beide IDs einzutragen aktiviert Dual nicht automatisch; dafür `mode: dual` wählen.

Standard-Interfaces im Dual-Modus: Client `pangolin-client`, Site-Client-Tunnel
`pangolin-site`, nativer Site-Haupttunnel `pangolin-main`. Eigene Namen über
`client.interface_name`, `site.interface` und `site.interface_main` müssen
unterschiedlich sein. Die beiden Site-Namen betreffen native Interfaces.

`client.http_addr` aktiviert optional die HTTP-API des Clients, zum Beispiel
`127.0.0.1:2113`. Ohne diese Option behält der Client seine Upstream-Konfiguration.
Die Site-Metriken verwenden standardmäßig `127.0.0.1:2112`; wenn beide HTTP-Server
aktiv sind, müssen sie verschiedene Bind-Adressen/Ports verwenden.

`extras.additional_args` gilt im Dual-Modus nur für den Client. Zusätzlich
stehen `extras.client_additional_args` und `extras.site_additional_args` für die
jeweilige Rolle zur Verfügung, auch in den Einzelmodi. Werte werden durch
Leerzeichen getrennt; Shell-Quoting wird nicht ausgewertet.

Die alte Newt-App vor dem Start derselben Site stoppen. Die Tunnel teilen das
Host-Netzwerk; Zielnetze und VPN-Routen müssen zur Pangolin-Konfiguration passen.

## Lokale Docker-Integration

In `site` und `dual` kann die CLI die lokalen Docker-Container erkennen.
Der Socket ist über `docker_api: true` eingebunden; Schutzmodus deaktivieren.
Für neue Installationen ist er voreingestellt. Bei bestehenden Konfigurationen
gegebenenfalls ergänzen:

```yaml
site:
  docker_socket: "unix:///var/run/docker.sock"
```

Ein externer Socket-Proxy kann weiterhin als `site.docker_socket` verwendet werden.
