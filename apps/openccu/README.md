# openccu

<!-- BADGES-START -->
![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v3.89.8.20260719-ha1-blue)
![Updated](https://img.shields.io/badge/updated-2026--08--27-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Privileged](https://img.shields.io/badge/privileged-IPC_LOCK%7CSYS_ADMIN%7CSYS_RAWIO%7CSYS_RESOURCE%7CNET_ADMIN-red)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Kernel Modules](https://img.shields.io/badge/kernel_modules-True-blue)
![Upstream](https://img.shields.io/badge/upstream-v3.89.8.20260719-yellow)
![Repo](https://img.shields.io/badge/repo-https%3A%2F%2Fgithub.com%2FOpenCCU%2FOpenCCU-informational)
![Commit](https://img.shields.io/badge/commit-sha256%3Ab2de2ff6e8e0f3d323714aecf20fb4c634f6aa114fd3e8404bae24f8e84db9b4-informational)
<!-- BADGES-END -->

Vollständige OpenCCU-Stable-Instanz mit lokalem Funkzugriff.

Original-Updates mit geprüftem, festem Login-Overlay aus dem angegebenen Fork.
Die Helper-App benötigt kein Login-Overlay. Experimentelle ha-repo-Variante.

Installation über dieses HA-Repository. Vor einem Wechsel unbedingt die
[Dokumentation und Migrationshinweise](DOCS.md) lesen.

[Original](https://github.com/OpenCCU/OpenCCU)

## About

This App allows to run a [HomeMatic/homematicIP][homematic] control center (CCU) on
your Home Assistant. It is based on [OpenCCU][openccu] which
is open-source and 100% compatible with the homematic vendor ([eQ3][eq3]) own CCU
system (CCU3) to connect to HomeMatic/homematicIP devices without any cloud connection.
Furthermore, it is based on [OCCU][occu] while providing additional exclusive features in
the WebUI and underlying operating system for an improved user experience.

## Features

- Use your Home Assistant central as a full-fledged HomeMatic/homematicIP control center unit (CCU).
- Access the CCU WebUI directly from your Home Assistant user interface.
- Provides all features of a OpenCCU system within your Home Assistant environment.
- Interconnect to HomeMatic/homematicIP devices using the standard, vendor-provided RF modules (`RPI-RF-MOD`, `HM-MOD-RPI-PCB`, `HmIP-RFUSB`, `HM-CFG-USB-2`, `HM-CFG-LAN`), Wired gateways (`HmIPW-DRAP`, `HMW-LGW-O-DR-GS-EU`) or LAN gateway solutions (`HmIP-HAP`, `HM-LGW-O-TW-W-EU`) – see [Requirements](https://github.com/OpenCCU/OpenCCU/wiki/Einleitung#vorraussetzungen).
- Supports additional third-party open-hardware based USB/Ethernet adapter devices (`HB-RF-USB`, `HB-RF-USB-2`, `HB-RF-ETH`).

## Documentation / Installation

For a detailed documentation please refer to the "Documentation" tab of the installed App or
consult the [online documentation](https://github.com/OpenCCU/OpenCCU/wiki/Installation-HomeAssistant) available in the OpenCCU GitHub project. Also note, that after having installed the App you also have to setup the [HomeMatic integration](https://github.com/OpenCCU/OpenCCU/wiki/HomeAssistant-Integration) part in Home Assistant itself so that your Home Assistant is able to see and use the HomeMatic/homematicIP devices of your OpenCCU.

:warning: Please note, that if you are going to use a `RPI-RF-MOD` or `HM-MOD-RPI-PCB` RF module connected to the GPIO of a Raspberry Pi or other SBC you have to make sure to explicitly [enable the UART interface](https://github.com/OpenCCU/OpenCCU/wiki/Installation-HomeAssistant#using-homeassistant-os) of these systems.

## License

This Home Assistant App as well as the OpenCCU base system is licensed under the Apache-2.0 open-source license.
