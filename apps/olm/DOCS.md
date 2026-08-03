### Home Assistant Repository – sandmaennchen5
## Dokumentation - OLM Client für Pangolin-Reverse-Proxy-Tunnel

Das [Fossorial-System – mit Pangolin](https://docs.fossorial.io/) als Kernkomponente – ist ein selbst gehosteter, getunnelter Reverse-Proxy mit Identitäts- und Zugriffsmanagement, der entwickelt wurde, um private Ressourcen sicher über verschlüsselte WireGuard-Tunnel im Userspace bereitzustellen. Stellen Sie sich das wie selbst gehostete Cloudflare-Tunnel vor.

Newt ist der Hauptclient, der eine Verbindung zu Pangolin herstellt und den Zugriff auf Dienste im selben Netzwerk wie Newt ermöglicht. Installieren Sie dies und verbinden Sie sich mit Ihrer Pangolin-Instanz, um den Fernzugriff auf Home Assistant über sichere WireGuard-Tunnel zu ermöglichen

## Home Assitant als Resource..

1. Rufen Sie Ihr Pangolin-Dashboard auf und fügen Sie eine neue Ressource namens `Home Assistant` hinzu. Wählen Sie die richtige Site aus, die sich auf die Home Assistant Newt-Instanz bezieht, die Sie in den Voraussetzungen definiert haben, und geben Sie Ihrer Ressource eine Subdomain.
2. Stelle sicher, dass die Option „SSL aktivieren“ aktiviert ist, damit du ein automatisch generiertes SSL-Zertifikat zur Verschlüsselung der Browserverbindungen erhältst.
3. Fügen Sie im Bereich „Zielkonfiguration“ ein Ziel mit der Methode `HTTP`, der Domain `homeassistant.local.hass.io` und dem Port `8123` hinzu. Klicken Sie auf „Ziel hinzufügen“ und speichern Sie die Einstellungen.
5. Besuche die [Home Assistant-Dokumentation](https://www.home-assistant.io/integrations/http) und befolge die Anweisungen, um einen `trusted_proxy` zu deiner `configuration.yaml`-Datei hinzuzufügen. Dieser lautet wahrscheinlich `172.30.33.0/24`. Stellen Sie sicher, dass Sie auch `use_x_forwarded_for: true` setzen, damit die IP-Adresse des Clients in Ihren Protokollen erscheint und nicht die IP-Adresse des Reverse-Proxys. Starten Sie Home Assistant neu.
7. (Optional) Wenn Sie eine Ressource wünschen, die auf ein Home Assistant-Add-on verweist, verwenden Sie im Abschnitt „domain“ oder im Bereich „Target configuration“ den Slug des Add-ons. Sie finden diesen auf der Add-on-Konfigurationsseite in Home Assistant. In diesem Beispiel lautet der Slug „a0d7b954_tailscale“. Wenn ein `_` vorhanden ist, wie in diesem Beispiel, muss es durch ein `-` ersetzt werden. Die korrekte Domain für dieses Beispiel wäre also `a0d7b954-tailscale`. Ihr Port hängt vom Add-on ab; Sie müssen die Dokumentation oder Konfiguration des Add-ons zu Rate ziehen.

## Einrichtung

1. Legen Sie in Pangolin einen Olm-Client an.
2. Tragen Sie Pangolin-Endpunkt, Olm-ID und Secret in der App-Konfiguration ein.
3. Starten Sie die App und kontrollieren Sie das Protokoll.

Die App verwendet Host-Netzwerk, `/dev/net/tun`, `NET_ADMIN` und `SYS_MODULE`, damit Olm das WireGuard-Interface und die benötigten Routen verwalten kann.

Olm wird von fosrl nur noch für fortgeschrittene Szenarien empfohlen. Für neue Installationen ist die Pangolin CLI die bevorzugte Variante.

Upstream-Dokumentation: https://docs.pangolin.net/manage/clients/understanding-clients

## Konfiguration

| Option | Pflicht | Standard | Beschreibung |
|---|:---:|---|---|
| `endpoint` | ja | `https://app.pangolin.net` | URL der Pangolin-Instanz |
| `id` | ja | leer | Olm-Client-ID aus Pangolin |
| `secret` | ja | leer | geheimer Clientschlüssel |
| `network.mtu` | nein | `1280` | MTU der WireGuard-Schnittstelle |
| `network.dns` | nein | `8.8.8.8` | DNS-Server für den Tunnel |
| `network.upstream_dns` | nein | `8.8.8.8:53` | übergeordneter DNS-Server mit Port |
| `network.interface` | nein | `olm` | Name der WireGuard-Schnittstelle |
| `extras.log_level` | nein | `INFO` | `DEBUG`, `INFO`, `WARN`, `ERROR` oder `FATAL` |
| `extras.disable_holepunch` | nein | `false` | direkte Peer-Verbindung deaktivieren |
| `extras.disable_relay` | nein | `false` | Relay-Verbindung deaktivieren |
| `extras.prefer_local_routes` | nein | `false` | vorhandene lokale Routen bevorzugen |
| `extras.override_dns` | nein | `true` | DNS-Einstellungen durch Olm verwalten lassen |
| `extras.tunnel_dns` | nein | `false` | DNS-Anfragen durch den Tunnel leiten |

### Beispielkonfiguration

```yaml
endpoint: "https://pangolin.example.com"
id: "olm-client-id"
secret: "MEIN-GEHEIMES-SECRET"
network:
  mtu: 1280
  dns: "8.8.8.8"
  upstream_dns: "8.8.8.8:53"
  interface: "olm"
extras:
  log_level: "INFO"
  disable_holepunch: false
  disable_relay: false
  prefer_local_routes: false
  override_dns: true
  tunnel_dns: false
```

Nach Änderungen muss die App neu gestartet werden. Ändern Sie MTU, DNS und
Routing nur bei einem konkreten Netzwerkproblem und jeweils einzeln, damit die
Auswirkung nachvollziehbar bleibt.

## Netzwerk und Healthcheck

Die App arbeitet im Host-Netzwerk und kann daher Routen des
Home-Assistant-Hosts beeinflussen. Der optionale Port `8096/tcp` dient nur dem
internen HTTP-Healthcheck. Er muss für den normalen Betrieb nicht am Host
veröffentlicht werden. Der Watchdog erkennt einen ausgefallenen App-Prozess,
prüft aber nicht jede entfernte Pangolin-Ressource.

Hole-Punching ermöglicht nach Möglichkeit eine direkte Verbindung. Ein Relay
dient als Rückfallweg, wenn direkte Verbindungen durch NAT oder Firewall nicht
möglich sind. Werden beide Funktionen deaktiviert, kann der Tunnel abhängig
vom Netzwerk vollständig ausfallen.

## Voraussetzungen

- Ein laufender [Pangolin](https://github.com/fosrl/pangolin)-Server
- Host-Netzwerkzugriff und WireGuard-Berechtigungen auf dem Home Assistant Host

## Daten, Backups und Migration

Die App speichert keine eigenständige Anwendungsdatenbank. Zugangsdaten und Optionen liegen in der Home-Assistant-App-Konfiguration und werden im Home-Assistant-Backup berücksichtigt. Ein eigener Import oder Export ist nicht erforderlich.

## Sicherheit

Aktivieren Sie nur benötigte Funktionen und Ports. Zugangsdaten gehören ausschließlich in die App-Konfiguration und nicht in Protokolle oder zusätzliche Befehlsargumente. Die tatsächlich benötigten Berechtigungen stehen in der jeweiligen config.yaml.

## Bekannte Probleme und Einschränkungen

- **Authentifizierung fehlerhaft:** `endpoint`, `id` und `secret` prüfen; ID und
  Secret müssen zum selben Olm-Client gehören.
- **Kein WireGuard-Interface:** Schutzmodus deaktivieren und `/dev/net/tun`
  sowie die benötigten Berechtigungen prüfen.
- **Verbindung instabil:** zuerst Erreichbarkeit des Endpunkts prüfen, danach
  testweise MTU reduzieren.
- **DNS-Probleme:** Verhalten mit `override_dns` und `tunnel_dns` einzeln testen
  und `upstream_dns` einschließlich Port kontrollieren.
- **Routenkonflikt:** überlappende lokale und entfernte Subnetze vermeiden;
  `prefer_local_routes` nur bewusst aktivieren.
- Für die Diagnose `extras.log_level: DEBUG` verwenden und anschließend wieder
  auf `INFO` zurückstellen.

## Weitere Informationen

- [Pangolin-Konfiguration](https://docs.pangolin.net)
- [Newt GitHub Repository](https://github.com/fosrl/olm)
