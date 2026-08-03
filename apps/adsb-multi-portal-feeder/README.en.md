# ADS-B Multi-Portal Feeder

[![Builder][builder-badge]][builder-url]
[![Lint][lint-badge]][lint-url]
[![Docker Lint][docker-lint-badge]][docker-lint-url]
[![YAML Lint][yaml-lint-badge]][yaml-lint-url]
[![CodeFactor][codefactor-badge]][codefactor-url]

<!-- BADGES START -->
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
<!-- BADGES-END -->

Docker image for dump1090-fa, fr24feed, FlightAware, adsbexchange, Plane Finder, OpenskyNetwork, adsb.fi, ADSBHub and Radarbox.

## About

Add-on for transferring ADS-B data from an inexpensive USB ADS-B stick (e.g. Nooelec NESDR Mini) to FlightRadar24, FlightAware, ADSBexchange and Plane Finder based on dump1090.

This add-on is based on the Docker image [docker-fr24feed-piaware-dump1090](https://github.com/Thom-x/docker-fr24feed-piaware-dump1090) from Thom-x

[Read the full add-on documentation][docs]

## Overview

- processes ADS-B data from a local RTL-SDR receiver with dump1090-fa
- can send data to, among others, FlightAware, Flightradar24, ADS-B Exchange,
  adsb.fi, Plane Finder, OpenSky, RadarBox and ADSBHub
- Integrated Dump1090 web interface via Home Assistant Ingress
- optional TCP outputs in Raw, BaseStation and Beast formats
- accepts location data from Home Assistant if desired
- supports `aarch64` and `amd64`

## Requirements

- compatible RTL-SDR dongle if no network receiver is used
- Antenna with suitable location and reception for 1090 MHz
- Access data or release keys for the desired feeder portals
- Internet access to the activated portals

## Installation

1. Add this repository under **Settings → Apps → App Store → Repositories**.
2. Install **ADS-B Multi-Portal Feeder** and connect the RTL-SDR dongle.
3. Configure location, activated services and their access data.
4. Save configuration and start the app.
5. Check log for USB, receiver and login errors.
6. Open the web interface and check whether aircraft are being received.

## Basic configuration

| option | Default | Description |
|---|---:|---|
| `SERVICE_ENABLE_DUMP1090` | `true` | Activate local ADS-B receiver |
| `SERVICE_ENABLE_PIAWARE` | `true` | Enable FlightAware feeder |
| `SERVICE_ENABLE_FR24FEED` | `true` | Activate Flightradar24 feeder |
| `SERVICE_ENABLE_HTTP` | `true` | Enable Dump1090 web interface |
| `HTML_SITE_LAT` / `HTML_SITE_LON` | HA location | Position of the receiving station |
| `HTML_SITE_ALT` | HA height | Station height above sea level |
| `DUMP1090_ADDITIONAL_ARGS` | empty | additional dump1090 arguments |

Feeders without valid identifiers or credentials should be disabled. The
Complete options list with portal-specific setup is available in
[DOCS.md](DOCS.md).

## Network and Security

Ingress does not require additional port sharing. The ports `30001` to
`30005` as well as the status ports `8080`, `8754` and `30053` should only then
Host can be assigned when an external recipient or client needs it.
Do not publish raw data and status pages unprotected on the Internet.

## Support

Create an issue on GitHub.

## Acknowledgments

- A big thank you and ❤️ goes to [Thom-x](https://github.com/Thom-x) for his work on [docker-fr24feed-piaware-dump1090](https://github.com/Thom-x/docker-fr24feed-piaware-dump1090)

[docs]: DOCS.md

## Further documentation

- [Full App Documentation](DOCS.md)
- [Version History](CHANGELOG.md)
- [General Storage Locations and Data Migration](../../docs/app-storage-and-migration.md)

## Links

- [Upstream Project](https://github.com/sandmaennchen5/ha-repo)- [Repository Support](https://github.com/sandmaennchen5/ha-repo/issues)

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
[repodev]: https://github.com/sandmaennchen5/ha-repo#dev
[repoadddev]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsandmaennchen5%2Fha-repo%23dev
[repoissues]: https://github.com/sandmaennchen5/ha-repo/issues
[repodashboard]: https://sandmaennchen5.github.io/ha-repo/