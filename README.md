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
![Version](https://img.shields.io/badge/version-v2.9.0.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--07-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Image Size](https://img.shields.io/badge/size-249_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.9.0-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fthomx%2Ffr24feed--piaware-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A9579f70397925b4d84c970dbe243b7dd21e4a30b382fd8713ec54d266a5e2bb2-informational)

## [📊 Checkmk Agent](apps/checkmk-agent/)

Expose the Checkmk monitoring agent on port 6556.

![Version](https://img.shields.io/badge/version-v2.5.0.16.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--14-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Image Size](https://img.shields.io/badge/size-12_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.5.0p16-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2FCheckmk%2Fcheckmk-informational)
![Commit](https://img.shields.io/badge/commit-1ca76bf3af9a9e4141535de19dfe107533b2cea2-informational)

## [🛟 Dockhand](apps/dockhand/)

Modern Docker and Compose management with Home Assistant Ingress.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v1.0.54.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--17-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-188_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.0.54-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2FFinsys%2Fdockhand-informational)
![Commit](https://img.shields.io/badge/commit-9efea8ba2e1e8779441a9b99c101a03f19ca515f-informational)

## [⚓ Drydock](apps/drydock/)

Container update monitoring and automation with Home Assistant Ingress.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v1.6.1.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--02-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-152_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.6.1-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fcodeswhat%2Fdrydock-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A0c522e2a76cd46125478ac48f97ac4baba92b1f906f8dd91f8c9df8258bd1f8d-informational)

## [🏠 Homey Self-Hosted Server](apps/homey-shs/)

Run Homey Self-Hosted Server on Home Assistant OS.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v13.5.2-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--16-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Image Size](https://img.shields.io/badge/size-283_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v13.5.2-yellow)
![Repo](https://img.shields.io/badge/repo-ghcr.io%2Fathombv%2Fhomey--shs-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ad44c6cd18d2c4d97479b51ba344983ba2b697882f6cc0b20183fd1ebe4103d86-informational)

## [🏠 OpenCCU (HA Repo)](apps/openccu/)

HomeMatic/homematicIP CCU central based on OpenCCU

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v3.89.11.20260919-ha1-blue)
![Updated](https://img.shields.io/badge/updated-2026--09--20-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Privileged](https://img.shields.io/badge/privileged-IPC_LOCK%7CSYS_ADMIN%7CSYS_RAWIO%7CSYS_RESOURCE%7CNET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Upstream](https://img.shields.io/badge/upstream-v3.89.11.20260919-yellow)
![Repo](https://img.shields.io/badge/repo-https%3A%2F%2Fgithub.com%2FOpenCCU%2FOpenCCU-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A3cfcb30e1921b36812cf1adc49dbc7aaca21079c1818450a7f18491e891077c8-informational)

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
![Version](https://img.shields.io/badge/version-v3.89.11.20261016-bcc2300-ha1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--16-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Privileged](https://img.shields.io/badge/privileged-IPC_LOCK%7CSYS_ADMIN%7CSYS_RAWIO%7CSYS_RESOURCE%7CNET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Upstream](https://img.shields.io/badge/upstream-v3.89.11.20261016-bcc2300-yellow)
![Repo](https://img.shields.io/badge/repo-https%3A%2F%2Fgithub.com%2FOpenCCU%2FOpenCCU-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A6a0602c96ae395c0e08120879b513c0961c055e8fc47ce9d1ee4d662fe656227-informational)

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

## [🦎 Pangolin - CLI](apps/pangolin-cli/)

Official Pangolin CLI and WireGuard VPN client and Site Connector for Linux.

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

## [🐳 Portainer (Edition Selector)](apps/portainer/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2026.10.2-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--12-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-223_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.2-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ce-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A37aa2620d882794ed3e425b386db750f07500add53aa10adc741218b1e8d5782-informational)

## [🔗 Portainer Agent (Channel Selector)](apps/portainer-agent/)

Portainer Agent with selectable LTS/STS channel.

![Version](https://img.shields.io/badge/version-v2026.10.2-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--12-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-74_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.2-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fagent-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ad4f03ec3ae2a8630394bb41df09788af3228ceb891f15b89ba6205bca07ada19-informational)

## Veraltete Apps (deprecated)

### [🛰️ Pangolin - Newt Tunnel](apps/pangolin-newt/)

Secure remote access with Pangolin tunnels.

![Version](https://img.shields.io/badge/version-v1.18.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--02-green)
![Stage](https://img.shields.io/badge/stage-deprecated-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN%7CSYS_MODULE-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Image Size](https://img.shields.io/badge/size-36_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.18.1-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Fnewt-informational)
![Commit](https://img.shields.io/badge/commit-7856d5f4c12e2afcadad182cca357bbbb6c80dc3-informational)

### [🍃 Pangolin - Olm Client](apps/pangolin-olm/)

Advanced WireGuard client for remote access to Pangolin and Newt sites.

![Version](https://img.shields.io/badge/version-v1.10.1.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--02-green)
![Stage](https://img.shields.io/badge/stage-deprecated-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN%7CSYS_MODULE-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Image Size](https://img.shields.io/badge/size-28_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.10.1-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Folm-informational)
![Commit](https://img.shields.io/badge/commit-4901fde4b1850b56026b9740f34032dab37e7794-informational)

### [🔗 Portainer Agent LTS](apps/portainer-agent-lts/)

Portainer Agent with selectable LTS/STS channel.

![Version](https://img.shields.io/badge/version-v2.45.2.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--08-green)
![Stage](https://img.shields.io/badge/stage-deprecated-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-42_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.2-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fagent-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ad4f03ec3ae2a8630394bb41df09788af3228ceb891f15b89ba6205bca07ada19-informational)

### [🔗 Portainer Agent STS](apps/portainer-agent-sts/)

Portainer Agent with selectable LTS/STS channel.

![Version](https://img.shields.io/badge/version-v2.45.2.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--08-green)
![Stage](https://img.shields.io/badge/stage-deprecated-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-42_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.2-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fagent-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ad4f03ec3ae2a8630394bb41df09788af3228ceb891f15b89ba6205bca07ada19-informational)

### [🐳 Portainer CE LTS](apps/portainer-ce-lts/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2.45.2.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--08-green)
![Stage](https://img.shields.io/badge/stage-deprecated-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-68_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.2-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ce-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A37aa2620d882794ed3e425b386db750f07500add53aa10adc741218b1e8d5782-informational)

### [🐳 Portainer CE STS](apps/portainer-ce-sts/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2.45.2.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--08-green)
![Stage](https://img.shields.io/badge/stage-deprecated-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-68_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.2-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ce-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A37aa2620d882794ed3e425b386db750f07500add53aa10adc741218b1e8d5782-informational)

### [💼 Portainer EE LTS](apps/portainer-ee-lts/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2.45.2.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--08-green)
![Stage](https://img.shields.io/badge/stage-deprecated-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-87_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.2-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ee-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A859c869c9b1b38ef460970f178534c053cc9c5b064099504ba672338a3372bfb-informational)

### [💼 Portainer EE STS](apps/portainer-ee-sts/)

Portainer CE/BE with selectable LTS/STS channel, ingress and data migration.

![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v2.45.2.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--08-green)
![Stage](https://img.shields.io/badge/stage-deprecated-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-85_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.45.2-yellow)
![Repo](https://img.shields.io/badge/repo-docker.io%2Fportainer%2Fportainer--ee-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A859c869c9b1b38ef460970f178534c053cc9c5b064099504ba672338a3372bfb-informational)

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
