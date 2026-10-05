# Pangolin CLI client and site

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES START -->
![Version](https://img.shields.io/badge/version-v0.18.1.4-blue)
![Updated](https://img.shields.io/badge/updated-2026--10--05-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Privileged](https://img.shields.io/badge/privileged-NET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Image Size](https://img.shields.io/badge/size-23_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v0.18.1-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2Ffosrl%2Fcli-informational)
![Commit](https://img.shields.io/badge/commit-91aed8f6aef125aa7e20d259c94167cd92d2ebd9-informational)
<!-- BADGES-END -->

The official Pangolin CLI connects Home Assistant OS as a WireGuard VPN client
or site connector to Pangolin Cloud or a self-hosted instance. Client mode
replaces Olm; site mode provides the functionality of Newt.

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
| `mode` | `client` | `client`, `site` or `dual` |
| `site_id` | empty | Site ID (site mode only) |
| `site_secret` | empty | Site secret (site mode only) |
| `site` | local Docker socket | optional site settings, see below |
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

## Site mode (Newt successor)

Set `mode: site` to run `pangolin-cli up site`. Client credentials are not
required in this mode. Existing configurations without `mode` keep running as
machine clients.

```yaml
mode: site
endpoint: https://pangolin.example.com
site_id: YOUR-NEWT-ID
site_secret: YOUR-NEWT-SECRET
site:
  disable_clients: false
  disable_ssh: false
  metrics: true
  metrics_admin_addr: 127.0.0.1:2112
extras:
  log_level: info
  additional_args: ""
```

To migrate from Pangolin Newt, copy its `id` and `secret` into `site_id` and
`site_secret`. Stop the old Newt app before starting this app to avoid connecting
the same site twice. Advanced Newt options are available under `site`.

Alternatively set `site.provisioning_key` and leave both site credentials empty.
Provisioned credentials persist in `/data/pangolin-site.json` by default and are
included in app backups. Use `site.config_file` to load an existing JSON file.
Place custom blueprints, certificates and scripts in `/config` (the app config
directory); all paths refer to the app container.


[All site options](DOCS.en.md#site-mode-newt-successor)

## Dual mode: client and site together

Set `mode: dual` to run the machine client and site connector simultaneously as
two separate s6 services. Each restarts independently when its process exits.
The process healthcheck requires both CLI processes in dual mode.

```yaml
mode: dual
endpoint: https://pangolin.example.com
client_id: YOUR-CLIENT-ID
client_secret: YOUR-CLIENT-SECRET
site_id: YOUR-SITE-ID
site_secret: YOUR-SITE-SECRET
site: {}
extras:
  log_level: info
  additional_args: ""
  client_additional_args: ""
  site_additional_args: ""
```

Each ID/secret pair belongs to its respective machine client or site. Both use
the same `endpoint`. Site provisioning and persisted JSON credentials also work
in dual mode. Entering both IDs does not automatically enable dual mode; select
`mode: dual` explicitly.

Dual defaults: client interface `pangolin-client`, site client tunnel interface
`pangolin-site`, native site main tunnel interface `pangolin-main`. Custom names
via `client.interface_name`, `site.interface`, and `site.interface_main` must be
distinct. The site interface names apply to native interfaces.

`client.http_addr` optionally enables the client HTTP API, e.g. `127.0.0.1:2113`.
If omitted, the client retains its upstream configuration. Site metrics default
to `127.0.0.1:2112`; use different bind addresses/ports if both HTTP servers are
active.

In dual mode `extras.additional_args` applies only to the client. Use
`extras.client_additional_args` and `extras.site_additional_args` for additional
role-specific arguments, also available in single modes. Arguments are separated
by whitespace; shell quoting is not evaluated.

Stop the old Newt app before connecting the same site. Both tunnels share the
host network; destination networks and VPN routes must match your Pangolin setup.

## Local Docker integration

In `site` and `dual`, the CLI can discover local Docker containers.
The socket is exposed through `docker_api: true`; disable protection mode.
It is configured by default for new installations. Existing configurations can
add it if needed:

```yaml
site:
  docker_socket: "unix:///var/run/docker.sock"
```

An external socket proxy can still be used as `site.docker_socket`.
