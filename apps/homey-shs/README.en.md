### Home Assistant Repository – sandmaennchen5
## App - Homey Self-Hosted Server

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES START -->
![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v13.4.0.3-blue)
![Updated](https://img.shields.io/badge/updated-2026--07--28-green)
![Stage](https://img.shields.io/badge/stage-stable-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Host Network](https://img.shields.io/badge/host_network-True-blue)
![Image Size](https://img.shields.io/badge/size-265_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v13.4.0-yellow)
![Repo](https://img.shields.io/badge/repo-ghcr.io%2Fathombv%2Fhomey--shs-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A97b00d6a074f8abc5d14a457f32e1c7a2b0bcbadfd56999932292efbe071abb9-informational)
<!-- BADGES-END -->

Run Homey Self-Hosted Server as a Home Assistant add-on

The app provides Home Assistant Ingress with Socket.IO/WebSocket support,
either `/data`, `/config` or `/share` as data storage as well as one
optional import and export via `/share`. Local Homey logins can
If desired, can be saved separately for each Home Assistant user.

## About

This add-on allows you to run the [Homey Self-Hosted Server](https://homey.app) within your Home Assistant OS installation.
Homey Self-Hosted Server is a software-only product based on the operating system that powers [Homey Pro](https://homey.app/homey-pro/).
It supports devices connecting via Wi-Fi, Ethernet, Cloud and Matter out of the box. Matter-over-Thread also works if you already have a Thread border router in your home. To add Zigbee, Z-Wave, Bluetooth LE, 433MHz or infrared devices, simply connect a [Homey Bridge](https://homey.app/homey-bridge/) to unlock these wireless technologies - no USB sticks required.
[Read the full add-on documentation][docs]

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
8. Install the **Homey** add-on.
10. Start the add-on.

After starting the add-on:

1. Open the Homey app on your iOS or Android device
2. Select **Add New Homey**
3. Select **Self-Hosted Server**
4. Follow the on-screen instructions to complete the setup

## Further documentation

- See [DOCS.md](DOCS.md) for complete add-on documentation and troubleshooting.
- See [CHANGELOG.md](CHANGELOG.md) for the upstream release overview.
- See [Storage Locations and Data Migration](../../docs/app-storage-and-migration.md)
  for backup behavior and manual restore.

## Links

- [Homey Community Forum Documentation][upstream-doc]
- [Newt GitHub Repository][upstream-repo]

<!-- LEFT -->
[builder-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/hasos-app.yaml?logo=buildkite&label=Builder
[builder url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/hasos-app.yaml
[lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-badge.yaml?logo=lintcode&label=Lint
[lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-badge.yaml
[docker-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-docker.yaml?logo=Docker&label=DockerLint
[docker-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-docker.yaml
[yaml-lint-badge]: https://img.shields.io/github/actions/workflow/status/sandmaennchen5/ha-repo/lint-yaml.yaml?logo=yaml&label=YamlLint
[yaml-lint-url]: https://github.com/sandmaennchen5/ha-repo/actions/workflows/lint-yaml.yaml
[codefactor badge]: https://img.shields.io/codefactor/grade/github/sandmaennchen5/ha-repo?logo=codefactor[codefactor url]: https://www.codefactor.io/repository/github/sandmaennchen5/ha-repo/branches
[paypal badge]: https://img.shields.io/badge/PayPal-Spenden-blue?logo=paypal
[paypal link]: https://www.paypal.me/sandmaennchen5
[repoadd-badge]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[repo]: https://github.com/sandmaennchen5/ha-repo
[repoadd]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo
[repodev]: https://github.com/sandmaennchen5/ha-repo#dev
[repoadddev]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo%23dev
[repoissues]: https://github.com/sandmaennchen5/ha-repo/issues
[repodashboard]: https://sandmaennchen5.github.io/ha-repo/

[upstream-doc]: https://community.homey.app
[upstream repo]: https://github.com/fosrl/newt
[docs]: DOCS.md