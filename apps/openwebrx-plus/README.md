# OpenWebRX+ ZVEI für Home Assistant OS

Lokales, Docker-basiertes Add-on für Raspberry Pi 5 mit 64-Bit-HAOS
(`aarch64`). Experimenteller Stand; ein Hardwaretest auf HAOS steht noch aus.
Homematic/OpenCCU und wmbusmeters werden nicht umkonfiguriert.

## Installation

1. Diesen Ordner vollständig nach `/addons/openwebrx-plus` auf dem HAOS-System
   kopieren (beispielsweise über die vorhandene Samba-Freigabe `addons`).
2. Im Add-on-/App-Store nach lokalen Apps suchen bzw. aktualisieren und
   **OpenWebRX+ ZVEI** installieren. Es gibt bewusst kein `image`-Feld:
   Supervisor baut den Container lokal für ARM64.
3. In den Add-on-Optionen die **tatsächliche, eindeutige Seriennummer des zweiten
   RTL-SDR** als `rtl_serial` eintragen. Kein Geräteindex wie `0` oder `1`!
   Es wird keine unbekannte Seriennummer angenommen und keine umprogrammiert.
   `00001001` ist für wmbusmeters reserviert und wird abgewiesen.
   Seriennummern vorab anhand vorhandener Geräteinformationen oder auf einem
   separaten Linux-Rechner prüfen; laufendes wmbusmeters nicht dafür stoppen.
4. `admin_password` mit mindestens zwölf Zeichen setzen. Der Benutzer `admin`
   wird nur beim ersten Start angelegt. Spätere Passwortänderungen erfolgen
   in OpenWebRX+; die Add-on-Option setzt ein vorhandenes Passwort nicht zurück.
5. Starten und `http://<HA-IP>:8073` öffnen. Kein Ingress erforderlich.

Beispiel (Seriennummer unbedingt ersetzen):

```yaml
rtl_serial: "DEINE_ZWEITE_SERIENNUMMER"
initial_frequency: 145500000
sample_rate: 1024000
rf_gain: 29
ppm: 0
admin_password: "EIN_LANGES_EIGENES_PASSWORT"
```

Die Frequenz ist ein Beispiel in Hz. `initial_frequency`, `sample_rate` und
`rf_gain` initialisieren nur das erste Profil. Anschließend Profile/Frequenzen
in der Weboberfläche unter Settings bearbeiten; diese Änderungen bleiben
bestehen. `rtl_serial` und `ppm` werden bei jedem Start aus den Add-on-Optionen
übernommen. Vor Änderungen an den Optionen das Add-on neu starten.

## Voreingestellte Profile ab Version 0.2.0

Im Empfänger die Profilauswahl öffnen. In Echo weiterhin den Servertyp
**OpenWebRX** verwenden. Die UKW-Profile schalten zwischen überlappenden
Empfangsfenstern um; dadurch ist das gesamte Band erreichbar, auch wenn
jeweils nur 2,4 MHz im Wasserfall sichtbar sind.

| Profil | Frequenz / Modus | Zweck |
| --- | --- | --- |
| ZVEI | bisherige Startfrequenz / Zvei | 5-Ton-Decodierung |
| UKW / RDS | 88,5 bis 107,5 MHz, mehrere Fenster / WFM | Rundfunk 87,5–108 MHz und RDS |
| CB | 27,2 MHz / AM | CB-Empfang, bei Bedarf FM auswählen |
| Flugfunk | 121,5 MHz / AM | Beispielprofil, Frequenz selbst einstellen |
| Amateurfunk 2 m | 145 MHz / FM | Analoger Sprechfunk |
| APRS | 144,800 MHz / Packet | APRS-Pakete über Dire Wolf |
| Amateurfunk 70 cm | 434 MHz / FM | Analoger Sprechfunk |
| PMR446 | 446,1 MHz / FM | PMR446-Kanäle |
| ISM 433 | 433,920 MHz / ISM | Von rtl_433 unterstützte Sensorprotokolle |

Beim ersten Start nach dem Update werden fehlende Voreinstellungen ergänzt.
Vorhandene Profile mit derselben Kennung behalten ihre Einstellungen, auch das
bisherige ZVEI-Profil. `/data/profile-presets-v1.json` merkt sich die einmalige
Ergänzung. Danach werden absichtlich gelöschte Profile nicht erneut angelegt.
Eigene Profile bleiben bestehen. Für eine bewusste erneute Ergänzung kann
bei gestopptem Add-on nach einem Backup ausschließlich diese Markerdatei
entfernt werden; `settings.json` dafür nicht löschen.

Ein Profilwechsel stimmt den gemeinsamen zweiten Stick um. Es gibt weiterhin
keine gleichzeitige Überwachung verschiedener Frequenzbereiche. Homematic und
der für wmbusmeters reservierte Stick `00001001` bleiben davon unabhängig.

## Decoder und Erweiterungen

Die Decoder werden als Linux-Pakete ins Image integriert. Es ist keine
Installation von Browser-Plugins oder fremdem JavaScript erforderlich.

| Decoder | Enthaltene Funktion | Auswahl |
| --- | --- | --- |
| multimon-ng | ZVEI1/2/3, DZVEI, PZVEI; DTMF/EEA/EIA/CCIR; POCSAG/FLEX | Zvei, SelCall oder Page |
| redsea | RDS, etwa Senderkennung und Radiotext bei ausreichendem Signal | UKW mit WFM |
| Dire Wolf + APRS-Symbole | AX.25/APRS | Packet / APRS-Profil |
| rtl_433 | Unterstützte ISM-Sensorprotokolle | ISM-Profil |
| LAME | MP3-Audioaufzeichnung; kein Funkdecoder | OpenWebRX+-Aufzeichnungsfunktion |

RDS, Packet, ISM, Page, SelCall und MP3 werden zusätzlich bei Build und Start
auf Verfügbarkeit geprüft. Welche Bedienelemente Echo davon zeigt, hängt von
der App ab; zum Prüfen die vollständige Weboberfläche in Safari verwenden.
Frequenz, Modulation, Signalqualität und das tatsächlich gesendete Protokoll
müssen zusammenpassen. Paging wird als Modus bereitgestellt, ohne eine
ortsabhängige Empfangsfrequenz vorzubelegen.

DAB+, DMR/TETRA und andere digitale Sprachdecoder sind mit diesen zusätzlichen
Paketen nicht automatisch installiert. Die optionale MQTT-Anbindung und
Einkanal-Dauerüberwachung werden im folgenden Abschnitt beschrieben.

## Empfang und ZVEI

Das Startprofil verwendet `start_mod: zvei`. OpenWebRX+ demoduliert NFM und
führt das Audio seinem integrierten multimon-ng zu. Die ZVEI-Familien ZVEI1,
ZVEI2, ZVEI3, DZVEI und PZVEI sind verfügbar. Im Browser den Modus **Zvei**
wählen, falls ein anderes Profil aktiv ist; Ergebnisse erscheinen im
Decoderbereich. Empfangsfrequenz und Wasserfall lassen sich im Browser
bedienen. Mit erlaubten Mittenfrequenzänderungen bzw. eigenen Profilen lässt
sich auch außerhalb des aktuell sichtbaren Empfangsfensters abstimmen,
innerhalb der Grenzen des angeschlossenen Tuners.

Für die ersten Tests die Rauschsperre öffnen bzw. niedrig einstellen und einen
bekannten, ausreichend starken Test mit einer 5-Ton-Folge verwenden. Die
reale ZVEI-Decodierung ist ohne SDR und Testsignal hier nicht nachgewiesen.
Der Container prüft beim Build und Start die Verfügbarkeit von ZVEI und
multimon-ng. Fehlende Decoder führen zum Fehler statt zu stillem FM-Betrieb.

Der Zvei-Modus im Browser bleibt interaktiv. Zusätzlich gibt es ab Version
0.3.0 einen separaten Einkanal-Hintergrunddecoder mit dauerhaftem Protokoll
und optionaler MQTT-Anbindung, siehe unten.

## ZVEI-Dauerüberwachung und Home Assistant ab 0.3.0

```yaml
monitor_enabled: true
monitor_frequency: 0
mqtt_enabled: false
mqtt_host: core-mosquitto
mqtt_port: 1883
mqtt_user: ""
mqtt_password: ""
mqtt_tls: false
mqtt_topic: openwebrx/zvei
```

`monitor_frequency` ist die feste Empfangsfrequenz in **Hz**. `0` übernimmt
beim Start die gespeicherte `start_freq` des bisherigen Profils `zvei`,
ansonsten `initial_frequency`. Das ist nicht automatisch die zuletzt im
Browser eingestellte Frequenz. Für verlässlichen Betrieb eine explizite
Frequenz eintragen und das Add-on neu starten.

Der Monitor aktiviert beim Start das verwaltete Profil
**ZVEI Dauerüberwachung** und hält den Empfänger ohne verbundenen Browser
aktiv. Er verwendet den vorhandenen IQ-Datenstrom von OpenWebRX+ mit einem
zusätzlichen NFM/multimon-ng-Decoder; es wird kein konkurrierendes `rtl_fm`
oder zweiter USB-Empfangsprozess gestartet. Die fünf ZVEI-Familien werden
parallel auf **diesem einen Kanal** ausgewertet.

Die erste Dienstinitialisierung benötigt durch den OpenWebRX+-Dienstplaner
ungefähr zehn Sekunden. Beim Profil- oder Mittenfrequenzwechsel wird der
Decoder neu aufgebaut. Liegt der feste Kanal außerhalb des neuen Fensters,
pausiert er und meldet `frequency_outside_window`. Zur Wiederaufnahme das
Profil **ZVEI Dauerüberwachung** auswählen; danach die Initialisierung
abwarten. Andere Frequenzen innerhalb desselben Fensters können im Browser
gehört werden. UKW-Rundfunk in einem anderen Fenster und gleichzeitige
ZVEI-Überwachung sind mit diesem Stick nicht möglich.

Während der Monitor aktiv ist, verwaltet das Add-on `always-on`, `services`,
`services_enabled`, `services_decoders` und das zusätzliche Monitorprofil.
Diese Einstellungen in der Weboberfläche nicht ausschalten. Die vorherigen
Dienst-Einstellungen werden in `/data/zvei-monitor-restore.json` gesichert
und beim Start mit `monitor_enabled: false` wiederhergestellt. Eigene
Empfangsprofile bleiben erhalten. Andere OpenWebRX+-Hintergrunddecoder werden
im Überwachungsmodus nicht zusätzlich gestartet.

### Dauerhaftes Protokoll

`/data/zvei/events.jsonl` enthält pro erkannter 5-Ton-Folge eine JSON-Zeile:

```json
{"event_type":"zvei","timestamp":"2026-11-04T21:00:00+00:00","frequency_hz":85000000,"rtl_serial":"00001002","decoder":"ZVEI1","tones":"1E2E3","sequence":"11223"}
```

Die Frequenz im Beispiel ist kein allgemeiner ZVEI-Kanal. Zeitstempel sind
UTC. `tones` enthält die ursprünglichen fünf Tonsymbole; `sequence` ersetzt
Wiederholton `E` durch die vorherige Ziffer. Nicht exakt fünfstellige oder
andere Sondertonfolgen werden nicht als 5-Ton-Ereignis übernommen.
Identische normalisierte Folgen werden innerhalb von zwei Sekunden
familienübergreifend zusammengefasst, auch wenn mehrere Decoder anschlagen.
Das kann sehr schnell wiederholte echte Rufe ebenfalls zusammenfassen.

Das Protokoll bleibt bei Neustarts und Updates erhalten, ist aber begrenzt:
5 MiB je Datei und fünf Archivdateien, insgesamt ungefähr 30 MiB. Älteste
Einträge werden anschließend überschrieben. Die Dateien gehören zum
Add-on-Backup und sind über den Dateisystemzugriff auf das Add-on-Datenverzeichnis
einsehbar; sie liegen nicht automatisch in der Samba-`config`-Freigabe.

### MQTT und automatisch erkannte HA-Entitäten

Einen vorhandenen MQTT-Broker und die MQTT-Integration in Home Assistant
verwenden. `mqtt_enabled: true` setzen, Host/Port und eigene Broker-Zugangsdaten
eintragen. `core-mosquitto` ist nur der übliche interne Hostname des
Mosquitto-Add-ons; es wird kein Broker installiert oder umkonfiguriert.
Für TLS `mqtt_tls: true` und den passenden Port (üblicherweise 8883) setzen;
Serverzertifikate werden gegen den System-Zertifikatsspeicher geprüft.

MQTT Discovery legt unter **OpenWebRX+ ZVEI** diese Entitäten an:

- Ereignis **Tonfolge**: neue ZVEI-Erkennung mit Frequenz, Decoder und Folge.
- Sensor **Letzte Tonfolge**: zuletzt veröffentlichte Folge mit JSON-Attributen.
- Binärsensor **Überwachung**: aktiv oder pausiert; Attribute enthalten Grund
  und Frequenz. Die Geräteverfügbarkeit zeigt die Verbindung des Add-ons zum
  Broker, nicht einen Nachweis der Funkempfangsqualität.

Standardtopics (Seriennummer durch den eigenen zweiten Stick ersetzen):

| Topic | Inhalt |
| --- | --- |
| `openwebrx/zvei/00001002/event` | Neue Folge als JSON, nicht retained |
| `openwebrx/zvei/00001002/last` | Letztes Ereignis, retained |
| `openwebrx/zvei/00001002/status` | Überwachungsstatus als JSON, retained |
| `openwebrx/zvei/00001002/availability` | `online` oder `offline`, retained/LWT |

Discovery wird bei Brokerverbindung und bei Home-Assistant-Neustart erneut
gesendet. Bei MQTT-Ausfall läuft die lokale Protokollierung weiter. Ereignisse
werden nicht nachträglich abgespielt; eine Folge während des Ausfalls erreicht
Home Assistant daher nicht. Dies vermeidet verspätete Alarme nach Reconnect.
MQTT ist keine garantierte Alarmübertragung.

Beispiel für eine HA-Automation auf eine bestimmte Folge; Topic und Folge
anpassen und eine eigene Aktion ergänzen:

```yaml
alias: ZVEI Tonfolge erkannt
triggers:
  - trigger: mqtt
    topic: openwebrx/zvei/00001002/event
conditions:
  - condition: template
    value_template: "{{ trigger.payload_json.sequence == '12345' }}"
actions:
  - action: persistent_notification.create
    data:
      title: ZVEI erkannt
      message: >-
        Folge {{ trigger.payload_json.sequence }} auf
        {{ trigger.payload_json.frequency_hz }} Hz
```

Ereignisse stammen aus automatischer Funkdecodierung und können falsch
erkannt werden. Erst mit einem bekannten Testsignal und passenden
Automationsbedingungen prüfen. Echo muss für den Hintergrundmonitor nicht
laufen; die MQTT-Entitäten werden in Home Assistant angezeigt.

## RDS-Protokoll und Home Assistant ab 0.4.0

```yaml
rds_logging: true
rds_mqtt_topic: openwebrx/rds
```

Zum Empfang ein **UKW / RDS**-Profil wählen und in Echo oder der
Weboberfläche einen Sender mit **WFM** hören. Die Erweiterung übernimmt die
Metadaten aus dem vorhandenen redsea/RDS-Decoder. Sie stimmt den Stick nicht
selbst um, startet keinen zusätzlichen USB-Empfänger und erzeugt keine
browserunabhängige UKW-Dauerüberwachung. Ohne aktiven WFM-Decoder kommen keine
neuen RDS-Einträge hinzu. Der ZVEI-Hintergrundmonitor pausiert beim Wechsel
in ein anderes Frequenzfenster wie bisher.

Erfasst werden, soweit gesendet und erfolgreich decodiert:

- `pi`: RDS-Programmkennung, beispielsweise `0xD3C2`.
- `ps`: bis zu acht Zeichen Sendername.
- `radiotext`: bis zu 64 Zeichen Radiotext.
- `prog_type`: Programmtyp.
- `tp` und `ta`: Verkehrsfunkkennung und aktuelle Verkehrsdurchsage.
- `frequency_hz`, UTC-`timestamp` und die verwendete SDR-Seriennummer.

Änderungen werden nach `/data/rds/events.jsonl` geschrieben. Gleichbleibende
RDS-Gruppen werden nicht immer wieder protokolliert; Frequenz- und PI-Wechsel
setzen die gesammelten Senderdaten zurück, sodass kein Radiotext des vorherigen
Senders übernommen wird. Die Datei rotiert wie das ZVEI-Protokoll mit 5 MiB
und fünf Archiven. `rds_logging: false` schaltet die zusätzliche Aufzeichnung
und RDS-MQTT-Verbindung ab; die normale RDS-Anzeige in OpenWebRX+ bleibt erhalten.

Für MQTT dieselben Broker-Optionen wie beim ZVEI-Monitor verwenden:
`mqtt_enabled: true`, Host/Port und Zugangsdaten. Die RDS-Anbindung funktioniert
auch mit `monitor_enabled: false`. Beide verwenden unterschiedliche Client-IDs
und Topics. Unter **OpenWebRX+ RDS** werden automatisch fünf Sensoren angelegt:

| Sensor | Inhalt |
| --- | --- |
| Zuletzt empfangener Sender | PS-Sendername, ersatzweise PI |
| RDS PI | Programmkennung |
| Radiotext | Zuletzt decodierter Text |
| RDS Frequenz | Empfangsfrequenz in MHz |
| Programmtyp | Decodierter Programmtyp |

Alle Sensoren enthalten den Zeitstempel und die übrigen Metadaten als
Attribute. Dies sind **zuletzt bekannte Daten**, kein Nachweis, dass dieser
Sender weiterhin empfangen wird. `timestamp` bezeichnet die aufgezeichnete
Metadatenänderung. Die MQTT-Geräteverfügbarkeit beschreibt die Verbindung des
Add-ons zum Broker, nicht die Verbindung eines Browsers oder den RDS-Empfang.

Standardtopics bei Seriennummer `00001002`:

- `openwebrx/rds/00001002/last`: letzte Metadaten, retained, für HA-Sensoren.
- `openwebrx/rds/00001002/event`: Änderungen, nicht retained.
- `openwebrx/rds/00001002/availability`: online/offline mit Last Will.

Beim Broker-/HA-Neustart werden Discovery und die zuletzt im laufenden Prozess
bekannten Metadaten erneut gesendet. Alte RDS-Ereignisse werden dabei nicht
abgespielt. Nach einem Add-on-Neustart zeigt MQTT gegebenenfalls noch den
retained Wert des früheren Empfangs; neue Werte kommen erst bei erneutem
WFM/RDS-Empfang. Die Textfelder werden nicht auf Vollständigkeit oder die
inhaltliche Richtigkeit der ausgestrahlten Informationen geprüft.

## Geräte und Speicherung

- Nur ein verwalteter Empfänger `dedicated_rtl`, Auswahl ausdrücklich über
  Seriennummer. Kein automatischer Rückfall auf den ersten USB-Empfänger.
- Ein vorgeschalteter `rtl_connector` verweigert fehlende oder abweichende
  Gerätekennungen auch nach Änderungen in der Weboberfläche. Weitere Geräte
  dort nicht anlegen; gespeicherte zusätzliche SDRs verhindern den Neustart.
- HAOS `usb: true` macht USB-Geräte im Container erreichbar. Das ist keine
  USB-Isolation nach Seriennummer; die Anwendungsauswahl schützt den normalen
  RTL-SDR-Betrieb. Kein privilegierter Modus, Docker-Socket, Hostnetzwerk oder
  Zugriff auf Homematic-Konfiguration ist nötig.
- `/data/openwebrx/settings.json`: Profile und Web-Einstellungen.
- `/data/openwebrx/users.json`: Benutzer und Passwort-Hashes.
- Weitere OpenWebRX+-Daten liegen ebenfalls in `/data/openwebrx`.
- `/data/openwebrx.conf`: beim Start erzeugte Serverkonfiguration, Port 8073.
- `/data` bleibt bei Neustarts und Updates erhalten und gehört in das
  Add-on-Backup. Deinstallation kann diese Daten löschen.

Bei fehlendem, belegtem oder nicht eindeutig serialisiertem zweiten Stick
zuerst die Gerätezuordnung prüfen. Keine USB-Resets, Treiberänderungen oder
EEPROM-Schreibbefehle am laufenden HAOS-System ausführen. Webzugriff auf das
vertrauenswürdige LAN beschränken; Port 8073 wird ohne TLS veröffentlicht.

## ARM64-Build und Prüfung

Das Image basiert auf Debian Bookworm und installiert `openwebrx`,
`multimon-ng`, `rtl-sdr`, `redsea`, `rtl-433`, `direwolf`, `aprs-symbols`
und `lame` aus Debian und dem offiziellen Plus-Repository.
Das Plus-Repository bietet Bookworm-Pakete für ARM64. Der Build verwendet
aktuelle Pakete, ist daher nicht auf unveränderliche Versionen festgelegt.
Die tatsächlich installierten Versionen stehen im Image in
`/usr/share/openwebrx-build-packages.txt`.

Die Repository-CI baut dieses lokale Add-on zur Prüfung, veröffentlicht aber
kein Image und keinen Registry-Manifest. `.var.yaml` kennzeichnet den
Upstream-Paketstand als `bookworm-rolling`; automatische Versionsupdates sind
für dieses nicht auf eine Paketversion festgelegte Add-on deaktiviert.

Auf einem Docker-Rechner mit ARM64-Unterstützung bzw. eingerichteter Emulation:

```sh
docker buildx build --platform linux/arm64 --load -t ha-openwebrx-plus:local apps/openwebrx-plus
python -m unittest discover -s apps/openwebrx-plus/tests -v
```

Ein anschließender HAOS-Test muss bestätigen: HTTP 8073 erreichbar, Anmeldung
möglich, Frequenzwechsel, ZVEI-Testfolge erkannt, Profile nach Neustart erhalten,
fehlender zweiter Stick ohne Zugriff auf `00001001`, wmbusmeters und Homematic
weiter funktionsfähig. Der ARM64-Container-Build wurde in GitHub Actions erfolgreich ausgeführt
(siehe VALIDATION.md). Ein Hardwaretest auf HAOS steht weiterhin aus.

## Mögliche Erweiterung: mehrere ZVEI-Kanäle

Mehrkanalüberwachung ist **nicht Bestandteil dieser Version**. Zusätzliche
Profile oder ein Scanner bedeuten keine gleichzeitige Überwachung. Upstreams
ZVEI-Modus ist derzeit nicht als Hintergrunddienst (`service=True`) registriert.
Eine Erweiterung müsste aus einem gemeinsamen IQ-Datenstrom mehrere Kanäle
innerhalb der SDR-Bandbreite demodulieren, pro Kanal multimon-ng betreiben und
Ergebnisse mit Frequenz und Zeitstempel zusammenführen. CPU-Last, Rauschsperre,
Browserunabhängigkeit und Neustartverhalten wären auf dem Pi 5 zu testen.
Dafür keinen zweiten konkurrierenden `rtl_fm`-Prozess am selben Stick starten.
Die Einkanal-Erweiterung ab 0.3.0 ist noch keine Mehrkanalüberwachung.

## Geprüfte Upstream-Quellen

- [Offizielles Plus-Paketrepository, ARM64 und Bookworm-Installation](https://luarvique.github.io/ppa/)
- [ZVEI-Modus und Dienstkennzeichnung](https://github.com/luarvique/openwebrx/blob/master/owrx/modes.py)
- [ZVEI-Decodierung mit multimon-ng](https://github.com/luarvique/openwebrx/blob/master/csdr/chain/toolbox.py)
- [Seriennummer als RTL-SDR-Gerätekennung](https://github.com/luarvique/openwebrx/blob/master/owrx/source/rtl_sdr.py)
- [Persistente settings.json](https://github.com/luarvique/openwebrx/blob/master/owrx/config/dynamic.py)
