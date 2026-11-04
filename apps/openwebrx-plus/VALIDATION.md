# Validierungsstand

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
- Kein Docker- oder Podman-Kommando in dieser Umgebung verfügbar. Daher kein
  Container-Build, keine Paketinstallation im Zielimage und kein HAOS-Lauf
  durchgeführt. Die im Dockerfile enthaltenen Laufzeitprüfungen müssen beim
  ersten echten Build noch erfolgreich durchlaufen.
- Kein SDR verfügbar: Funkempfang, tatsächliche ZVEI-Decodierung und
  störungsfreier Parallelbetrieb mit wmbusmeters/Homematic bleiben auf HAOS
  zu prüfen. Bestehende Add-on-Dateien wurden nicht verändert.

Die Build- und Hardware-Prüfschritte stehen in der README. Dies ist kein
Bericht über einen erfolgreich gebauten oder auf dem Pi getesteten Container.
