# openccu-proxy

<!-- BADGES-START -->
![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v0.7.0-ha1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Upstream](https://img.shields.io/badge/upstream-v0.7.0-yellow)
![Repo](https://img.shields.io/badge/repo-https%3A%2F%2Fgithub.com%2FOpenCCU%2FOpenCCU-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3A4ea40c4b0bfa2cfdbb531d4eb2b721d532bc1964bb497a434f8f4aecc233c733-informational)
<!-- BADGES-END -->

Ingress-Zugang zu einer separat laufenden OpenCCU. Zieladresse unter `webui-url` einstellen.

Original-Updates mit geprüftem, festem Login-Overlay aus dem angegebenen Fork.
Die Helper-App benötigt kein Login-Overlay. Experimentelle ha-repo-Variante.

Installation über dieses HA-Repository. Vor einem Wechsel unbedingt die
[Dokumentation und Migrationshinweise](DOCS.md) lesen.

[Original](https://github.com/OpenCCU/OpenCCU)

## About

⚠️ This App does NOT provide a full OpenCCU system ⚠️

It acts as a web proxy to an external running [OpenCCU](openccu) CCU instance. Thus, the sole purpose of this App is to add a OpenCCU icon to the sidebar of Home Assistant which will open the frontend of an external running OpenCCU instance so that it can be accessed from within HA.

## Documentation / Installation

In addition to installing this HA App you will have to set some mandatory App options to link against an external OpenCCU WebUI:

- `webui-url` (required): the URL on which the external OpenCCU WebUI is accessible, e.g. `http://192.168.2.43`.

In addition, you have to make sure that your HA system is able to directly access the OpenCCU CCU WebUI. Thus, if you have the internal firewall system of your OpenCCU system enabled, make sure to add the ip adress of your HA system to these firewall settings.

## License

This Home Assistant App as well as OpenCCU is licensed under the Apache-2.0 open-source license.