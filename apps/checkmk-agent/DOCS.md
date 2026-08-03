# Checkmk Agent

Diese Home-Assistant-App stellt den offiziellen Checkmk-Agenten über TCP-Port `6556` bereit. Sie besitzt keine Weboberfläche und benötigt keine Konfigurationsoptionen.

## Einrichtung

1. App installieren und starten.
2. Sicherstellen, dass Port `6556/tcp` dem Host zugewiesen ist.
3. In Checkmk den Home-Assistant-Host mit der IP-Adresse von Home Assistant aufnehmen.
4. Die Agentenverbindung auf Port `6556` testen und anschließend die Service-Erkennung ausführen.

## Sicherheit

Der klassische Checkmk-Agent liefert seine Daten auf Port 6556 grundsätzlich im Klartext aus. Der Port sollte daher nur in einem vertrauenswürdigen lokalen Netz erreichbar sein. Für Zugriffe über andere Netze sollte der Verkehr durch Firewall, VPN oder eine Checkmk-seitig unterstützte verschlüsselte Verbindung geschützt werden. Port 6556 darf nicht ungeschützt ins Internet weitergeleitet werden.

## Umfang der Daten

Der Agent läuft innerhalb des App-Containers. Er meldet daher primär die im Container sichtbaren Systeminformationen und nicht automatisch sämtliche Dateien oder Prozesse des Home-Assistant-Hosts.

Upstream: <https://github.com/Checkmk/checkmk>

## Versionierung

Home Assistant erkennt Checkmks `p`-Schreibweise nicht zuverlässig. Deshalb wird `X.Y.ZpN` als rein numerische App-Version `X.Y.Z.N.R` veröffentlicht. `R` ist die Revision unserer App. Beispiel: Checkmk `2.5.0p6`, erster App-Build = `2.5.0.6.1`.

## Daten, Backups und Migration

Die App speichert keine eigenständige Anwendungsdatenbank. Zugangsdaten und Optionen liegen in der Home-Assistant-App-Konfiguration und werden im Home-Assistant-Backup berücksichtigt. Ein eigener Import oder Export ist nicht erforderlich.

## Bekannte Probleme und Einschränkungen

Bei Problemen zuerst das App-Protokoll, die Erreichbarkeit des Upstream-Dienstes und die konfigurierten Ports prüfen. Architektur- und Upstream-Einschränkungen gelten entsprechend der verlinkten Herstellerdokumentation.

## Support

- App-Integration: [Issues im Home-Assistant-App-Repository](https://github.com/sandmaennchen5/ha-repo/issues)
- Programmfunktion: [Upstream-Projekt](https://checkmk.com/)
