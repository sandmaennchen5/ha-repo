# Pangolin CLI Client – Dokumentation

Die App führt die offizielle Pangolin CLI auf Home Assistant OS aus. Nach der
Anmeldung baut sie einen WireGuard-Tunnel auf und hält ihn im Vordergrund
aktiv. Dadurch können Dienste im Home-Assistant-Netz und – abhängig von der
Pangolin-Konfiguration – entfernte private Ressourcen sicher erreicht werden.

## Voraussetzungen

- Pangolin Cloud oder eine erreichbare selbst gehostete Pangolin-Instanz
- ein im Pangolin-Dashboard angelegter **Machine Client**
- dessen Client-ID und Client-Secret
- Home Assistant OS oder Home Assistant Supervised mit Unterstützung für Apps

## Machine Client in Pangolin anlegen

1. Pangolin-Dashboard öffnen und den Bereich für Clients aufrufen.
2. Einen neuen Machine Client erstellen.
3. Endpunkt, Client-ID und Client-Secret kopieren.
4. Die Werte direkt in die App-Konfiguration eintragen und das Secret nicht in
   Notizen, Protokollen oder zusätzlichen Argumenten ablegen.

## Einrichtung

1. Erstellen Sie in Pangolin einen Machine Client.
2. Kopieren Sie Endpunkt, Client-ID und Client-Secret in die App-Konfiguration.
3. Starten Sie die App und kontrollieren Sie das Protokoll.

Die App startet dauerhaft `pangolin-cli up --attach`. Sie verwendet Host-Netzwerk, `/dev/net/tun` und `NET_ADMIN`, damit der Client das WireGuard-Interface und die Routen verwalten kann.

`Zusätzliche Argumente` ist ausschließlich für von der installierten CLI-Version unterstützte Optionen gedacht. Zugangsdaten sollten dort nicht wiederholt werden.

Upstream-Dokumentation: https://docs.pangolin.net/manage/clients/install-client#pangolin-cli-linux

## Konfigurationsoptionen

| Option | Pflicht | Standard | Beschreibung |
|---|:---:|---|---|
| `endpoint` | ja | `https://app.pangolin.net` | HTTPS-URL der Pangolin-Instanz |
| `client_id` | ja | leer | ID des Machine Clients |
| `client_secret` | ja | leer | Secret des Machine Clients |
| `extras.log_level` | nein | `info` | `trace`, `debug`, `info`, `warn` oder `error` |
| `extras.additional_args` | nein | leer | weitere Argumente für `pangolin-cli up` |

### Beispiel

```yaml
endpoint: "https://pangolin.example.com"
client_id: "pc_0123456789"
client_secret: "MEIN-GEHEIMES-SECRET"
extras:
  log_level: "info"
  additional_args: ""
```

Änderungen werden erst nach einem Neustart der App wirksam. Verwenden Sie
`additional_args` nur für Optionen, die von der jeweils installierten
CLI-Version dokumentiert sind. Fehlerhafte Argumente verhindern den Start.

## Netzwerk und Ports

Die App verwendet das Host-Netzwerk. `/dev/net/tun` und `NET_ADMIN` erlauben
das Erstellen der WireGuard-Schnittstelle und das Setzen von Routen.

| Port | Zweck | Veröffentlichung nötig? |
|---:|---|---|
| `2112/tcp` | optionaler Admin-/Prometheus-Endpunkt der CLI | normalerweise nein |

Eine Portzuordnung ist nur nötig, wenn der Admin- oder Metrikendpunkt bewusst
aus dem lokalen Netz abgefragt werden soll.

## Funktionsprüfung

Nach dem Start sollte das Protokoll eine erfolgreiche Anmeldung und den Aufbau
des Tunnels melden. Prüfen Sie danach eine in Pangolin freigegebene Ressource.
Der Docker-Healthcheck prüft den CLI-Prozess direkt, ohne TCP-Port.
Er bestätigt nicht die Erreichbarkeit jeder einzelnen Ressource.

## Daten, Backups und Migration

Die App speichert keine eigenständige Anwendungsdatenbank. Zugangsdaten und Optionen liegen in der Home-Assistant-App-Konfiguration und werden im Home-Assistant-Backup berücksichtigt. Ein eigener Import oder Export ist nicht erforderlich.

## Sicherheit

Aktivieren Sie nur benötigte Funktionen und Ports. Zugangsdaten gehören ausschließlich in die App-Konfiguration und nicht in Protokolle oder zusätzliche Befehlsargumente. Die tatsächlich benötigten Berechtigungen stehen in der jeweiligen config.yaml.

## Bekannte Probleme und Einschränkungen

- **Anmeldung schlägt fehl:** Endpunkt ohne zusätzlichen Pfad sowie Client-ID
  und Secret desselben Machine Clients prüfen.
- **Tunnel startet nicht:** Schutzmodus deaktivieren und prüfen, ob
  `/dev/net/tun` auf dem Host verfügbar ist.
- **Ressource nicht erreichbar:** Freigaben, Zieladresse und Routen im
  Pangolin-Dashboard prüfen; außerdem auf Überschneidungen lokaler Netze achten.
- **DNS-Auflösung fehlerhaft:** zunächst IP-Zugriff testen und anschließend die
  DNS-Konfiguration von Pangolin und des Zielnetzes kontrollieren.
- Für eine detaillierte Analyse `extras.log_level` vorübergehend auf `debug`
  oder `trace` setzen und danach wieder reduzieren.

## Support

- App-Integration: [Issues im Home-Assistant-App-Repository](https://github.com/sandmaennchen5/ha-repo/issues)
- Programmfunktion: [Upstream-Projekt](https://github.com/fosrl/cli)
