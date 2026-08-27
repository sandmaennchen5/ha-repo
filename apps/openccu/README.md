# openccu

<!-- BADGES-START -->
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
