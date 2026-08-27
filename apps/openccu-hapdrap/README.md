# openccu-hapdrap

<!-- BADGES-START -->
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
<!-- BADGES-END -->

HAP/DRAP-Helfer für eine OpenCCU-Instanz. Kein Ingress und kein Login-Patch.

Original-Updates mit geprüftem, festem Login-Overlay aus dem angegebenen Fork.
Die Helper-App benötigt kein Login-Overlay. Experimentelle ha-repo-Variante.

Installation über dieses HA-Repository. Vor einem Wechsel unbedingt die
[Dokumentation und Migrationshinweise](DOCS.md) lesen.

[Original](https://github.com/OpenCCU/OpenCCU)

The **OpenCCU HAP/DRAP Helper App** is a Home Assistant companion app for [OpenCCU][openccu] installations using **HmIP-HAP** or **HmIPW-DRAP**.

It does **not** replace OpenCCU. Its job is to keep Docker networking and routing in a state where OpenCCU can reliably communicate with HAP/DRAP devices over multicast UDP.

## Why this app exists

HmIP-HAP/HmIPW-DRAP communication depends on multicast and LAN-reachable routing behavior that is often not available by default for the regular OpenCCU app container.

This helper app continuously:

- creates/maintains an OpenCCU macvlan Docker network on your LAN,
- connects the OpenCCU app container to that network with a stable LAN IP,
- enforces required container routes (multicast route + default route),
- re-checks and repairs this setup in regular intervals.

## When you need it

Use this app if:

- you run OpenCCU in Home Assistant as a HA-App, and
- you use or plan to use HmIP-HAP or HmIPW-DRAP hardware.

## Requirements

- Home Assistant system.
- Running OpenCCU as a HA-app container.
- A free, dedicated IPv4 address in your LAN for OpenCCU (`openccu_ip`).
- **Protection mode disabled** for this helper app.
- Elevated permissions enabled (the app uses Docker API and host networking).

## Configuration

| Option | Required | Default | Description |
|---|---|---|---|
| `openccu_ip` | Yes | `""` | Static dedicated LAN IPv4 address for the OpenCCU app macvlan attachment. |
| `openccu_mac` | No | auto-derived | Static MAC address for the OpenCCU app macvlan attachment. If empty, the helper first reuses the OpenCCU container's existing macvlan MAC when available, otherwise it derives one from the parent interface by incrementing the last octet and trying higher values when needed. |
| `check_interval` | No | `15` | Polling interval in seconds (`10..3600`). If left empty, the helper uses `15`. |
| `openccu_slug` | No | `openccu` | Slug of the OpenCCU app if different from default naming. Container auto-detection supports Supervisor naming variants like `addon_*_<slug>` and `app_*_<slug>`. |
| `network_name` | No | `ccu` | Name of the macvlan Docker network to create/manage for OpenCCU. |
| `parent_interface` | No | auto-detected | Parent NIC for macvlan (example: `enp0s18`). |
| `subnet` | No | auto-detected | Subnet used for macvlan network creation. |
| `gateway` | No | auto-detected | Gateway used for macvlan network creation and route setup. |

## Setup

1. Install and start the regular "OpenCCU" app.
2. Install this "OpenCCU HAP/DRAP-Helper" app.
3. Set **OpenCCU IP** to a free, dedicated LAN IPv4 address.
4. Optionally set **OpenCCU MAC** to a fixed MAC address if you want the OpenCCU app to keep the same MAC across host changes.
5. Disable **Protection mode** for this helper app.
6. Enable **Start on boot**.

## Runtime behavior

At each cycle, the app:

1. Searches for the OpenCCU HA-App by slug (supports both `addon_*_<slug>` and `app_*_<slug>` container names).
2. Ensures the macvlan network exists with the expected parent/subnet/gateway.
3. Ensures OpenCCU is connected to that network with the configured IP and MAC address.
4. Ensures routes inside the OpenCCU container:
   - `224.0.0.0/24 dev <macvlan-if> scope link`
   - `default via <gateway>`

If OpenCCU is not currently running, the helper keeps polling and applies networking as soon as OpenCCU appears.

## Important notes

- This app requires elevated permissions because it manages Docker networking and container routes.
- Keep this app running together with the regular OpenCCU app.
- If `openccu_mac` is left empty, the helper first reuses the OpenCCU container's current macvlan MAC when one is already attached. Otherwise it derives the MAC from the parent interface by incrementing the last octet (`+1`, then `+2`, and so on if needed). This keeps the MAC stable across helper restarts while still allowing fallback to higher values when needed. For the most predictable behavior, set `openccu_mac` explicitly.
- If startup fails, verify Protection mode is disabled and the configured IP/gateway/subnet values are valid for your LAN.

## More information

- OpenCCU project: <https://github.com/OpenCCU/OpenCCU>