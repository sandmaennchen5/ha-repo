### Home Assistant Repository – sandmaennchen5
## Dokumentation - Homey Self-Hosted Server

Diese App führt den offiziellen Homey Self-Hosted Server von
`ghcr.io/athombv/homey-shs:latest` auf Home Assistant OS aus.

![Screenshot des Homey Self-Hosted Servers](https://raw.githubusercontent.com/sandmaennchen5/ha-repo/master/apps/homey-shs/Homey%20Self-Hosted%20Server.png)

## Konfiguration

**Hinweis**: _Denken Sie daran, das Add-on neu zu starten, wenn die Konfiguration geändert wird._

In der App-Konfiguration können die Ports für HTTP, HTTPS und beide
Homey-Bridge-Protokolle sowie der experimentelle WebRTC-Port geändert werden.
Alle konfigurierten Ports müssen frei und voneinander verschieden sein.

Das Add-on verwendet den Host-Netzwerkmodus, was bedeutet, dass der Homey
Self-Hosted Server unter den konfigurierten Ports direkt im lokalen Netzwerk
erreichbar ist. Der Server sollte automatisch von der Homey-App erkannt werden.

Die tatsächlichen Ports werden ausschließlich über die vier Optionen
`port_server_http`, `port_server_https`, `port_server_bridge_v1` und
`port_server_bridge_v2` festgelegt. Wegen des Host-Netzwerkmodus ist keine
zusätzliche Portzuordnung im Home-Assistant-Bereich **Netzwerk** erforderlich.

Falls Homey die LAN-Adresse des Hosts nicht korrekt erkennt, kann sie unter
**Erweiterte Einstellungen → Lokale IPv4-Adresse**
(`extras.homey_local_address`) eingetragen werden. Bleibt das Feld leer,
verwendet Homey weiterhin die automatische Erkennung.

Im aufklappbaren Bereich **Erweiterte Einstellungen** stehen außerdem von Homey
derzeit nicht offiziell dokumentierte Optionen für WebRTC, Matter-mDNS,
App-Protokollierung, Web-App-Proxy, App-Entwicklermodus und den öffentlichen
Delegation-Token-Schlüssel zur Verfügung. Diese Optionen sollten nur bei einem
konkreten Bedarf geändert werden; leere Felder verwenden das jeweilige
Homey-Standardverhalten.

Mit `storage_location` wird festgelegt, ob Homey seine Daten privat unter
`/data`, im sichtbaren App-Konfigurationsordner unter `/config` oder in einem
frei wählbaren Unterordner von `/share` speichert.

```yaml
storage_location: share
share_storage_directory: /config/homey-shs
```

Ein führender Schrägstrich wird bei `share_storage_directory` als relativ zu
`/share` interpretiert. Das Beispiel verwendet daher
`/share/config/homey-shs`. Auch `/homey-shs-config` ist möglich.

Beim Wechsel überträgt die App einen vorhandenen Datenbestand in das gewählte
Ziel. Nach erfolgreicher Übertragung wird der Homey-Bestand im unbenutzten
Speicherort entfernt. Existieren Daten in mehreren Verzeichnissen, gilt der
von einer älteren App-Version markierte Speicherort einmalig als maßgeblich;
ansonsten hat die aktuelle Option Vorrang. Die Markierung wird anschließend
entfernt. `/data/options.json` wird weder verschoben noch gelöscht.

## Netzwerk

Die App verwendet das Host-Netzwerk und belegt diese TCP-Ports:

- `4859`: HTTP und Socket.IO
- `4860`: HTTPS
- `4861`: Homey Bridge v1
- `4862`: Homey Bridge v2
- `8555`: WebRTC (experimentell)

Dies sind die Standardwerte. Werden sie in der Konfiguration geändert, verwendet
Homey die dort eingetragenen Ports. Bei einem abweichenden HTTP-Port kann die
Weboberfläche direkt über `http://<HOST>:<HTTP-PORT>` geöffnet werden.

Stelle sicher, dass die Ports auf dem Home-Assistant-Host nicht bereits von
anderen Diensten verwendet werden.

## Weboberfläche und lokaler Homey-Benutzer

Die Schaltfläche **Weboberfläche öffnen** verwendet den integrierten
Ingress-Proxy auf Port `8099`. Er liest
den von Home Assistant bereitgestellten `X-Ingress-Path`, setzt Homeys
Host-, Origin- und Referer-Header um und passt Weiterleitungen, Cookies,
HTML-, API- und Ressourcenpfade sowie Socket.IO-/WebSocket-Verbindungen an.

Die direkte Oberfläche bleibt unabhängig davon unter
`http://<HOST>:<HTTP-PORT>` erreichbar. Da Homeys Web-App nicht offiziell für
dynamische Unterpfade entwickelt wurde, können einzelne Ansichten oder
zukünftige Homey-Versionen weiterhin über Ingress fehlschlagen.

### Lokalen Benutzer anlegen

Die Ersteinrichtung des Homey Self-Hosted Servers muss bereits mit der mobilen
Homey-App abgeschlossen sein. Danach legt der Besitzer den lokalen Benutzer in
der Homey Web App an:

1. Die [Homey Web App](https://my.homey.app/) öffnen und als Besitzer anmelden.
2. Zu **Familie & Gäste** wechseln.
3. Die Person auswählen, für die ein lokaler Zugang eingerichtet werden soll.
4. Das Drei-Punkte-Menü öffnen und **Lokalen Benutzer aktivieren** auswählen.
5. Einen lokalen Benutzernamen und ein separates Passwort festlegen.
6. In Home Assistant die App-Seite öffnen und **Web-UI öffnen** wählen oder
   den direkten lokalen Link verwenden.
7. Mit dem soeben angelegten lokalen Homey-Benutzer anmelden.

Der Besitzer kann lokale Zugänge für alle Personen verwalten. Andere Benutzer
können nur ihren eigenen lokalen Zugang verwalten. Alternativ ist die Anmeldung
im lokalen Netz direkt über `http://<HOME-ASSISTANT-IP>:4859` möglich.

## Technische Details

- **Docker-Image**: `ghcr.io/athombv/homey-shs:latest`
- **Netzwerkmodus**: Host-Netzwerk (erforderlich für die Geräteerkennung)
- **Privilegierter Modus**: Aktiviert (Homey Self-Hosted Server erwartet, im privilegierten Modus ausgeführt zu werden)
- **Datenverzeichnis**: wahlweise `/data`, `/config` oder ein Unterordner von `/share`
- **Direkte Web-UI**: Erreichbar unter `http://<HOST>:<port_server_http>`
- **Ingress**: Experimenteller Anpassungsproxy auf Port `8099`

### Home-Assistant-Authentifizierung

Home Assistant authentifiziert den Benutzer bereits vor dem Ingress-Zugriff
und übermittelt dessen Identität in `X-Remote-User-*`-Headern. Homey besitzt
jedoch keine dokumentierte Schnittstelle, die diese Identität als lokalen
Homey-Benutzer akzeptiert. Deshalb ist weiterhin die Anmeldung mit dem lokalen
Homey-Benutzernamen und Passwort erforderlich.

`auth_api: true` würde der App lediglich Zugriff auf Home Assistants
Benutzerprüfung geben. Es erzeugt keine Homey-Sitzung und ist deshalb nicht
aktiviert.

### Automatische Zuordnung je Home-Assistant-Benutzer

Mit **Homey-Anmeldung je HA-Benutzer merken**
(`remember_ingress_users`) kann die automatische Zuordnung aktiviert werden.
Danach funktioniert die
Einrichtung für jeden berechtigten Home-Assistant-Benutzer getrennt:

1. Die Homey-Weboberfläche über Ingress öffnen.
2. Einmal mit dem gewünschten lokalen Homey-Benutzer anmelden.
3. Beim nächsten Öffnen ordnet der Proxy die gespeicherte Homey-Sitzung anhand
   der von Home Assistant gelieferten Benutzer-ID automatisch wieder zu.

Das lokale Homey-Passwort wird dabei weder abgefangen noch gespeichert. Die
gespeicherte Sitzung ist trotzdem wie ein Zugangsschlüssel zu behandeln. Sie
liegt mit eingeschränkten Dateirechten unter `/data/ingress-sessions`, wird
nicht in einen konfigurierten `/share`-Export aufgenommen und bei einer von
Homey abgelehnten Sitzungsprüfung automatisch gelöscht.

Die Browserdaten der Homey-Web-App werden ebenfalls je Home-Assistant-Benutzer
getrennt. Für eine neue Zuordnung muss die gespeicherte Sitzung gelöscht und
die Weboberfläche erneut geöffnet werden. Dies ist über einen POST-Aufruf auf
den Ingress-internen Pfad `/__homey_ingress_forget_session` möglich.

Die Zuordnung gilt nur für den Ingress-Zugriff. Beim direkten Aufruf von
`http://<HOST>:<HTTP-PORT>` bleibt Homeys normale lokale Anmeldung aktiv.

## Sicherheitsbewertung

Home Assistant bewertet diese App derzeit mit **1**. Der entscheidende Grund
ist `full_access: true`: Vollzugriff setzt die Bewertung unabhängig von Ingress
oder weiteren Schutzmaßnahmen direkt auf 1. Der ebenfalls benötigte
Host-Netzwerkmodus würde die Bewertung ohne Vollzugriff zusätzlich um einen
Punkt senken.

Für eine höhere Bewertung müsste `full_access` entfernt und durch die
tatsächlich benötigten einzelnen Geräte-, Kernel- und Netzwerkberechtigungen
ersetzt werden. Das sollte erst nach Tests aller Homey-Funktionen wie
Discovery, Matter, WebRTC und Homey Bridge erfolgen; ein ungeprüftes Entfernen
kann Funktionen unbemerkt beschädigen.

Eine sinnvolle weitere Härtung wäre anschließend ein eigenes AppArmor-Profil.
Solange `full_access: true` erforderlich ist, bleibt die sichtbare
Sicherheitsbewertung jedoch 1.

## Daten und Backups

Homey speichert seine Daten unter `/homey/user`. In dieser App zeigt der Pfad
je nach `storage_location` auf `/data`, `/config` oder den konfigurierten
`/share`-Unterordner. Dadurch bleiben Einstellungen, Geräte und Flows bei
App-Updates erhalten. `/data` und das eigene `/config` werden mit der App in
Home-Assistant-Backups aufgenommen. Inhalte unter `/share` gehören dagegen
nicht zum partiellen Backup dieser App und benötigen eine separate Sicherung.

Beim Start richtet ein Entrypoint-Wrapper die Verknüpfung ein und kopiert bei
Bedarf Daten aus älteren Installationen in den gewählten Speicherort.
RRD-Daten werden in dessen Unterordner `rrd` gespeichert.

Der Share-Speicherordner darf sich nicht mit `export_directory` oder
`import_search_directory` überschneiden. Dadurch werden rekursive Exporte und
das versehentliche Löschen von Backup-Archiven verhindert.

### Export und Import

Die Import- und Exporteinstellungen befinden sich im ausklappbaren Bereich
**Import/Export**:

```yaml
import_export:
  export_on_stop: false
  export_directory: homey-shs-backups
  export_filename: "homey-shs-{version}-{timestamp}.tar.gz"
  import_mode: none
  import_search_directory: homey-shs-backups
  import_source: ""
  overwrite_existing_data: false
  allow_version_downgrade: false
  delete_after_import: false
```

Mit `import_export.export_on_stop: true` beendet die App Homey zuerst sauber
und exportiert danach den gewählten Datenspeicher. `export_directory` ist ein
relativer Pfad unter `/share`; `export_filename` unterstützt `{version}`,
`{timestamp}`, `{storage}` und `{slug}`.

`import_mode: auto` sucht unter `import_search_directory` nach einem passenden
Homey-SHS-Export. `import_mode: manual` verwendet den relativen `/share`-Pfad
aus `import_source`. Importiert wird nur in einen Speicherort, der noch keine
Homey-Daten enthält. Mit `overwrite_existing_data: true` kann ein geprüfter
Import den vorhandenen Homey-Bestand ersetzen; `/data/options.json` bleibt
erhalten. Erkannte Downgrades werden standardmäßig abgelehnt. Mit
`allow_version_downgrade: true` kann diese Prüfung ausdrücklich umgangen
werden. Das kann zu inkompatiblen oder unbrauchbaren Homey-Daten führen. Die
übrigen Archiv- und Pfadprüfungen bleiben aktiv. Das Archiv bleibt standardmäßig
erhalten und wird nur mit `delete_after_import: true` gelöscht.

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
