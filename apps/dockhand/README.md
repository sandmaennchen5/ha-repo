# Dockhand Home Assistant App

<!-- BADGES-START -->
![Ingress](https://img.shields.io/badge/ingress-True-blue)
![Version](https://img.shields.io/badge/version-v1.0.47.1-blue)
![Updated](https://img.shields.io/badge/updated-2026--09--12-green)
![Stage](https://img.shields.io/badge/stage-experimental-orange)
![Arch](https://img.shields.io/badge/arch-aarch64%2C%20amd64-green)
![Docker API](https://img.shields.io/badge/docker_api-True-blue)
![Image Size](https://img.shields.io/badge/size-182_MB-informational)
![Upstream](https://img.shields.io/badge/upstream-v1.0.47-yellow)
![Repo](https://img.shields.io/badge/repo-github.com%2FFinsys%2Fdockhand-informational)
![Commit](https://img.shields.io/badge/commit-2a9299f932271fb6c0e2bccb0e64b096da463731-informational)
<!-- BADGES-END -->

Dockhand als Home-Assistant-App mit Ingress, persistentem Speicher und lokaler
Docker-/Compose-Verwaltung. Der Funktionsumfang umfasst Container, Images, Stacks,
Volumes, Netzwerke, Logs, Terminal, Git-Deployments und mehrere Umgebungen.

Speicherwahl: `/data`, `/config` oder eigener `/share`-Unterordner.
Optional merkt sich `remember_ingress_users` die Anmeldung getrennt je
HA-Benutzer bis zum Dockhand-Sitzungsablauf; Passwörter werden nicht gespeichert.

## Installation

Füge `https://github.com/sandmaennchen5/ha-repo` als App-Repository hinzu,
installiere **Dockhand** und öffne anschließend die Weboberfläche.

Weitere Hinweise stehen in [DOCS.md](DOCS.md).

- [Dockhand-Dokumentation](https://dockhand.pro/manual/)
- [Upstream-Repository](https://github.com/Finsys/dockhand)

