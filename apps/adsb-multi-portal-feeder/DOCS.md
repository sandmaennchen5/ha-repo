# Home Assistant-Add-on:
# adsb-multi-portal-feeder

Die verfügbaren Optionen orientieren sich an der aktuellen
[Upstream-Dokumentation von Thom-x](https://github.com/Thom-x/docker-fr24feed-piaware-dump1090#configuration).
Explizit dokumentierte Umgebungsvariablen werden in der Home-Assistant-App als
Konfigurationsfelder angeboten. Die von upstream ebenfalls unterstützten frei
definierbaren `FR24FEED_*`- und `PIAWARE_*`-Eigenschaften können nicht dynamisch
als einzelne Home-Assistant-Felder dargestellt werden.

![Bild der Dump1090-Webapp](https://raw.githubusercontent.com/sandmaennchen5/hassio-addons/master/images/screenshot.png)

# Voraussetzungen

- Docker
- RTL-SDR DVBT USB-Dongle (RTL2832)

# Konfiguration

## Sensoren für Home Assistant

### Automatisch hinzugefügte Sensoren

Mit Version `1.27.0` habe ich das tolle Projekt [adsb-hassio-sensors](https://github.com/plo53/adsb-hassio-sensors/tree/master) von [plo53](https://github.com/plo53) integriert.

Dadurch werden Sensoren bereitgestellt, die sich auf den Feeder beziehen, z. B. `sensor.adsbfi_icao`, `sensor.adsbfi_mlat`, `sensor.adsbfi_mode_s`, `sensor.adsbfi_status` für den Adsb.fi-Feeder.

![Assistant ADS-B-Sensoren](https://raw.githubusercontent.com/sandmaennchen5/hassio-addons/main/images/Home%20Assistant%20ADS-B%20sensors.jpg)
![Assistant adsb.fi stats.jpg](https://raw.githubusercontent.com/sandmaennchen5/hassio-addons/main/images/Home%20Assistant%20adsb.fi%20stats.jpg)

### REST-Sensoren

Wenn Sie ansprechende Statistiken wünschen, können Sie einen REST-Sensor mit etwas Template-Magie nutzen, um z. B. die Anzahl der aktuell verfolgten Flugzeuge anzuzeigen:

![Sensor „Verfolgte Flugzeuge“](https://raw.githubusercontent.com/sandmaennchen5/hassio-addons/main/images/sensor_aircraft_tracked.png)

<figure>Beispiel für den Sensor „Verfolgte Flugzeuge“</figure>

Siehe diesen [Beitrag in der Home Assistant Community](https://community.home-assistant.io/t/flightradar24-as-an-add-on/75081).
Ersetzen Sie einfach die IP-Adresse `<raspberry pi>` durch

```yaml
resource: http://f1c878cb-adsb-multi-portal-feeder:8754/monitor.json
```

## Allgemein

Um den Start eines Dienstes zu deaktivieren, können Sie eine Umgebungsvariable hinzufügen:

| Umgebungsvariable | Wert   | Beschreibung | Standardwert |
| ----------------------------------- | ------- | -------------------------- | ------------- |
| `SERVICE_ENABLE_DUMP1090` | `false` | Dump1090-Dienst deaktivieren   | `true` |
| `SERVICE_ENABLE_PIAWARE` | `false` | Piaware-Dienst deaktivieren    | `true` |
| `SERVICE_ENABLE_FR24FEED` | `false` | fr24feed-Dienst deaktivieren   | `true` |
| `SERVICE_ENABLE_HTTP` | `false` | HTTP-Dienst deaktivieren | `true` |
| `SERVICE_ENABLE_IMPORT_OVER_NETCAT` | `false` | Import über Netcat deaktivieren | `false` |
| `SERVICE_ENABLE_ADSBEXCHANGE` | `false` | Adsbexchange-Feed deaktivieren  | `false` |
| `SERVICE_ENABLE_PLANEFINDER` | `false` | Plane-Finder-Feed deaktivieren  | `false` |
| `SERVICE_ENABLE_OPENSKY` | `false` | Opensky-Feeder deaktivieren     | `false` |
| `SERVICE_ENABLE_ADSBFI` | `false` | ADSB.FI-Feed deaktivieren     | `false` |
| `SERVICE_ENABLE_RADARBOX` | `false` | Radarbox-Feed deaktivieren    | `false` |
| `SERVICE_ENABLE_ADSBHUB` | `false` | ADSBHUB-Feeder deaktivieren     | `false` |
| `SERVICE_ENABLE_BIAST` | `false` | BIAST-T-Option deaktivieren     | `false` |


## FlightAware

Registrieren Sie sich auf https://flightaware.com/account/join/.

Wenn der Container startet, sollten Sie die Feeder-ID sehen – notieren Sie diese. Warten Sie 5 Minuten, dann sollte ein neuer Empfänger unter https://fr.flightaware.com/adsb/piaware/claim (verwenden Sie dieselbe IP wie Ihr Docker-Host), beanspruchen Sie ihn und beenden Sie den Container.
Falls nicht, öffnen Sie einfach https://fr.flightaware.com/adsb/piaware/claim/ `Ihre-Feeder-ID`

Fügen Sie die Umgebungsvariable `PIAWARE_FEEDER_DASH_ID` mit Ihrer Feeder-ID hinzu.

| Umgebungsvariable | Konfigurationseigenschaft | Standardwert |
| ---------------------------- | ---------------------- | ------------- |
| `PIAWARE_FEEDER_DASH_ID`     | `feeder-id (erforderlich)` | leer |
| `PIAWARE_RECEIVER_DASH_TYPE` | `receiver-type` | `other` |
| `PIAWARE_RECEIVER_DASH_HOST` | `receiver-host` | `127.0.0.1`   |
| `PIAWARE_RECEIVER_DASH_PORT` | `receiver-port` | `30005` |


## FlightRadar24

| Umgebungsvariable | Konfigurationseigenschaft | Standardwert     |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------- |
| `FR24FEED_RECEIVER` | `receiver` | `beast-tcp` |
| `FR24FEED_FR24KEY` | `fr24key (erforderlich)` | leer |
| `FR24FEED_HOST` | `host` | `127.0.0.1:30005` |
| `FR24FEED_BS` | `bs` | `no` |
| `FR24FEED_RAW` | `raw` | `no` |
| `FR24FEED_LOGMODE` | `logmode` | `1` |
| `FR24FEED_LOGPATH` | `logpath` | `/tmp` |
| `FR24FEED_MLAT` | `mlat` | `no` |
| `FR24FEED_MLAT_DASH_WITHOUT_DASH_GPS` | `mlat-without-gps` | `no` |
| `SYSTEM_FR24FEED_ULIMIT_N` | Dateilimit für den FR24-Feeder; upstream verwendet `-1` ohne Begrenzung. | App-Standard `1024` |

Beispiel: `-e 'FR24FEED_FR24KEY=0123456789'`

## ADS-B Exchange

Fügen Sie die Umgebungsvariable `ADSBEXCHANGE_UUID` mit einer von <https://www.uuidgenerator.net/> generierten UUID hinzu.
Bei mehreren Empfängern verwenden Sie bitte für jeden Empfänger eine andere UUID.

Fügen Sie die Umgebungsvariable `SERVICE_ENABLE_ADSBEXCHANGE` hinzu und setzen Sie sie auf `true`.

| Umgebungsvariable | Beschreibung | Standardwert |
| ----------------------------- | ------------------------- | ------------- |
| `ADSBEXCHANGE_UUID` | UUID (erforderlich) | leer |
| `ADSBEXCHANGE_STATION_NAME`   | Stationsname | leer |
| `ADSBEXCHANGE_MLAT` | mlat | `true` |

Konfigurieren Sie die MLAT-Koordinaten, damit adsbexchange MLAT funktioniert. (siehe eigenen Abschnitt weiter unten)
Wenn Sie Ihre genauen Koordinaten nicht angeben möchten, setzen Sie bitte die Umgebungsvariable `ADSBEXCHANGE_MLAT` auf `false`. (Sie erhalten dann keine MLAT-Ergebnisse und tragen nicht zu MLAT bei)

Fügen Sie die Umgebungsvariable `ADSBEXCHANGE_STATION_NAME` hinzu; sie wird für die MLAT-Karte und den Synchronisationsstatus verwendet.
Sie können überprüfen, ob Ihr MLAT korrekt funktioniert, indem Sie hier nach Ihrem Stationsnamen suchen: <https://map.adsbexchange.com/mlat-map/>
(Die MLAT-Kartenmarkierung wird an ein 5-Meilen-Raster angeordnet und dann zufällig versetzt, um eine Überlappung der Markierungen zu vermeiden. Die genauen Breiten- und Längengrade für MLAT sind bei adsbexchange nicht öffentlich zugänglich.)

Die ADS-B Exchange Anywhere-Karte ist verfügbar unter: <https://www.adsbexchange.com/api/feeders/?feed=MY_UUID>


## adsb.fi

Fügen Sie die Umgebungsvariable `ADSBFI_UUID` mit einer UUID hinzu, die mit `cat /proc/sys/kernel/random/uuid` oder `uuidgen` generiert wurde, falls Sie kein `/proc` haben.


Bei mehreren Empfängern verwenden Sie bitte für jeden Empfänger eine andere UUID.

Fügen Sie die Umgebungsvariable `SERVICE_ENABLE_ADSBFI` hinzu und setzen Sie sie auf `true`.

| Umgebungsvariable | Beschreibung | Standardwert |
| ----------------------------- | ------------------------- | ------------- |
| `ADSBFI_UUID` | UUID (erforderlich) | leer |
| `ADSBFI_STATION_NAME` | Stationsname | leer |
| `ADSBFI_MLAT` | MLAT aktivieren/deaktivieren | `true` |

Konfigurieren Sie die MLAT-Koordinaten, damit adsbfi MLAT funktionieren kann. (siehe eigenen Abschnitt weiter unten)
Wenn Sie Ihre genauen Koordinaten nicht angeben möchten, setzen Sie bitte die Umgebungsvariable `ADSBFI_MLAT` auf `false`. (Sie erhalten dann keine MLAT-Ergebnisse und tragen nicht zu MLAT bei)

Fügen Sie die Umgebungsvariable `ADSBFI_STATION_NAME` hinzu; sie wird für die MLAT-Karte und den Synchronisationsstatus verwendet.
Sie können überprüfen, ob Ihr MLAT korrekt funktioniert, indem Sie hier nach Ihrem Stationsnamen suchen: <https://map.adsbfi.com/mlat-map/>
(Der MLAT-Kartenmarker wird an ein 5-Meilen-Raster angeordnet und dann zufällig versetzt, um eine Überlappung der Marker zu vermeiden; die genauen Breiten- und Längengrade für MLAT sind bei adsbfi nicht öffentlich zugänglich)

Die ADS-B Exchange Anywhere-Karte ist verfügbar unter: <https://www.adsbfi.com/api/feeders/?feed=MY_UUID>


## Genaue Koordinaten für MLAT

Rufen Sie Ihre genauen Koordinaten und die Höhe über dem Meeresspiegel in Metern auf einer dieser Websites ab:

- <https://www.freemaptools.com/elevation-finder.htm>
- <https://www.mapcoordinates.net/en>

Für die Genauigkeit von MLAT ist es wichtig, dass diese nicht um mehr als etwa 10 m / 30 ft abweichen.

| Umgebungsvariable | Beschreibung | Standardwert |
| -------------------------- | ------------------------- | ------------- |
| `MLAT_EXACT_LAT` | Dezimaler Breitengrad | leer |
| `MLAT_EXACT_LON` | Dezimaler Längengrad | leer |
| `MLAT_ALTITUDE_MSL_METERS` | Höhe über MSL in m   | leer |

## Plane Finder

Erstnutzer sollten sich einen PlaneFinder-Freigabecode besorgen.

Um einen PlaneFinder-Freigabecode zu erhalten, starten wir einen temporären Container, auf dem `pfclient` läuft. Dieser durchläuft einen Konfigurationsassistenten und generiert einen Freigabecode.


Sobald der Container gestartet ist, sollte eine Meldung wie die folgende angezeigt werden:

```text
2020-04-11 06:45:25.823307 [-] Wir konnten keine Konfigurationsdatei finden und sind standardmäßig in den Konfigurationsmodus gewechselt. Bitte besuchen Sie: http://172.22.7.12:30053, um die Konfiguration abzuschließen.
```

Öffnen Sie nun einen Webbrowser und rufen Sie <http://dockerhost:30053>. Ersetzen Sie `dockerhost` durch die IP-Adresse Ihres Hosts, auf dem Docker läuft. Sie können die im Protokoll angegebene URL nicht verwenden, da es sich bei der angegebenen IP-Adresse um die private IP des Docker-Containers handelt.

Folgen Sie in Ihrem Browser den Anweisungen des Konfigurationsassistenten. Nach Abschluss des Vorgangs erhalten Sie einen PlaneFinder-Freigabecode. Bewahren Sie diesen an einem sicheren Ort auf.

Sie können den Container nun durch Drücken von `STRG-C` beenden.

Fügen Sie die Umgebungsvariable `SERVICE_ENABLE_PLANEFINDER` hinzu und setzen Sie sie auf `true`.

| Umgebungsvariable | Beschreibung | Standardwert |
| ---------------------------- | --------------------------------- | ------------- |
| `PLANEFINDER_SHARECODE` | generierter Freigabecode (erforderlich)   | leer |
| `PLANEFINDER_INPUT_HOST`     | Eingabe-Host | `127.0.0.1`     |
| `PLANEFINDER_INPUT_PORT`     | Eingabe-Port | `30005` |

Beispiel: `-e 'SERVICE_ENABLE_PLANEFINDER=true' -e 'PLANEFINDER_SHARECODE=65dsfsd56f'`

## Opensky

Erstnutzer sollten sich eine Opensky-Seriennummer besorgen.

Um eine Opensky-Seriennummer zu erhalten, starten wir einen temporären Container mit minimaler Konfiguration, um Opensky zum Laufen zu bringen, wodurch die Seriennummer generiert wird.



Sobald der Container gestartet ist, sollte eine Meldung wie die folgende angezeigt werden:

```text
[opensky-feeder] [INFO] [SERIAL] Neue Seriennummer anfordern
[opensky-feeder] [INFO] [SERIAL] Neue Seriennummer erhalten: -16546546532
```

Notieren Sie sich die Seriennummer und fügen Sie sie für den nächsten Lauf zur Umgebungsvariable `OPENSKY_SERIAL` hinzu.

Sie können den Container nun durch Drücken von `STRG-D` beenden.

Fügen Sie die Umgebungsvariable `SERVICE_ENABLE_OPENSKY` hinzu und setzen Sie sie auf `true`.

| Umgebungsvariable    | Standardwert | Beschreibung |
| ----------------------- | ------------- | --------------------------------------------- |
| `OPENSKY_USERNAME` | leer | Opensky-Benutzername (erforderlich) |
| `OPENSKY_SERIAL` | leer | Generierte Seriennummer (nach dem ersten Lauf erforderlich)   |
| `OPENSKY_DEVICE_TYPE`   | `default`     | Gerätetyp |
| `OPENSKY_INPUT_HOST`    | `127.0.0.1`   | Eingabe-Host |
| `OPENSKY_INPUT_PORT`    | `30005` | Eingabe-Port |
| `HTML_SITE_LAT` | `45.0` | Breitengrad des Empfängers |
| `HTML_SITE_LON` | `9.0` | Empfänger-Längengrad |
| `HTML_SITE_ALT` | `0` | Empfänger-Höhe |

Beispiel: `-e 'SERVICE_ENABLE_OPENSKY=true' -e 'OPENSKY_USERNAME=MyUserName' -e 'OPENSKY_SERIAL=-462168426854'`

## Airnavradar (früher Radarbox)

Erstnutzer sollten sich einen Freigabeschlüssel besorgen.

Um einen Freigabeschlüssel zu erhalten, starten wir einen temporären Container mit minimaler Konfiguration, um Radarbox zum Laufen zu bringen, wodurch der Schlüssel generiert wird.

Sobald der Container gestartet ist, sollte eine Meldung wie die folgende angezeigt werden:

```text
[radarbox-feeder] [2023-06-20 18:51:01]  CPU-Seriennummer leer. Verwenden Sie stattdessen die MAC-Adresse.
[radarbox-feeder] [2023-06-20 18:51:02]  Ihr neuer Schlüssel lautet 35345bf2258aea6b9c7280fbe4467fcd. Bitte speichern Sie diesen Schlüssel für die zukünftige Verwendung. Sie benötigen diesen Schlüssel, um diesen Empfänger mit Ihrem Konto auf RadarBox24.com zu verknüpfen. Dieser Schlüssel wird auch in der Konfigurationsdatei (/etc/rbfeeder.ini) gespeichert
```

Notieren Sie sich die Seriennummer und fügen Sie sie für den nächsten Lauf zur Umgebungsvariablen `RADARBOX_SHARING_KEY` hinzu.

Sie können den Container nun durch Drücken von `STRG-D` beenden.

Fügen Sie die Umgebungsvariable `SERVICE_ENABLE_RADARBOX` hinzu und setzen Sie sie auf `true`.

| Umgebungsvariable    | Standardwert | Beschreibung |
| ----------------------- | ------------- | ------------------------------------------------ |
| `RADARBOX_SHARING_KEY`  | leer | Generierter Freigabeschlüssel (nach dem ersten Lauf erforderlich) |
| `RADARBOX_INPUT_HOST`   | `127.0.0.1`   | Eingabe-Host |
| `RADARBOX_INPUT_PORT`   | `30005` | Eingangsport |
| `RADARBOX_MLAT     `    | `false` | MLAT aktivieren/deaktivieren |
| `HTML_SITE_LAT` | `45.0` | Empfänger-Breitengrad |
| `HTML_SITE_LON` | `9.0` | Empfänger-Längengrad |
| `HTML_SITE_ALT` | `0` | Empfänger-Höhe |

_Hinweis: Dieser Fehler kann unter Windows auftreten: `[radarbox-feeder] /usr/bin/rbfeeder: Zeile 17:   208 Segmentation fault /usr/bin/rbfeeder_armhf "$@"` auf, dafür gibt es keine Lösung._
_Hinweis: Möglicherweise tritt ein Segmentierungsfehler auf; eine Lösung finden Sie unter https://github.com/mikenye/docker-radarbox/issues/9#issuecomment-633068833_
_Hinweis: Möglicherweise erhalten Sie die Fehlermeldung „bereits beansprucht“ für den bereitgestellten Freigabeschlüssel; siehe https://github.com/Thom-x/docker-fr24feed-piaware-dump1090/issues/145_

## Adsbhub

Erstnutzer sollten einen Freigabeschlüssel anfordern.

Um einen Freigabeschlüssel zu erhalten, müssen Sie sich unter https://www.adsbhub.org/ registrieren und unter „Einstellungen“ eine neue Station anlegen. Richten Sie die Station wie folgt ein:

- Stationsmodus: Client
- Feeder-Typ: Linux
- Datenprotokoll: Raw
- Stationshost (IP): Ihre öffentliche IP-Adresse


Fügen Sie die Umgebungsvariable `ADSBHUB_CKEY` hinzu und setzen Sie sie auf den Wert unter „Station dynamic IP update ckey“.
Fügen Sie die Umgebungsvariable `SERVICE_ENABLE_ADSBHUB` hinzu und setzen Sie sie auf `true`.


| Umgebungsvariable    | Standardwert | Beschreibung |
| ----------------------- | ------------- | -------------------------------------------------- |
| `ADSBHUB_CKEY` | leer | Freigabeschlüssel für die Verbindung Ihrer Station mit adsbhub |


## Benutzerdefinierte Eigenschaften hinzufügen

**Hinweis**: Sie können beliebige Eigenschaften zur Konfigurationsdatei von fr24feed oder piaware hinzufügen, indem Sie eine Umgebungsvariable hinzufügen, die mit `PIAWARE_...` oder `FR24FEED_...` beginnt.

Beispiel:

| Umgebungsvariable | Konfigurationseigenschaft | Wert    | Konfigurationsdatei |
| -------------------------------- | ---------------------- | -------- | ------------------ |
| `FR24FEED_TEST=Wert` | `test` | `Wert`  | `fr24feed.init`    |
| `FR24FEED_TEST_DASH_TEST=Wert2` | `test-test` | `Wert2` | `fr24feed.init`    |
| `PIAWARE_TEST=Wert` | `test` | `Wert`  | `piaware.conf`     |

## Dump1090 & Web-UI

| Umgebungsvariable | Standardwert   | Beschreibung |
| ------------------------------------------ | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `HTML_SITE_LAT` | `45.0` | Breitengrad des Empfängers |
| `HTML_SITE_LON` | `9.0` | Längengrad des Empfängers |
| `HTML_SITE_ALT` | `0` | Höhe des Empfängers |
| `HTML_SITE_NAME` | `My Radar Site` | Name des Empfängers |
| `HTML_DEFAULT_TRACKER` | `FlightAware`   | Welche Flugverfolgungs-Website standardmäßig verwendet werden soll. Mögliche Werte sind `FlightAware` oder `Flightradar24` oder `Adsbexchange` oder `Planefinder` oder `OpenskyNetwork` |
| `HTML_RECEIVER_STATS_PAGE_FLIGHTAWARE`     | leer | URL der Statistikseite Ihres Empfängers auf FlightAware. In der Regel https://flightaware.com/adsb/stats/user/ |
| `HTML_RECEIVER_STATS_PAGE_FLIGHTRADAR24`   | leer | URL der Statistikseite Ihres Empfängers auf Flightradar24. Normalerweise https://www.flightradar24.com/account/feed-stats/?id=<ID> |
| `HTML_RECEIVER_STATS_PAGE_ADSBEXCHANGE`    | leer | URL der Statistikseite Ihres Empfängers auf ADS-B Exchange. Normalerweise https://www.adsbexchange.com/api/feeders/?feed=<ID> |
| `HTML_RECEIVER_STATS_PAGE_PLANEFINDER`     | leer | URL der Statistikseite Ihres Empfängers auf PlaneFinder. Normalerweise https://planefinder.net/coverage/receiver/<ID> |
| `HTML_RECEIVER_STATS_PAGE_OPENSKY_NETWORK` | leer | URL der Statistikseite Ihres Empfängers auf Opensky Network. Normalerweise https://opensky-network.org/receiver-profile?s=<ID> |
| `HTML_RECEIVER_STATS_PAGE_RADARBOX` | leer | URL der Statistikseite Ihres Empfängers auf Radarbox. Normalerweise https://www.radarbox.com/stations/<ID> |
| `HTML_RECEIVER_STATS_PAGE_ADSBFI` | leer | URL der Statistikseite Ihres Empfängers auf ADSB.fi. Normalerweise https://adsb.fi/ |
| `HTML_RECEIVER_STATS_PAGE_ADSBHUB` | leer | URL der Statistikseite Ihres Empfängers auf ADSBHub. Normalerweise https://www.adsbhub.org/statistic.php |
| `HTML_FR24_FEEDER_STATUS_PAGE` | leer | URL Ihrer lokalen FR24-Feeder-Statusseite. Normalerweise http://<dockerhost>:8754/ (abhängig vom Port, den Sie beim Starten des Containers angegeben haben) |
| `DUMP1090_ADDITIONAL_ARGS` | leer | Optionale, durch Leerzeichen getrennte Argumente für dump1090. |
| `SYSTEM_HTTP_ULIMIT_N` | App-Standard `1048576` | Dateilimit des HTTP-Dienstes; upstream verwendet standardmäßig `-1`. |

Beispiel: `-e 'HTML_SITE_NAME=Meine Website'`

### Zusätzliche dump1090-Argumente

Die App-Option `DUMP1090_ADDITIONAL_ARGS` reicht zusätzliche Parameter direkt
an dump1090 weiter. Mehrere Parameter werden mit Leerzeichen getrennt.

Häufig verwendete Parameter:

| Parameter | Bedeutung | Beispiel |
| --- | --- | --- |
| `--device-type` | Wählt den SDR-Typ; Standard ist `rtlsdr`. | `--device-type rtlsdr` |
| `--device` | Wählt das Gerät anhand seines Index oder seiner Seriennummer. | `--device 0` oder `--device 00000001` |
| `--enable-agc` | Aktiviert die digitale AGC von dump1090 (nicht die Tuner-AGC). | `--enable-agc` |
| `--gain` | Legt die Verstärkung fest. Der zulässige Bereich hängt vom Empfänger ab. | `--gain 40` |
| `--ppm` | Korrigiert die Frequenzabweichung des Empfängers in PPM. | `--ppm 1` |
| `--freq` | Legt die Empfangsfrequenz in Hertz fest; ADS-B verwendet normalerweise 1090 MHz. | `--freq 1090000000` |
| `--json-location-accuracy` | Legt die Genauigkeit der Standortwerte in den JSON-Ausgaben fest. | `--json-location-accuracy 2` |

Beispiel für mehrere Parameter:

```text
--device 00000001 --gain 40 --ppm 1 --freq 1090000000
```

Die verfügbaren Argumente hängen von der enthaltenen dump1090-Version und ihren
Build-Optionen ab. Maßgeblich ist deshalb immer die Ausgabe von `dump1090 --help`
im App-Protokoll. Die derzeit enthaltene Version `dump1090-fa v10.2` verwendet
für Index und Seriennummer gemeinsam `--device`; `--device-index` und
`--device-serial` werden von ihr nicht unterstützt.

Nicht jeder dump1090-Build unterstützt alle im Internet beschriebenen
Parameter. Bei einem unbekannten Argument beendet sich dump1090 möglicherweise;
in diesem Fall das betreffende Argument entfernen und die App neu starten.

Auf Home Assistant OS ab Hauptversion 16 werden `SYSTEM_HTTP_ULIMIT_N` und
`SYSTEM_FR24FEED_ULIMIT_N` aus Kompatibilitätsgründen nicht an den Container
weitergereicht. Die Felder sind für ältere HA-OS-Versionen weiterhin vorhanden.

## DUMP1090-Weiterleitung

| Umgebungsvariable | Standardwert | Beschreibung |
| ----------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------- |
| `SERVICE_ENABLE_IMPORT_OVER_NETCAT` | `false` | Aktiviert die Netcat-Weiterleitung der Beast-Ausgabe eines entfernten Dump1090-Servers an den lokalen Dump1090-Beast-Eingang |
| `DUMP1090_LOCAL_PORT` | leer | Muss derselbe Port sein, der als `--net-bi-port` in `DUMP1090_ADDITIONAL_ARGS` angegeben ist |
| `DUMP1090_REMOTE_HOST` | leer | IP-Adresse des entfernten dump1090-Servers |
| `DUMP1090_REMOTE_PORT` | leer | Port des Remote-Dump190-Servers, der auf dem Remote-System als Argument `--net-bo-port` angegeben wurde |

## RTL_TCP-Weiterleitung

**WARNUNG:** Diese Art der Weiterleitung beansprucht viel Bandbreite und kann in WLAN-Umgebungen instabil sein.

| Umgebungsvariable  | Standardwert | Beschreibung |
| --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RTL_TCP_OVER_NETCAT` | `false` | Verwende dump1090 in Kombination mit netcat, um Daten vom rtl_tcp-Server zu übertragen. (Erfordert ca. 35–40 Mbit/s). Beispiel für einen RTL_TCP-Befehl: `./rtl_tcp -a 0.0.0.0 -f 1090000000 -s 2400000 -p 30005 -P 28 -g -10` |
| `RTL_TCP_REMOTE_HOST` | leer | IP-Adresse des rtl_tcp-Servers |
| `RTL_TCP_REMOTE_PORT` | leer | Port des rtl_tcp-Servers |

## BIAS-T-Option

Sie können die BIAS-T-Option für das RTL-SDR-Gerät aktivieren, indem Sie die Umgebungsvariable `SERVICE_ENABLE_BIAST` auf `true` setzen. Dadurch wird die Bias-Tee-Stromversorgung auf dem RTL-SDR-Gerät aktiviert, was für die Stromversorgung externer LNA-Geräte (Low Noise Amplifier) nützlich ist.
Es wird der Befehl `rtl_biast -b 1` ausgeführt, um die Bias-T-Option zu aktivieren.

| Umgebungsvariable   | Standardwert | Beschreibung |
|------------------------|---------------|------------------------------------------|
| `SERVICE_ENABLE_BIAST` | `false` | Aktiviert die Bias-T-Option für das RTL-SDR-Gerät. |
| `BIAST_ARGS` | `-b 1` | Argumente für Bias-T |

## Geländegrenzenringe (optional):

Wenn Sie diese Funktion nicht benötigen, ignorieren Sie diesen Abschnitt.

Erstellen Sie auf http://www.heywhatsthat.com ein Panorama für den Standort Ihres Empfängers.

| Umgebungsvariable | Standardwert | Beschreibung |
| -------------------- | ------------- | ------------------------------------------ |
| `PANORAMA_ID` | leer | Panorama-ID |
| `PANORAMA_ALTS` | `1000,10000`  | Durch Kommas getrennte Liste der Höhen in Metern |

_Hinweis: Der Wert der Panorama-ID entspricht der URL oben auf der Panorama-http://www.heywhatsthat.com/?view=XXXX. Höhenangaben sind in Metern angegeben. Sie können eine Liste von Höhenangaben angeben._

Beispiel: `-e 'PANORAMA_ID=FRUXK2G7'`

Wenn Sie die Daten nicht jedes Mal neu herunterladen möchten, wenn Sie den Container starten, können Sie die Datei `http://www.heywhatsthat.com/api/upintheair.json?id=${PANORAMA_ID}&refraction=0.25&alts=${PANORAMA_ALTS}` als upintheair.json herunterladen und unter `/usr/lib/fr24/public_html/upintheair.json` einbinden.

## Open Weather Map-Ebenen:

Wenn Sie diese Funktion nicht benötigen, ignorieren Sie diesen Abschnitt.

Wenn Sie einen API-Schlüssel angeben, stehen OWM-Ebenen zur Verfügung.
Erstellen Sie ein Konto und erhalten Sie einen API-Schlüssel unter https://home.openweathermap.org/users/sign_up.
Beachten Sie, dass OWM eine kostenlose Testversion für seine API anbietet; nach einer gewissen Zeit müssen Sie jedoch bezahlen.
Siehe: https://openweathermap.org/price

| Umgebungsvariable | Standardwert | Beschreibung |
| -------------------- | ------------- | ------------------------ |
| `LAYERS_OWM_API_KEY` | leer | Open Weather Map API-Schlüssel |


## Installation

- Falls noch nicht geschehen, fügen Sie das Add-on-Repository hinzu ([siehe](https://github.com/sandmaennchen5/homeassistant-addons#installation))
- Wenn Sie Daten an FlightRadar24 und/oder FlightAware und/oder ADSBexchange und/oder Plane Finder weitergeben möchten, generieren Sie die erforderlichen Schlüssel ([siehe unten](https://github.com/sandmaennchen5/hassio-addons/tree/main/adsb-multi-portal-feeder#flightaware-feeder-id--flightrader24-key--adsbexchange-uuid))
- Wenn Sie das dump1090-Webinterface (wie im Screenshot oben) nutzen möchten müssen Sie die Längen- und Breitengrade für Ihren Standort einstellen ([siehe unten](https://github.com/sandmaennchen5/hassio-addons/tree/main/adsb-multi-portal-feeder#latitude--longitude))

## Konfiguration

Die gesamte Konfiguration soll ähnlich wie das ursprüngliche Docker-Image funktionieren.
Weitere Informationen findest du unter [docker-fr24feed-piaware-dump1090](https://github.com/Thom-x/docker-fr24feed-piaware-dump1090).

Ich habe den (vermutlich) am häufigsten verwendeten Workflow vorgefertigt: Sende Daten vom USB-ADS-B-Stick an FlightRadar24, FlightAware, ADSBexchange und Plane Finder und erhalte eine nette kleine webbasierte Übersicht als Home Assistant-Menüeintrag.

Es ist möglich, die Standortinformationen von Home Assistant selbst abzurufen und zu verwenden, indem man einige „magische“ Variablen nutzt, die automatisch ersetzt werden:

- `HOMEASSISTANT_LATITUDE`
- `HOMEASSISTANT_LONGITUDE`
- `HOMEASSISTANT_ELEVATION`

Wenn Sie etwas anderes hinzufügen möchten, fügen Sie einfach die entsprechende Umgebungsvariable als Konfigurationsoption hinzu.
Möglicherweise müssen Sie auf die drei kleinen Punkte in der oberen rechten Ecke klicken und `In YAML bearbeiten` auswählen.

Beispiel: Sie möchten den Standard-Tracker auf der HTML-Seite von FlightAware zu Flightradar24 ändern?

```json
...
HTML_DEFAULT_TRACKER: 'Flightradar24'
...
```

### Breitengrad / Längengrad

Sie können

- Google Maps dafür nutzen: Gehen Sie auf https://www.google.com/maps/ und klicken Sie einfach mit der rechten Maustaste auf Ihr Haus. Die Breiten- und Längengrade sollten angezeigt werden
- die Daten über eine Website ermitteln: https://latitudelongitude.org/

## Zugriff auf WebIF


- Dieses Add-On bietet Zugriffsfunktionen auf eine ansprechende Karte mit empfangenen Daten.
  Aktiviere einfach die Funktion _In Seitenleiste anzeigen_ oder greife über die Schaltfläche _OPEN WEB UI_ darauf zu.
- fr24feed (der Feeder von FlightRadar24) stellt einige Statistiken an seinem internen Port 8754 bereit.
  Um darauf zuzugreifen, fügen Sie im Reiter „Konfiguration“ unter „Netzwerk“ einen externen Port wie folgt hinzu:
  ![network](https://raw.githubusercontent.com/sandmaennchen5/hassio-addons/main/images/port-8754.png)
  ![fr24stats](https://raw.githubusercontent.com/sandmaennchen5/hassio-addons/main/images/flightradar24-stats.png)

## Daten, Backups und Migration

Beachten Sie für persistente Daten, Home-Assistant-Backups, Speicherorte und manuelle Wiederherstellung die gemeinsame Anleitung [Speicherorte und Datenmigration](../../docs/app-storage-and-migration.md). App-spezifische Import-/Export-Optionen sind in den vorherigen Abschnitten beschrieben.

## Sicherheit

Aktivieren Sie nur benötigte Funktionen und Ports. Zugangsdaten gehören ausschließlich in die App-Konfiguration und nicht in Protokolle oder zusätzliche Befehlsargumente. Die tatsächlich benötigten Berechtigungen stehen in der jeweiligen config.yaml.

## Bekannte Probleme und Einschränkungen

Bei Problemen zuerst das App-Protokoll, die Erreichbarkeit des Upstream-Dienstes und die konfigurierten Ports prüfen. Architektur- und Upstream-Einschränkungen gelten entsprechend der verlinkten Herstellerdokumentation.

## Support

- App-Integration: [Issues im Home-Assistant-App-Repository](https://github.com/sandmaennchen5/ha-repo/issues)
- Programmfunktion: [Upstream-Projekt](https://github.com/sandmaennchen5/ha-repo)
