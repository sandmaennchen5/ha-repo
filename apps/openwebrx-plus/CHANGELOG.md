# Changelog


## [1.2.117.2] - 2026-11-05

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/luarvique/openwebrx

---

## [1.2.117.1] - 2026-11-04

### Manuelles Update

- App-Revision für einen vollständigen Neuaufbau um eins erhöht.

Weitere Informationen: https://github.com/luarvique/openwebrx

---

## [1.2.117] - 2026-06-26

### Upstream Release Notes

Stanislav (LZ2SLL) has built this SD card image for Raspberry Pi containing a clean OpenWebRX+ 1.2.117 installation. **The image should run on all devices except for RPI1, RPI2, and RPIZero1** and supports all common SDR devices out of the box. The RTL-SDR and SDRPlay devices have been confirmed to work with no additional modifications to the image.

To flash image to an SD card, run [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and click _"APP OPTIONS"_ button, then click _"EDIT"_ button on the _"Content Repository"_. Select _"Use Custom File"_ option, then browse to the JSON file you downloaded from this page.

**Prior to flashing SD card, you can tell RPI Imager to set up the root password.** If you skip this step, you will be asked to create root password on the first startup.

Please note that **this image comes without the software support for digital modes** (DMR, NXDN, etc), since the software decoder for these modes (mbelib) has questionable origins. In order to enable digital modes in this image, ssh into the user account you created while installing the image and type:

`sudo install-softmbe.sh`

Weitere Informationen: https://github.com/luarvique/openwebrx/releases/latest

---

=======
# Änderungen

## 0.4.0

- Änderungen von RDS-Sendername, PI, Radiotext, Programmtyp und TP/TA
  beim WFM-Empfang dauerhaft als rotierendes JSONL protokollieren.
- MQTT-Discovery für fünf RDS-Sensoren mit zuletzt bekannten Senderdaten.
- Frequenz-/PI-Wechsel ohne Übernahme alter Sendertexte behandeln.
- Vorhandene Browser-Metadaten und Audioverarbeitung beibehalten.
- RDS-Aufzeichnung unabhängig vom ZVEI-Monitor aktivierbar.
- Build-Smoke-Test für den echten OpenWebRX+-RDS-Parser ergänzen.

## 0.3.0

- Einkanal-ZVEI-Hintergrunddecoder im gemeinsamen OpenWebRX+-IQ-Datenstrom.
- Verwaltetes Startprofil, kontinuierlicher Empfang ohne Browser und
  expliziter Pausenstatus bei Wechsel aus dem Empfangsfenster.
- Persistentes, rotierendes JSONL-Protokoll mit UTC, Frequenz, Decoder und Folge.
- Wiederholton-Normalisierung und Zusammenfassung identischer Folgen für zwei Sekunden.
- Optionale MQTT-Anbindung mit TLS, Last Will und Home-Assistant-Discovery
  für Ereignis, letzte Tonfolge und Überwachungsstatus.
- Keine nachträgliche Wiedergabe von MQTT-Ereignissen nach Verbindungsausfall.
- Wiederherstellung der vorherigen Diensteinstellungen beim Deaktivieren.
- Build-Prüfung mit echtem DSP-Aufbau und simuliertem Frequenzwechsel ohne USB.

## 0.2.0

- UKW mit überlappenden Fenstern für 87,5–108 MHz sowie CB, Flugfunk,
  Amateurfunk 2 m/70 cm, PMR446, APRS und ISM 433 als Profile ergänzen.
- Voreinstellungen einmalig auch in bestehende Installationen übernehmen;
  eigene Änderungen und später gelöschte Profile erhalten.
- redsea, rtl_433, Dire Wolf, APRS-Symbole und LAME installieren.
- Decoder-Verfügbarkeit zusätzlich bei Build und Start prüfen.

## 0.1.0

- Lokales ARM64-Add-on mit OpenWebRX+, multimon-ng und festem RTL-SDR.