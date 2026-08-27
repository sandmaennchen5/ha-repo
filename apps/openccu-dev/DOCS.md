# openccu-dev

Vollständige OpenCCU-Snapshot-Instanz mit lokalem Funkzugriff.

## Original und Updates

Grundlage sind die offiziellen OpenCCU-Images. Diese Variante wird von ha-repo
gebaut, ist keine offizielle OpenCCU-Veröffentlichung und wird zunächst als
experimentell angeboten. Originalversion und Image-Digest stehen in
`upstream.lock.json`. Ein eigener täglicher Workflow übernimmt Original-Updates
mit festem Patch-Stand; Konflikte und fehlgeschlagene Builds stoppen die Freigabe.

Snapshot enthält Entwicklungsversionen. Nicht ohne Tests für eine produktive Zentrale einsetzen.
## Ingress-Anmeldung

- `remember_ingress_users`: Sitzung je HA-Benutzer merken, Standard **aus**.
- `remember_ingress_credentials`: Zugangsdaten verschlüsselt speichern und bei
  Bedarf erneut anmelden, Standard **aus**; benötigt die erste Option.
- `ingress_keepalive_interval`: Erneuerungsintervall in Sekunden, Standard 250.

Sitzungen werden dadurch aktiv am Leben gehalten. Wer Zugriff auf das HA-Konto
hat, kann auch die zugehörige OpenCCU-Sitzung nutzen. Ein WebUI-Logout entfernt
den gespeicherten Datensatz des Benutzers. Das Abschalten der Optionen löscht
vorhandene Dateien nicht automatisch.

Speicher: `/usr/local/etc/config/ha-ingress-sessions`.
Zugangsdaten sind mit AES-256-GCM verschlüsselt, der Schlüssel liegt im selben
Ordner. Backups mit Schlüssel und Datensätzen ermöglichen die Entschlüsselung:
Backups schützen und nicht weitergeben. Die normale WebUI-Anmeldung bleibt erhalten.

## Wechsel von einer bestehenden Installation

Diese App aus einem anderen Repository hat eine eigene HA-Identität und eigene
Daten. **Keine automatische Datenübernahme.** Vorher ein OpenCCU-WebUI-Backup
und ein HA-Backup erstellen. Bei Stable/Snapshot die bisherige Zentrale stoppen,
bevor die neue Instanz dasselbe Funkmodul benutzt. Niemals zwei Zentralen parallel
auf dasselbe Modul zugreifen lassen. Backup in der neuen Instanz wiederherstellen
und Homematic-Integration, Hostname sowie IP/Ports kontrollieren.

Bei Proxy die Zieladresse neu konfigurieren. Beim HAP/DRAP-Helper `openccu_slug`
auf die neue vollständige HA-App-ID prüfen; die alte ID wird nicht automatisch
übernommen. Rückfall: neue Zentrale stoppen, alte Installation mit gesicherten
Daten wieder starten. Bestehende Apps oder Daten werden durch dieses Repository
nicht gelöscht oder verschoben.

## Grenzen

Die Original-Hardwareberechtigungen und Portfreigaben werden übernommen; keine
zusätzlichen Ports werden automatisch veröffentlicht. Hardware-, Supervisor- und
vollständige Login-Tests sind vor produktiver Nutzung erforderlich.

[OpenCCU](https://github.com/OpenCCU/OpenCCU) ·
[Login-Patch](https://github.com/sandmaennchen5/fork_OpenCCU/tree/ingress-loginsave)
