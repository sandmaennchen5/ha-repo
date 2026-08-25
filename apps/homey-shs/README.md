### Home Assistant Repository – sandmaennchen5
## App - Homey Self-Hosted Server

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES-START -->
![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v13.4.0.5-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--05-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Image Size](https://img.shields.io/badge/size-282_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v13.4.0-yellow)
![Repo](https://img.shields.io/badge/repo-ghcr.io%2Fathombv%2Fhomey--shs-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Aaa9db022515a40479076fe2d3196f10e0d5d572a61a5d1353bebfd40441d168c-informational)
<!-- BADGES-END -->

Homey Self-Hosted Server als Home Assistant-Add-on ausführen

Die App bietet Home-Assistant-Ingress mit Socket.IO/WebSocket-Unterstützung,
wahlweise `/data`, `/config` oder `/share` als Datenspeicher sowie einen
optionalen Import und Export über `/share`. Lokale Homey-Anmeldungen können
auf Wunsch getrennt je Home-Assistant-Benutzer gespeichert werden.

## Über

Mit diesem Add-on können Sie den [Homey Self-Hosted Server](https://homey.app) innerhalb Ihrer Home Assistant OS-Installation ausführen.
Homey Self-Hosted Server ist ein reines Softwareprodukt, das auf dem Betriebssystem basiert, das [Homey Pro](https://homey.app/homey-pro/) antreibt.
Es unterstützt standardmäßig Geräte, die sich über WLAN, Ethernet, Cloud und Matter verbinden. Matter-over-Thread funktioniert ebenfalls, wenn Sie bereits einen Thread-Border-Router in Ihrem Zuhause haben. Um Zigbee-, Z-Wave-, Bluetooth LE-, 433-MHz- oder Infrarot-Geräte hinzuzufügen, schließen Sie einfach eine [Homey Bridge](https://homey.app/homey-bridge/) an, um diese drahtlosen Technologien freizuschalten – es sind keine USB-Sticks erforderlich.
[Lesen Sie die vollständige Add-on-Dokumentation][docs]

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
8. Installiere das Add-on **Homey**.
10. Starte das Add-on.

Nach dem Start des Add-ons:

1. Öffnen Sie die Homey-App auf Ihrem iOS- oder Android-Gerät
2. Wählen Sie **Neues Homey hinzufügen**
3. Wählen Sie **Selbst gehosteter Server**
4. Befolgen Sie die Anweisungen auf dem Bildschirm, um die Einrichtung abzuschließen

## Weitere Dokumentation

- Siehe [DOCS.md](DOCS.md) für vollständige Add-on-Dokumentation und Troubleshooting.
- Siehe [CHANGELOG.md](CHANGELOG.md) für den upstream Release-Überblick.
- Siehe [Speicherorte und Datenmigration](../../docs/app-storage-and-migration.md)
  für Backup-Verhalten und manuelle Wiederherstellung.

## Links

- [Homey Community-Forum Dokumentation][upstream-doc]
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

[upstream-doc]: https://community.homey.app
[upstream-repo]: https://github.com/fosrl/newt
[docs]: DOCS.md
