### Home Assistant Repository – sandmaennchen5
## Dokumentation - Homey Self-Hosted Server

Diese App führt den offiziellen Homey Self-Hosted Server von
`ghcr.io/athombv/homey-shs:latest` auf Home Assistant OS aus.

![Screenshot des Homey Self-Hosted Servers](https://raw.githubusercontent.com/sandmaennchen5/ha-repo/master/apps/homey-shs/Homey%20Self-Hosted%20Server.png)

## Konfiguration

**Hinweis**: _Denken Sie daran, das Add-on neu zu starten, wenn die Konfiguration geändert wird._

Derzeit erfordert dieses Add-on keine zusätzliche Konfiguration. Das Add-on verwendet standardmäßig den Host-Netzwerkmodus, was bedeutet, dass der Homey Self-Hosted Server in Ihrem lokalen Netzwerk erreichbar ist. Der Server sollte automatisch von der Homey-App erkannt werden.

Das Add-on speichert seine Daten automatisch im Verzeichnis `/data`.

## Netzwerk

Die App verwendet das Host-Netzwerk und belegt diese TCP-Ports:

- `4859`: HTTP und Socket.IO
- `4860`: HTTPS
- `4861`: Homey Bridge v1
- `4862`: Homey Bridge v2

Stelle sicher, dass die Ports auf dem Home-Assistant-Host nicht bereits von
anderen Diensten verwendet werden.

## Technische Details

- **Docker-Image**: `ghcr.io/athombv/homey-shs:latest`
- **Netzwerkmodus**: Host-Netzwerk (erforderlich für die Geräteerkennung)
- **Privilegierter Modus**: Aktiviert (Homey Self-Hosted Server erwartet, im privilegierten Modus ausgeführt zu werden)
- **Datenverzeichnis**: `/data` (wird automatisch gespeichert)
- **Web-UI**: Erreichbar unter `http://[HOST]:4859`, wenn das Add-on läuft
- **Ingress**: Nicht unterstützt (inkompatibel mit dem für die Geräteerkennung erforderlichen Host-Netzwerk)

## Daten und Backups

Homey speichert seine Daten unter `/homey/user`. In dieser App zeigt der Pfad
auf das persistente `/data`-Verzeichnis der App. Dadurch bleiben Einstellungen,
Geräte und Flows bei App-Updates erhalten und werden in Home-Assistant-Backups
der App aufgenommen.

Beim Start richtet ein Entrypoint-Wrapper die Verknüpfung ein und verschiebt
bei Bedarf Daten aus älteren Installationen nach `/data`. RRD-Daten werden
unter `/data/rrd` gespeichert.

Führe niemals zwei Homey-SHS-Instanzen gleichzeitig mit demselben Datenbestand
aus.

## Lizenzierung

Jede neue Installation von Homey Self-Hosted Server beinhaltet eine 30-tägige kostenlose Testversion, für die keine Zahlungsdaten erforderlich sind.

Nach Ablauf der Testphase können Sie Homey Self-Hosted Server weiterhin nutzen, indem Sie ein monatliches Abonnement abschließen oder eine lebenslange Lizenz erwerben – damit unterstützen Sie die weitere Entwicklung von Homey.

Selbst gehostete Server und Lizenzen können auf der Seite [Meine selbst gehosteten Server](https://homey.app/account/self-hosted-servers/) auf der Homey-Website verwaltet werden.

## Monatliches Abonnement

Sobald Sie Ihren Homey Self-Hosted Server eingerichtet haben, können Sie auf der Seite [Meine Self-Hosted Server](https://homey.app/account/self-hosted-servers/) ein monatliches Abonnement abschließen.

**Wichtig**: Wenn Ihr monatliches Abonnement abläuft, wird Ihr Homey Self-Hosted Server automatisch offline geschaltet, bis Sie das Abonnement verlängern oder eine lebenslange Lizenz erwerben.

## Lebenslange Lizenz

Sobald Sie Ihren Homey Self-Hosted Server eingerichtet haben, können Sie auf der Seite [Meine selbst gehosteten Server](https://homey.app/account/self-hosted-servers/) eine lebenslange Lizenz erwerben.

Sie können Ihre lebenslange Lizenz über die Verwaltungsseite für selbst gehostete Server zwischen verschiedenen Installationen übertragen.

## Bekannte Probleme und Einschränkungen

- Dieses Add-on erfordert Home Assistant OS oder Home Assistant Supervised (Add-ons sind auf Home Assistant Core- oder Container-Installationen nicht verfügbar).
- Das Add-on benötigt den privilegierten Modus und Host-Netzwerkfunktionen, um ordnungsgemäß zu funktionieren.
- Es werden mindestens 1 GB verfügbarer RAM und 1 GB verfügbarer Speicherplatz empfohlen.
- Für die Erkennung ist eine dedizierte LAN-IP-Adresse erforderlich.

## Support

- [Offizielle Docker-Installationsanleitung](https://support.homey.app/hc/en-us/articles/24010537261980-How-to-install-Homey-Self-Hosted-Server-with-Docker-on-Linux)
- [Homey Self-Hosted Server Support](https://support.homey.app/hc/en-us/categories/23974566220572)
