# Dockhand

Diese Home-Assistant-App startet das offizielle Dockhand-Image. Dockhand bietet
Container-, Image-, Netzwerk-, Volume- und Compose-Stack-Verwaltung, Live-Logs,
Terminalzugriff, Git-Deployments und mehrere Docker-Umgebungen.

## Erster Start

Öffne **Weboberfläche öffnen** und lege den ersten Benutzer an. Die lokale Docker
Engine ist über `/var/run/docker.sock` erreichbar. Wähle beim Anlegen der lokalen
Umgebung den Verbindungstyp **Unix Socket**. Dockhand speichert Datenbank, Stacks
und Git-Repositories dauerhaft unter `/data`.

Port `3000/tcp` ist standardmäßig nicht veröffentlicht. Weise ihn nur zu, wenn du
Dockhand außerhalb von Home Assistant Ingress erreichen möchtest.

Dockhand benötigt für lokale Verwaltung weitreichenden Docker-Socket-Zugriff.
Deaktiviere den Schutzmodus der App, falls Home Assistant dies für `docker_api`
verlangt. Der Betrieb als kommerzieller gehosteter Dienst ist gemäß Upstream-Lizenz
nicht gestattet.

Dokumentation: <https://dockhand.pro/manual/>

