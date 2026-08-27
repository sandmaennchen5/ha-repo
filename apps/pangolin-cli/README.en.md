# Pangolin CLI client

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES START -->
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

The official Pangolin CLI connects Home Assistant OS as a WireGuard VPN client
with Pangolin Cloud or a self-hosted Pangolin instance. She is the one
Recommended successor to Olm for new client installations.

## Overview

- persistent connection via `pangolin-cli up --attach`
- Access remote Pangolin resources via WireGuard
- Host network access for directly usable routes
- optional Admin and Prometheus endpoint on port `2112`
- local process healthcheck without a TCP port
- supports `aarch64` and `amd64`

## Requirements

- Pangolin Cloud or a self-hosted Pangolin instance
- a machine client created in Pangolin
- Client ID and client secret of this machine client
- disabled protection mode for `/dev/net/tun` and `NET_ADMIN`

## Installation

1. Add this repository in Home Assistant under **Settings → Apps → App Store → Repositories**.
2. Install **Pangolin CLI Client**.
3. Enter `endpoint`, `client_id` and `client_secret`.
4. Deactivate protection mode, save configuration and start the app.
5. Check the log to see whether the login and tunnel setup were successful.

## Configuration

| option | Default | Description |
|---|---:|---|
| `endpoint` | `https://app.pangolin.net` | Pangolin instance URL |
| `client_id` | – | ID of the machine client |
| `client_secret` | – | Secret of the Machine Client |
| `extras.log_level` | `info` | `trace`, `debug`, `info`, `warn` or `error` |
| `extras.additional_args` | empty | additional arguments supported by the installed CLI |

Credentials may not be entered in `additional_args`. Detailed
Notes and error help are available in [DOCS.md](DOCS.md).

## Security

The app manages routes and a WireGuard interface with `NET_ADMIN`
Host network. Enable the optional endpoint on port `2112` only if this
is really needed and limit access to trusted ones
networks.

## Further documentation

- [Full App Documentation](DOCS.md)
- [Version History](CHANGELOG.md)
- [General Storage Locations and Data Migration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream Project](https://github.com/fosrl/cli)
- [Repository Support](https://github.com/sandmaennchen5/ha-repo/issues)

<!-- LEFT -->
[builder-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/hasos-app.yaml?logo=buildkite&label=Builder
[builder url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/hasos-app.yaml
[lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-badge.yaml?logo=lintcode&label=Lint
[lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-badge.yaml
[docker-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-docker.yaml?logo=Docker&label=DockerLint
[docker-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-docker.yaml
[yaml-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-yaml.yaml?logo=yaml&label=YamlLint
[yaml-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-yaml.yaml
[codefactor badge]: https://img.shields.io/codefactor/grade/github/sandmaennchen5/ha-repo?logo=codefactor
[codefactor url]: https://www.codefactor.io/repository/github/sandmaennchen5/ha-repo/branches[paypal badge]: https://img.shields.io/badge/PayPal-Spenden-blue?logo=paypal
[paypal link]: https://www.paypal.me/sandmaennchen5
[repoadd-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repo]: https://github.com/sandmaennchen5/ha-repo
[repoadd]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo
[repodev]: https://github.com/sandmaennchen5/ha-repo#dev
[repoadddev]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo%23dev
[repoissues]: https://github.com/sandmaennchen5/ha-repo/issues
[repodashboard]: https://sandmaennchen5.github.io/ha-repo/
