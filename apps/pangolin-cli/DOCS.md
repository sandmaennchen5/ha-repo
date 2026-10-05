# Pangolin CLI Client und Site – Dokumentation

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
| `mode` | nein | `client` | `client`, `site` oder `dual` |
| `site_id` | im Site-Modus | leer | Site-ID; alternativ Provisioning oder JSON |
| `site_secret` | im Site-Modus | leer | Site-Secret; alternativ Provisioning oder JSON |
| `client_id` | im Client-Modus | leer | ID des Machine Clients |
| `client_secret` | im Client-Modus | leer | Secret des Machine Clients |
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

## Site-Modus (Newt-Nachfolger)

Mit `mode: site` startet die App `pangolin-cli up site`. Client-Zugangsdaten
werden in diesem Modus nicht benötigt. Bestehende Konfigurationen ohne `mode`
starten weiterhin als Machine Client.

```yaml
mode: site
endpoint: https://pangolin.example.com
site_id: DEINE-NEWT-ID
site_secret: DEIN-NEWT-SECRET
site:
  disable_clients: false
  disable_ssh: false
  metrics: true
  metrics_admin_addr: 127.0.0.1:2112
extras:
  log_level: info
  additional_args: ""
```

Für die Migration von Pangolin Newt dessen `id` und `secret` als `site_id` und
`site_secret` übernehmen. Die alte Newt-App vor dem Start stoppen, damit dieselbe
Site nicht doppelt verbunden wird. Erweiterte Newt-Optionen stehen unter `site`.

Alternativ `site.provisioning_key` verwenden und beide Site-Zugangsdaten leer
lassen. Die erhaltenen Zugangsdaten werden standardmäßig in
`/data/pangolin-site.json` gespeichert und mit der App gesichert. Ein vorhandenes
JSON kann mit `site.config_file` geladen werden. Eigene Dateien wie Blueprints,
Zertifikate und Skripte können unter `/config` (App-Konfigurationsverzeichnis)
abgelegt werden; Pfade beziehen sich immer auf den App-Container.

Die folgenden Site-Optionen gelten in den Modi `site` und `dual`. Nur gesetzte Werte werden
exportiert; auch `false` wird übergeben. CLI-Argumente haben Vorrang vor ENV,
ENV vor JSON und JSON vor Upstream-Standardwerten. `trace` wird für Sites auf
`DEBUG` abgebildet. `tls_client_ca` und `local_endpoint_interfaces` erwarten
kommagetrennte Werte. Docker-Discovery kann mit
`site.docker_socket: unix:///var/run/docker.sock` den lokalen Docker-Socket
verwenden. Dieser ist über `docker_api: true` eingebunden und bei neuen
Installationen voreingestellt. Dafür muss der Schutzmodus deaktiviert sein.
Bei bestehenden Konfigurationen den Wert bei Bedarf unter `site` ergänzen.
Ein externer Docker-Socket-Proxy bleibt als Alternative nutzbar.
Netzwerkvalidierung funktioniert laut Upstream nicht im Host-Netzwerk.
`otlp_endpoint` legt das OTLP-Ziel fest; mit `otlp: true` wird der Export aktiviert.
Der Prozess-Healthcheck bleibt aktiv; `health_file` ist eine zusätzliche
Verbindungsanzeige und wird vom Docker-Healthcheck nicht ausgewertet.

| Option | ENV / Flag |
|---|---|
| `site.provisioning_key` | `SITE_PROVISIONING_KEY` |
| `site.name` | `SITE_NAME` |
| `site.config_file` | `CONFIG_FILE` |
| `site.dns` | `DNS` |
| `site.ping_interval` | `PING_INTERVAL` |
| `site.ping_timeout` | `PING_TIMEOUT` |
| `site.udp_proxy_idle_timeout` | `SITE_UDP_PROXY_IDLE_TIMEOUT` |
| `site.docker_socket` | `DOCKER_SOCKET` |
| `site.docker_enforce_network_validation` | `DOCKER_ENFORCE_NETWORK_VALIDATION` |
| `site.disable_clients` | `DISABLE_CLIENTS` |
| `site.disable_ssh` | `DISABLE_SSH` |
| `site.health_file` | `HEALTH_FILE` |
| `site.blueprint_file` | `BLUEPRINT_FILE` |
| `site.provisioning_blueprint_file` | `PROVISIONING_BLUEPRINT_FILE` |
| `site.updown` | `UPDOWN_SCRIPT` |
| `site.no_cloud` | `NO_CLOUD` |
| `site.metrics` | `SITE_METRICS_PROMETHEUS_ENABLED` |
| `site.otlp` | `SITE_METRICS_OTLP_ENABLED` |
| `site.otlp_endpoint` | `OTEL_EXPORTER_OTLP_ENDPOINT` |
| `site.metrics_admin_addr` | `SITE_ADMIN_ADDR` |
| `site.metrics_async_bytes` | `SITE_METRICS_ASYNC_BYTES` |
| `site.pprof` | `SITE_PPROF_ENABLED` |
| `site.region` | `SITE_REGION` |
| `site.enforce_hc_cert` | `ENFORCE_HC_CERT` |
| `site.tls_client_cert_file` | `TLS_CLIENT_CERT` |
| `site.tls_client_key` | `TLS_CLIENT_KEY` |
| `site.tls_client_ca` | `TLS_CLIENT_CAS` |
| `site.tls_client_cert` | `TLS_CLIENT_CERT_PKCS12` |
| `site.ad_pre_shared_key` | `AD_KEY` |
| `site.ad_principals_file` | `AD_PRINCIPALS_FILE` |
| `site.ad_ca_cert_path` | `AD_CA_CERT_PATH` |
| `site.ad_generate_random_password` | `AD_GENERATE_RANDOM_PASSWORD` |
| `site.interface` | `INTERFACE` |
| `site.port` | `PORT` |
| `site.mtu` | `MTU` |
| `site.native` | `USE_NATIVE_INTERFACE` |
| `site.native_main` | `USE_NATIVE_MAIN_INTERFACE` |
| `site.interface_main` | `INTERFACE_MAIN` |
| `site.local_endpoint_interfaces` | `LOCAL_ENDPOINT_INTERFACES` |
| `site.prefer_endpoint` | `--prefer-endpoint` |

[Upstream Site configuration](https://docs.pangolin.net/manage/sites/configure-site)

## Dual-Modus: Client und Site gleichzeitig

Mit `mode: dual` laufen Machine Client und Site Connector gleichzeitig als zwei
getrennte s6-Dienste. Beide werden unabhängig neu gestartet, wenn ihr Prozess
endet. Der Prozess-Healthcheck prüft im Dual-Modus beide CLI-Prozesse.

```yaml
mode: dual
endpoint: https://pangolin.example.com
client_id: DEINE-CLIENT-ID
client_secret: DEIN-CLIENT-SECRET
site_id: DEINE-SITE-ID
site_secret: DEIN-SITE-SECRET
site: {}
extras:
  log_level: info
  additional_args: ""
  client_additional_args: ""
  site_additional_args: ""
```

Die IDs und Secrets gehören jeweils zum Machine Client bzw. zur Site. Beide
verwenden denselben `endpoint`. Für die Site funktionieren weiterhin Provisioning
und eine gespeicherte JSON-Konfiguration als Alternative zu ID und Secret.
Beide IDs einzutragen aktiviert Dual nicht automatisch; dafür `mode: dual` wählen.

Standard-Interfaces im Dual-Modus: Client `pangolin-client`, Site-Client-Tunnel
`pangolin-site`, nativer Site-Haupttunnel `pangolin-main`. Eigene Namen über
`client.interface_name`, `site.interface` und `site.interface_main` müssen
unterschiedlich sein. Die beiden Site-Namen betreffen native Interfaces.

`client.http_addr` aktiviert optional die HTTP-API des Clients, zum Beispiel
`127.0.0.1:2113`. Ohne diese Option behält der Client seine Upstream-Konfiguration.
Die Site-Metriken verwenden standardmäßig `127.0.0.1:2112`; wenn beide HTTP-Server
aktiv sind, müssen sie verschiedene Bind-Adressen/Ports verwenden.

`extras.additional_args` gilt im Dual-Modus nur für den Client. Zusätzlich
stehen `extras.client_additional_args` und `extras.site_additional_args` für die
jeweilige Rolle zur Verfügung, auch in den Einzelmodi. Werte werden durch
Leerzeichen getrennt; Shell-Quoting wird nicht ausgewertet.

Die alte Newt-App vor dem Start derselben Site stoppen. Die Tunnel teilen das
Host-Netzwerk; Zielnetze und VPN-Routen müssen zur Pangolin-Konfiguration passen.
