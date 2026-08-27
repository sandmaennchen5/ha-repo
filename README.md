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
https://github.com/sandmaennchen5/ha-repo
```
6. Klicke auf **Hinzufügen**.
7. Aktualisiere den Apps-Store.

Danach stehen die Apps aus diesem Repository zur Installation bereit.

> **Hinweis:** Sollte der Installationsbutton nur den Add-on-Store öffnen, nutze bitte die manuelle Installation über die oben angegebene Repository-URL.

## Speicher und Migration

Die gemeinsame Anleitung [Speicherorte und Datenmigration für
Home-Assistant-Apps](docs/app-storage-and-migration.md) erklärt `/data`,
`/config`, `/share`, Backups sowie den sicheren Wechsel zwischen App-Varianten.

## Apps von dieser Repository bereitgestellt

<!-- APPS-LIST-START -->
## [✈️ ADS-B Multi-Portal Feeder](apps/adsb-multi-portal-feeder/)

Dump1090 based feeder for FlightRadar24, FlightAware and more

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Hass.io API](https://img.shields.io/badge/hassio_api-True-blue)
![HA API](https://img.shields.io/badge/ha_api-True-blue)
![Version](https://img.shields.io/badge/version-v2.8.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--05--28-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Image Size](https://img.shields.io/badge/size-206_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.8.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fthomx%2Ffr24feed--piaware-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A582c604751c9d30970bf0d11e4cb6da65b04e27bb02b7eed463d08e627a4f8c7-informational)

## [📊 Checkmk Agent](apps/checkmk-agent/)

Expose the Checkmk monitoring agent on port 6556.

![Version](https://img.shields.io/badge/version-v2.5.0.12.2-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--21-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Image Size](https://img.shields.io/badge/size-12_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.5.0p12-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2FCheckmk%2Fcheckmk-informational)
![Commit](https://img.shields.io/badge/commit-1a1870ce0c8a0b27932ffb5c5f400971551a9f8d-informational)

## [🛟 Dockhand](apps/dockhand/)

Modern Docker and Compose management with Home Assistant Ingress.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v1.0.45.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-181_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.0.45-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2FFinsys%2Fdockhand-informational)
![Commit](https://img.shields.io/badge/commit-5adb374c0d79c8df0f8524f6c7fe27bbc493a1dc-informational)

## [⚓ Drydock](apps/drydock/)

Container update monitoring and automation with Home Assistant Ingress.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v1.6.0.5-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-150_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.6.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fcodeswhat%2Fdrydock-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A43d4807aba1e39944275ed027d08f6ce670a07efa8916ba06a1d257a2bcbf786-informational)

## [🏠 Homey Self-Hosted Server](apps/homey-shs/)

Run Homey Self-Hosted Server on Home Assistant OS.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v13.4.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--19-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Image Size](https://img.shields.io/badge/size-282_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v13.4.1-yellow)
![Repo](https://img.shields.io/badge/repo-ghcr.io%2Fathombv%2Fhomey--shs-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A268b146973bddce7ee14ed5a5a8225a1b58419c15941f54916f352ff8015283f-informational)

## [🛰️ Newt - Pangolin Tunnels](apps/newt/)

Secure remote access with Pangolin tunnels.

![Version](https://img.shields.io/badge/version-v1.16.0.2-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--19-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN%7CSYS_MODULE-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Image Size](https://img.shields.io/badge/size-35_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.16.0-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Fnewt-informational)
![Commit](https://img.shields.io/badge/commit-0e415f0a01223dd53d19185083048e0017c755b3-informational)

## [🍃 Olm - Pangolin Client](apps/olm/)

Advanced WireGuard client for remote access to Pangolin and Newt sites.

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

## [🏠 OpenCCU (HA Repo)](apps/openccu/)

HomeMatic/homematicIP CCU central based on OpenCCU

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v3.89.8.20260719-ha3-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Privileged](https://img.shields.io/badge/privileged-IPC_LOCK%7CSYS_ADMIN%7CSYS_RAWIO%7CSYS_RESOURCE%7CNET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Image Size](https://img.shields.io/badge/size-248_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v3.89.8.20260719-yellow)
![Repo](https://img.shields.io/badge/repo-https%3A%2F%2Fgithub.com%2FOpenCCU%2FOpenCCU-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ab2de2ff6e8e0f3d323714aecf20fb4c634f6aa114fd3e8404bae24f8e84db9b4-informational)

## [🏠 OpenCCU (Proxy) (HA Repo)](apps/openccu-proxy/)

Proxy to externally running OpenCCU

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v0.7.0-ha3-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Image Size](https://img.shields.io/badge/size-57_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v0.7.0-yellow)
![Repo](https://img.shields.io/badge/repo-https%3A%2F%2Fgithub.com%2FOpenCCU%2FOpenCCU-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A4ea40c4b0bfa2cfdbb531d4eb2b721d532bc1964bb497a434f8f4aecc233c733-informational)

## [🏠 OpenCCU (snapshot) (HA Repo)](apps/openccu-dev/)

HomeMatic/homematicIP CCU central based on OpenCCU (Snapshot)

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v3.89.8.20260826-dfd4f38-ha3-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Privileged](https://img.shields.io/badge/privileged-IPC_LOCK%7CSYS_ADMIN%7CSYS_RAWIO%7CSYS_RESOURCE%7CNET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Image Size](https://img.shields.io/badge/size-247_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v3.89.8.20260826-dfd4f38-yellow)
![Repo](https://img.shields.io/badge/repo-https%3A%2F%2Fgithub.com%2FOpenCCU%2FOpenCCU-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A1acedc3698d9a053b8b37d8779f2ed67a9c2727d1350dd4498f258d442fc5ea4-informational)

## [🏠 OpenCCU HAP/DRAP-Helper (HA Repo)](apps/openccu-hapdrap/)

OpenCCU Helper App for HmIP-HAP / HmIPW-DRAP connectivity

![Version](https://img.shields.io/badge/version-v0.3.1-ha1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-21_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v0.3.1-yellow)
![Repo](https://img.shields.io/badge/repo-https%3A%2F%2Fgithub.com%2FOpenCCU%2FOpenCCU-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ad433ff395bed9a64075c8d341fb9196dc3fc1b312c2e7cf79e79ef63a18b0f1c-informational)

## [🦎 Pangolin CLI Client](apps/pangolin-cli/)

Official Pangolin CLI and WireGuard VPN client for Linux.

![Version](https://img.shields.io/badge/version-v0.16.0.3-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--21-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Image Size](https://img.shields.io/badge/size-24_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v0.16.0-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Fcli-informational)
![Commit](https://img.shields.io/badge/commit-dd61170ef18ee8b76286f18416ce6124a86e4098-informational)

## [🐳 Portainer (Edition Selector)](apps/portainer/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2026.8.3-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-223_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ce-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ae6b0225f4bbc989e398c85062f7426f8cf4b61f8aca6f40bf44789d1dada1949-informational)

## [🔗 Portainer Agent (Channel Selector)](apps/portainer-agent/)

Portainer Agent with selectable LTS/STS channel.

![Version](https://img.shields.io/badge/version-v2026.8.3-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-74_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fagent-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A2a0e0fd85636b04b3e816b1c52ede8b3bf44e42420a0bbf2d9962ae8bfe6fea8-informational)

## [🔗 Portainer Agent LTS](apps/portainer-agent-lts/)

Portainer Agent with selectable LTS/STS channel.

![Version](https://img.shields.io/badge/version-v2.45.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-42_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fagent-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A2a0e0fd85636b04b3e816b1c52ede8b3bf44e42420a0bbf2d9962ae8bfe6fea8-informational)

## [🔗 Portainer Agent STS](apps/portainer-agent-sts/)

Portainer Agent with selectable LTS/STS channel.

![Version](https://img.shields.io/badge/version-v2.45.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-42_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fagent-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A2a0e0fd85636b04b3e816b1c52ede8b3bf44e42420a0bbf2d9962ae8bfe6fea8-informational)

## [🐳 Portainer CE LTS](apps/portainer-ce-lts/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2.45.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-68_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ce-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ae6b0225f4bbc989e398c85062f7426f8cf4b61f8aca6f40bf44789d1dada1949-informational)

## [🐳 Portainer CE STS](apps/portainer-ce-sts/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2.45.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-68_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ce-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ae6b0225f4bbc989e398c85062f7426f8cf4b61f8aca6f40bf44789d1dada1949-informational)

## [💼 Portainer EE LTS](apps/portainer-ee-lts/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2.45.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-87_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ee-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A379f8ca470e9d442f4742f33a50449638810c82e572b670354db5dbef32ed090-informational)

## [💼 Portainer EE STS](apps/portainer-ee-sts/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2.45.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-85_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ee-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A379f8ca470e9d442f4742f33a50449638810c82e572b670354db5dbef32ed090-informational)

<!-- APPS-LIST-END -->

## Dashboard

Das automatisch generierte Dashboard mit Badge-Matrix, Health-Score und History ist verfügbar auf:
**[GitHub Pages Dashboard][repodashboard]**

## 💖 Unterstütze die Entwicklung

Wenn dir dieses Apps Zeit spart oder die Einrichtung erleichtert, wäre ich dir für deine Unterstützung sehr dankbar!

[![PayPal][paypal-badge]][paypal-link]

### Gibt auch DEV Repo für Test/Entwicklung

Config/Hostname ist durch URL ID unterschiedlich keine automatisch übernahme von Config dev -> main

[![Repository hinzufügen][repoadd-badge]][repoadddev]

```text
https://github.com/sandmaennchen5/ha-repo#dev
```

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
[paypal-badge]: https://img.shields.io/badge/PayPal-Spenden-blue?logo=paypal
[paypal-link]: https://www.paypal.me/sandmaennchen5
[repoadd-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repo]: https://github.com/sandmaennchen5/ha-repo
[repoadd]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo
[repodev]: https://github.com/sandmaennchen5/ha-repo#dev
[repoadddev]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo%23dev
[repoissues]: https://github.com/sandmaennchen5/ha-repo/issues
[repodashboard]: https://sandmaennchen5.github.io/ha-repo/

[forum]: https://community.home-assistant.io/
