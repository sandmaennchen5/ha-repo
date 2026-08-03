# Checkmk Agent for Home Assistant

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES START -->
![Version](https://img.shields.io/badge/version-v2.5.0.10.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--28-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Image Size](https://img.shields.io/badge/size-11_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v2.5.0p10-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2FCheckmk%2Fcheckmk-informational)
![Commit](https://img.shields.io/badge/commit-a197bee7557196aa3e94ec523c570f3ff5039884-informational)
<!-- BADGES-END -->

Sets the official Checkmk agent as a home assistant app on the TCP port
`6556` ready. A Checkmk site can query the agent and the within
Evaluate system information visible in the app container.

- Architectures: `amd64`, `aarch64`
- No WebUI
- No app options required
- TCP watchdog and container health check
- Automatic upstream update; Checkmk `X.Y.ZpN` is published as app version `X.Y.Z.N.R`

## Requirements

- an accessible Checkmk site
- Network access from the Checkmk site to the IP of the Home Assistant host
- a firewall rule for TCP port `6556` exclusively from the monitoring network

Further information can be found in [DOCS.md](DOCS.md).

## Installation

1. Add this repository in Home Assistant under **Settings → Apps → App Store → Repositories**.
2. Install and start **Checkmk Agent**.
3. Check whether `6556/tcp` is published on port `6556` of the host.
4. Add the Home Assistant host in Checkmk with its IP address.
5. Test agent connection and then run service discovery.

## Security and scope

The classic agent delivers its output unencrypted. Port `6556` is allowed
not be redirected to the Internet; use firewall, VPN or one
Encrypted connection supported by Checkmk. Since the agent is in one
Container is running, it does not automatically see all processes and files of the
Home Assistant Hosts.

Details about connection testing, versioning and restrictions are available in
[DOCS.md](DOCS.md).

## Further documentation

- [Full App Documentation](DOCS.md)
- [Version History](CHANGELOG.md)
- [General Storage Locations and Data Migration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream Project](https://checkmk.com/)
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
[codefactor url]: https://www.codefactor.io/repository/github/sandmaennchen5/ha-repo/branches
[paypal badge]: https://img.shields.io/badge/PayPal-Spenden-blue?logo=paypal
[paypal link]: https://www.paypal.me/sandmaennchen5
[repoadd-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repo]: https://github.com/sandmaennchen5/ha-repo
[repoadd]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo
[repodev]: https://github.com/sandmaennchen5/ha-repo#dev[repoadddev]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo%23dev
[repoissues]: https://github.com/sandmaennchen5/ha-repo/issues
[repodashboard]: https://sandmaennchen5.github.io/ha-repo/