# Olm – Pangolin Client

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES START -->
![Version](https://img.shields.io/badge/version-v1.8.1.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--30-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN%7CSYS_MODULE-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Image Size](https://img.shields.io/badge/size-26_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.8.1-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Folm-informational)
![Commit](https://img.shields.io/badge/commit-96e1d0f98c4480dd066fbe73dfba5ec0b95d5f7a-informational)
<!-- BADGES-END -->

Olm connects Home Assistant OS via an encrypted WireGuard tunnel
Pangolin and Newt locations. The app is suitable for advanced
Remote access scenarios where Home Assistant accesses remote private networks
should access.

> Olm will be gradually replaced upstream in favor of the **Pangolin CLI**. For
> The app **Pangolin CLI Client** is therefore recommended for new installations.

## Overview

- Connect to Pangolin Cloud or a self-hosted Pangolin instance
- configurable WireGuard interface, MTU and DNS resolution
- Hole punching, relay and local route options
- Internal HTTP health check with Home Assistant Watchdog
- supports `aarch64` and `amd64`

## Requirements

- an Olm client created in Pangolin with ID and secret
- a Pangolin endpoint reachable from the Home Assistant host
- disabled protection mode because `/dev/net/tun`, `NET_ADMIN`, `SYS_MODULE` and
  Host network access is required

## Installation

1. Add this repository in Home Assistant under **Settings → Apps → App Store → Repositories**.
2. Install **Olm – Pangolin Client**.
3. Enter `endpoint`, `id` and `secret` from Pangolin.
4. Deactivate protection mode, save configuration and start the app.
5. Check the log whether tunnels, DNS and routes were set up successfully.

## Important options

| option | Default | Description |
|---|---:|---|
| `endpoint` | `https://app.pangolin.net` | Pangolin instance URL |
| `id` | – | Client ID from Pangolin |
| `secret` | – | client secret key |
| `network.mtu` | `1280` | MTU of the WireGuard interface |
| `network.dns` | `8.8.8.8` | DNS servers in the tunnel |
| `network.interface` | `olm` | Network interface name |
| `extras.log_level` | `INFO` | Log level from `DEBUG` to `FATAL` |

All options and a complete example configuration are available in
[DOCS.md](DOCS.md).

## Security

ID and Secret belong exclusively in the app configuration. The app receives
extensive network rights; therefore only install them on one
trusted Home Assistant system. The healthcheck requires no TCP port.

## Further documentation

- [Full App Documentation](DOCS.md)
- [Version History](CHANGELOG.md)
- [General Storage Locations and Data Migration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream Project](https://github.com/fosrl/olm)
- [Repository Support](https://github.com/sandmaennchen5/ha-repo/issues)

<!-- LEFT -->
[builder-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/hasos-app.yaml?logo=buildkite&label=Builder
[builder url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/hasos-app.yaml
[lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-badge.yaml?logo=lintcode&label=Lint
[lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-badge.yaml
[docker-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-docker.yaml?logo=Docker&label=DockerLint
[docker-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-docker.yaml
[yaml-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-yaml.yaml?logo=yaml&label=YamlLint[yaml-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-yaml.yaml
[codefactor badge]: https://img.shields.io/codefactor/grade/github/sandmaennchen5/ha-repo?logo=codefactor
[codefactor url]: https://www.codefactor.io/repository/github/sandmaennchen5/ha-repo/branches
[paypal badge]: https://img.shields.io/badge/PayPal-Spenden-blue?logo=paypal
[paypal link]: https://www.paypal.me/sandmaennchen5
[repoadd-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repo]: https://github.com/sandmaennchen5/ha-repo
[repoadd]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo
[repodev]: https://github.com/sandmaennchen5/ha-repo#dev
[repoadddev]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo%23dev
[repoissues]: https://github.com/sandmaennchen5/ha-repo/issues
[repodashboard]: https://sandmaennchen5.github.io/ha-repo/
