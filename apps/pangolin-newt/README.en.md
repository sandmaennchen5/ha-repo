### Home Assistant Repository – sandmaennchen5
## App - Newt Client for Pangolin reverse proxy tunnel

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES START -->
![Version](https://img.shields.io/badge/version-v1.15.0.1-blue)
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
<!-- BADGES-END -->

Newt is a Home Assistant add-on for the Pangolin WireGuard tunnel client and TCP/UDP proxy. It securely connects your Home Assistant host to a Pangolin server and provides access to private services via a User-Space WireGuard tunnel.

## Overview

- Add-on for the Pangolin Newt client
- Uses `host_network` for direct host network access
- Requires additional permissions: `NET_ADMIN`, `SYS_MODULE`
- Supported architectures: `aarch64`, `amd64`

## Installation

[![Add repository][repoadd-badge]][repoadd]

1. Open Home Assistant.
2. Go to **Settings → Apps → Install app**.
3. Click on the three dots (** ⋮ →**) in the top right.
4. Select **Repositories**.
5. Add the following repository URL:
```text
https://github.com/sandmaennchen5/ha-repo
```
6. Click **Add**.
7. Update the apps store.
8. Install the add-on **Newt**.
9. Configure the add-on options.
10. Start the add-on.

> Enable Docker Socket access: Disable **protection mode** on the add-on main page.

## Add-on configuration

| option | Type | Description |
|--------|-----|--------------|
| `endpoint` | `str` | URL of the Pangolin server, e.g. E.g. `https://app.pangolin.net` |
| `id` | `str` | Newt ID from Pangolin Dashboard |
| `secret` | `str` | Newt-Secret from the Pangolin Dashboard |
| `extras.log_level` | `str` | `trace`, `debug`, `info`, `warn`, `error` (default: `info`) |

## Where can I find `id` and `secret`?

1. Open the Pangolin dashboard.
2. Select the desired site or create a new one.
3. Copy the generated `id` and `secret` from the site credentials.

## Requirements

- A running Pangolin server or managed Pangolin instance
- A site registered in Pangolin with Newt ID and Secret

## Notes

- The add-on uses `host_network` so that the tunnel can be operated directly over the host network.
- After making changes to the configuration, the add-on must be restarted.

## Further documentation

- See [DOCS.md](DOCS.md) for complete add-on documentation and troubleshooting.
- See [CHANGELOG.md](CHANGELOG.md) for the upstream release overview.

## Links

- [Pangolin Documentation][upstream-doc]
- [Newt GitHub Repository][upstream-repo]

<!-- LEFT -->
[builder-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/hasos-app.yaml?logo=buildkite&label=Builder
[builder url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/hasos-app.yaml
[lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-badge.yaml?logo=lintcode&label=Lint
[lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-badge.yaml
[docker-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-docker.yaml?logo=Docker&label=DockerLint
[docker-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-docker.yaml
[yaml-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-yaml.yaml?logo=yaml&label=YamlLint
[yaml-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-yaml.yaml[codefactor badge]: https://img.shields.io/codefactor/grade/github/sandmaennchen5/ha-repo?logo=codefactor
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

[upstream doc]: https://docs.pangolin.net
[upstream repo]: https://github.com/fosrl/newt