# Validierungsstand

## Erweiterung 0.4.0

- RDS-Datenformat mit dem redsea-Beispiel und `owrx.toolbox.RdsParser`
  abgeglichen; vorhandene Browser-Ausgabe wird vom Hook zurückgegeben.
- Teilnachrichten, identische Gruppen, Frequenz-/PI-Wechsel, Textgrenzen,
  Protokoll-Persistenz, MQTT-Discovery und Reconnect ohne Ereigniswiedergabe
  werden durch Unit-Tests geprüft. Parser-/MQTT-Schnittstellen sind dabei
  simuliert; der Build-Smoke-Test nutzt die echte Upstream-Parserklasse.
- `smoke_rds.py` wird im Docker-Build mit zehn Sekunden Zeitlimit ausgeführt.
- Der neue ARM64-Container-Build, redsea mit RF-Testsignal und eine echte
  MQTT-Verbindung konnten hier mangels Docker/SDR/Broker nicht geprüft werden.
- Quellen: [redsea-Format](https://github.com/windytan/redsea#redsea-rds-decoder),
  [OpenWebRX+-Parser](https://github.com/luarvique/openwebrx/blob/master/owrx/toolbox.py).


## Erweiterung 0.3.0

- Browserunabhängiger Einkanal-Dienst auf Basis des vorhandenen
  OpenWebRX+-IQ-Puffers; keine zusätzliche USB-Empfangsinstanz.
- Dienstaufbau mit simuliertem Empfänger, Weitergabe von Decoderzeilen,
  Abschaltung bei Frequenzwechsel, fehlender Quelle und Decoderfehler getestet.
- JSONL-Persistenz über Neustarts, Wiederholton-Normalisierung, Filterung auf
  fünf Töne und Zusammenfassung identischer Folgen getestet.
- MQTT-Discovery, Status bei Reconnect/HA-Neustart, nicht-retained Ereignisse
  und unterdrückte Veröffentlichung bei Verbindungsausfall getestet.
- Aktivieren/Deaktivieren inklusive Wiederherstellung vorheriger Einstellungen
  und Übernahme einer bestehenden ZVEI-Frequenz getestet.
- Die Add-on-Tests sind nun Teil des CI-Build-Jobs. Der Docker-Build prüft
  zusätzlich die tatsächlich installierte Upstream-Service-API und erzeugt
  eine echte DSP-Kette ohne USB, inklusive Stop beim Frequenzwechsel
  (`smoke_background.py`, Zeitlimit 30 Sekunden).
- Die Unit-Tests simulieren MQTT und DSP-Quellen. Der aktuelle Container-Build,
  der neue Build-Smoke-Test, ein echter MQTT-Broker und der Empfang eines
  Testsignals auf HAOS konnten in dieser Umgebung noch nicht geprüft werden.
- Die Erweiterung verwendet interne OpenWebRX+-Service-Schnittstellen. Bei
  inkompatiblen Upstream-Änderungen sollen die Build-Prüfungen fehlschlagen;
  ein erfolgreicher früherer Build belegt diese Erweiterung nicht.


## Erweiterung 0.2.0

- Voreingestellte Empfangsfenster ergänzt; automatisiert geprüft, dass die
  UKW-Fenster lückenlos 87,5–108 MHz abdecken und die Startfrequenzen in den
  jeweiligen Fenstern liegen.
- Einmalige Übernahme in bestehende Konfigurationen geprüft: angepasste
  Profile erhalten, fehlende ergänzen, nachträglich gelöschte nicht neu anlegen.
- Neun Add-on-Tests sowie YAML- und Python-Syntaxprüfung.
- Pakete und Feature-IDs mit `owrx/feature.py` von OpenWebRX+ abgeglichen:
  redsea/RDS, Dire Wolf/Packet, APRS-Symbole, rtl_433/ISM und LAME/MP3.
- Neue Feature-Prüfungen im Dockerfile und beim Start. Der Container mit
  diesen zusätzlichen Paketen wurde hier mangels Docker/Podman noch nicht
  gebaut; der unten genannte erfolgreiche CI-Build gilt für Version 0.1.0.
- Kein Hardwaretest der neuen Decoder oder der Echo-Darstellung erfolgt.

## Basisversion 0.1.0

Prüfung am 04.11.2026:

- Repository verwendet `apps/<slug>/config.yaml` und Dockerfiles. Nur das neue
  Verzeichnis `apps/openwebrx-plus` wurde als Implementierung hinzugefügt.
- Upstream-Quellcode geprüft: `luarvique/openwebrx`, Commit
  `bf0f7715509e85b528dae15b21187183a0d8936a`.
- `owrx/modes.py`: ZVEI basiert auf NFM, benötigt `selcall` und ist nicht als
  Hintergrunddienst registriert.
- `csdr/chain/toolbox.py`: ZVEI1/2/3, DZVEI und PZVEI mit multimon-ng.
- `owrx/dsp.py`: `start_mod: zvei` aktiviert den sekundären Decoder.
- `owrx/source/connector.py`: Gerätekennung wird über `-d` übergeben.
- `owrx/feature.py`: die Geräteprüfung benötigt `rtl_connector --version`;
  diese hardwarefreie Abfrage wird vom Schutzskript durchgereicht.
- Sieben automatisierte Tests bestanden: Initialisierung, Persistenz,
  Optionsvalidierung, beschädigte Konfigurationen, reservierte/abweichende
  Gerätekennungen, fehlende/doppelte USB-Seriennummern und Versionsabfrage.
  USB-Aufrufe sind dabei simuliert; kein Hardware-Nachweis.
- YAML geparst, ARM64-Deklaration, Port, Options-/Schema-Schlüssel sowie
  Python-Syntax und LF-Zeilenenden geprüft.
- ARM64-Container-Build in GitHub Actions erfolgreich: Lauf
  [41903958772](https://github.com/sandmaennchen5/ha-repo/actions/runs/41903958772),
  Job `Build openwebrx-plus / Build aarch64`. Damit wurden auch die im
  Dockerfile enthaltenen Prüfungen von OpenWebRX+, RTL-Connector und
  multimon-ng erfolgreich ausgeführt. Kein Image veröffentlicht (lokales Add-on).
- Der nachgelagerte Job zum Eintragen der Image-Größe scheiterte in diesem
  Lauf am erwartbar fehlenden Artefakt. Der Workflow wird für reine lokale
  Builds nun ohne diesen Veröffentlichungsschritt ausgeführt.
- Kein SDR verfügbar: Funkempfang, tatsächliche ZVEI-Decodierung und
  störungsfreier Parallelbetrieb mit wmbusmeters/Homematic bleiben auf HAOS
  zu prüfen. Bestehende Add-on-Dateien wurden nicht verändert.

Die Build- und Hardware-Prüfschritte stehen in der README. Der Container-Build
ist in CI nachgewiesen; ein HAOS-/Pi-Hardwaretest steht weiterhin aus.
