# Portainer Agent

The app runs the official standard Portainer Agent. The selector chooses the LTS or STS channel; the fixed apps contain one channel only. The Agent has no Web UI and stores no application state, so storage selection and import/export are intentionally omitted.

Connect Portainer Server to `<Home-Assistant-IP>:9001` without a protocol prefix. The connection is encrypted by the Agent. A newly started Agent must be claimed promptly by Portainer; otherwise restart the app and connect again.

Set the same `agent_secret` on Server and Agent when using a shared secret. Additional documented Agent variables can be entered under `environment`. The Docker socket is supplied through Home Assistant's Docker API permission.

Documentation: <https://docs.portainer.io/admin/environments/add/docker/agent>

## Versioning and automatic updates

The selector uses calendar versions in the form `YYYY.M.N` and tracks the `alpine` LTS and `alpine-sts` STS tags together. Fixed Agent apps use `<Agent upstream version>.<app revision>`.

## Daten, Backups und Migration

Die App speichert keine eigenständige Anwendungsdatenbank. Zugangsdaten und Optionen liegen in der Home-Assistant-App-Konfiguration und werden im Home-Assistant-Backup berücksichtigt. Ein eigener Import oder Export ist nicht erforderlich.

## Sicherheit

Aktivieren Sie nur benötigte Funktionen und Ports. Zugangsdaten gehören ausschließlich in die App-Konfiguration und nicht in Protokolle oder zusätzliche Befehlsargumente. Die tatsächlich benötigten Berechtigungen stehen in der jeweiligen config.yaml.

## Bekannte Probleme und Einschränkungen

Bei Problemen zuerst das App-Protokoll, die Erreichbarkeit des Upstream-Dienstes und die konfigurierten Ports prüfen. Architektur- und Upstream-Einschränkungen gelten entsprechend der verlinkten Herstellerdokumentation.

## Support

- App-Integration: [Issues im Home-Assistant-App-Repository](https://github.com/sandmaennchen5/ha-repo/issues)
- Programmfunktion: [Upstream-Projekt](https://docs.portainer.io/admin/environments/add/docker/agent)
