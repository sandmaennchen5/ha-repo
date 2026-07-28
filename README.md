# Home Assistant Repository – sandmaennchen5

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

## Über

Home Assistant ermöglicht es jedem, Add-on-Repositorys zu erstellen, um seine
Add-ons für Home Assistant einfach zu teilen. Dieses Repository ist eines dieser Repositorys und
bietet zusätzliche Home Assistant-Add-ons für Ihre Installation.

## Installation

[![Repository hinzufügen][repoadd-badge]][repoadd]

### Falls der Button nicht funktioniert

Aufgrund eines bekannten Problems mit My Home Assistant kann es vorkommen, dass der Add-on-Store geöffnet wird, das Repository jedoch nicht automatisch hinzugefügt wird

1. Öffne Home Assistant.
2. Gehe zu **Einstellungen → Apps → App instalieren**.
3. Klicke oben rechts auf die drei Punkte (** ⋮ →**).
4. Wähle **Repositories**.
5. Füge folgende Repository-URL hinzu:
```text
[repo]
```
6. Klicke auf **Hinzufügen**.
7. Aktualisiere den Apps-Store.

Danach stehen die Apps aus diesem Repository zur Installation bereit.

> **Hinweis:** Sollte der Installationsbutton nur den Add-on-Store öffnen, nutze bitte die manuelle Installation über die oben angegebene Repository-URL.

## Apps von dieser Repository bereitgestellt

<!-- APPS-LIST-START -->
## [🏠 Homey Self-Hosted Server](apps/homey-shs/)

Run Homey Self-Hosted Server on Home Assistant OS.

![Version](https://img.shields.io/badge/version-v13.4.0-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--28-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Image Size](https://img.shields.io/badge/size-265_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v13.4.0-yellow)
![Repo](https://img.shields.io/badge/repo-ghcr.io%2Fathombv%2Fhomey--shs-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A97b00d6a074f8abc5d14a457f32e1c7a2b0bcbadfd56999932292efbe071abb9-informational)

## [🛰️ Newt - Pangolin Tunnels](apps/newt/)

Secure remote access with Pangolin tunnels.

![Version](https://img.shields.io/badge/version-v1.15.0-blue)
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

<!-- APPS-LIST-END -->

## Dashboard

Das automatisch generierte Dashboard mit Badge-Matrix, Health-Score und History ist verfügbar auf:
**[GitHub Pages Dashboard][repodashboard]**

## 💖 Unterstütze die Entwicklung

Wenn dir dieses Apps Zeit spart oder die Einrichtung erleichtert, wäre ich dir für deine Unterstützung sehr dankbar!

[![PayPal][paypal-badge]][paypal-link]

## Support
Hast du Fragen?
Du hast mehrere Möglichkeiten, Antworten zu erhalten:

- Das Home Assistant [Community-Forum][forum]
- Issues in diesem Repository [Issues][repoissues]

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
[repoadd-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repoadd]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo
[repo]: https://github.com/sandmaennchen5/ha-repo
[repoissues]: https://github.com/sandmaennchen5/ha-repo/issues)
[repodashboard]: https://sandmaennchen5.github.io/ha-repo/
[paypal-badge]: https://img.shields.io/badge/PayPal-Spenden-blue?logo=paypal
[paypal-link]: https://www.paypal.me/sandmaennchen5
[forum]: https://community.home-assistant.io/
