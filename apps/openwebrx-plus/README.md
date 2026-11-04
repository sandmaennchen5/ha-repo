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

Dies ist interaktive Decodierung für den gewählten Browserkanal. Ein
unbeaufsichtigter Dauerbetrieb ohne verbundenen Browser, Alarmierung, MQTT-
Weiterleitung und permanente Protokollierung sind nicht implementiert.

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
`multimon-ng` und `rtl-sdr` aus Debian und dem offiziellen Plus-Repository.
Das Plus-Repository bietet Bookworm-Pakete für ARM64. Der Build verwendet
aktuelle Pakete, ist daher nicht auf unveränderliche Versionen festgelegt.
Die tatsächlich installierten Versionen stehen im Image in
`/usr/share/openwebrx-build-packages.txt`.

Auf einem Docker-Rechner mit ARM64-Unterstützung bzw. eingerichteter Emulation:

```sh
docker buildx build --platform linux/arm64 --load -t ha-openwebrx-plus:local apps/openwebrx-plus
python -m unittest discover -s apps/openwebrx-plus/tests -v
```

Ein anschließender HAOS-Test muss bestätigen: HTTP 8073 erreichbar, Anmeldung
möglich, Frequenzwechsel, ZVEI-Testfolge erkannt, Profile nach Neustart erhalten,
fehlender zweiter Stick ohne Zugriff auf `00001001`, wmbusmeters und Homematic
weiter funktionsfähig. In der Entwicklungsumgebung ist kein Docker vorhanden;
ein erfolgreicher Container-Build oder Hardwaretest wird nicht behauptet.

## Mögliche Erweiterung: mehrere ZVEI-Kanäle

Mehrkanalüberwachung ist **nicht Bestandteil dieser Version**. Zusätzliche
Profile oder ein Scanner bedeuten keine gleichzeitige Überwachung. Upstreams
ZVEI-Modus ist derzeit nicht als Hintergrunddienst (`service=True`) registriert.
Eine Erweiterung müsste aus einem gemeinsamen IQ-Datenstrom mehrere Kanäle
innerhalb der SDR-Bandbreite demodulieren, pro Kanal multimon-ng betreiben und
Ergebnisse mit Frequenz und Zeitstempel zusammenführen. CPU-Last, Rauschsperre,
Browserunabhängigkeit und Neustartverhalten wären auf dem Pi 5 zu testen.
Dafür keinen zweiten konkurrierenden `rtl_fm`-Prozess am selben Stick starten.

## Geprüfte Upstream-Quellen

- [Offizielles Plus-Paketrepository, ARM64 und Bookworm-Installation](https://luarvique.github.io/ppa/)
- [ZVEI-Modus und Dienstkennzeichnung](https://github.com/luarvique/openwebrx/blob/master/owrx/modes.py)
- [ZVEI-Decodierung mit multimon-ng](https://github.com/luarvique/openwebrx/blob/master/csdr/chain/toolbox.py)
- [Seriennummer als RTL-SDR-Gerätekennung](https://github.com/luarvique/openwebrx/blob/master/owrx/source/rtl_sdr.py)
- [Persistente settings.json](https://github.com/luarvique/openwebrx/blob/master/owrx/config/dynamic.py)
