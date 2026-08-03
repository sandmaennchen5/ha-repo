# Speicherorte und Datenmigration für Home-Assistant-Apps

Home-Assistant-Apps können Daten an mehreren Orten ablegen. Der Speicherort
bestimmt, ob Daten mit der App gesichert werden, an ihren Slug gebunden sind
und bei einer Deinstallation erhalten bleiben.

> Bevor Daten manuell kopiert werden, ein aktuelles Backup erstellen und alle
> beteiligten Apps stoppen. Vorhandene Zieldaten niemals ungeprüft
> überschreiben.

## Speicherorte im Überblick

| Pfad im Container | Typischer Pfad auf HA OS | App-Backup | Slug-unabhängig | Verwendung |
|---|---|---:|---:|---|
| `/data` | `/mnt/data/supervisor/apps/data/<slug>` | Ja | Nein | Interne Laufzeitdaten |
| `/config` mit `addon_config` | `/mnt/data/supervisor/app_configs/<slug>` | Ja | Nein | Sichtbare App-Konfiguration |
| `/share/<name>` | `/mnt/data/supervisor/share/<name>` | Nur bei Auswahl von Share | Ja | Gemeinsame Daten und Exporte |
| `/homeassistant/<pfad>` | `/mnt/data/supervisor/homeassistant/<pfad>` | Mit Home Assistant | Ja | Nur bei notwendigem HA-Konfigurationszugriff |
| `/media/<name>` | `/mnt/data/supervisor/media/<name>` | Nur bei Auswahl von Media | Ja | Audio, Video und Bilder |
| Container-Dateisystem | Container-Layer | Nein | Nein | Nicht für dauerhafte Daten |

Die Host-Pfade sind Implementierungsdetails von Home Assistant OS. Apps sollten
innerhalb ihres Containers ausschließlich die vorgesehenen eingebundenen Pfade
verwenden.

## `/data`: interne App-Daten

`/data` ist automatisch vorhanden und schreibbar; ein Eintrag unter `map` ist
nicht erforderlich. Hier liegt auch `/data/options.json` mit den vom Supervisor
verwalteten App-Optionen.

Geeignet für:

- interne Datenbanken und Zustände;
- automatisch erzeugte Dateien;
- Daten, die Benutzer nicht direkt bearbeiten müssen.

`/data` wird mit dem App-Backup gesichert und bleibt bei normalen Updates
erhalten. Der Ordner ist jedoch an den vollständigen Repository- und App-Slug
gebunden. Eine STS-, LTS-, DEV- oder umbenannte Variante erhält deshalb ein
eigenes Verzeichnis.

## `/config`: sichtbare App-Konfiguration

Aktuelle Schreibzuordnung in `config.yaml`:

```yaml
map:
  - type: addon_config
    read_only: false
```

Der Supervisor bindet den app-spezifischen Ordner innerhalb des Containers als
`/config` ein. Auf Home Assistant ist er über `/addon_configs/<slug>`
zugänglich.

Geeignet für:

- editierbare Konfigurationsdateien;
- Zertifikate und Vorlagen;
- Diagnoseausgaben;
- Daten, die zusammen mit der App gesichert werden sollen.

Der Ordner wird gemeinsam mit der ausgewählten App gesichert. Er ist ebenfalls
slug-gebunden. Bei der Deinstallation kann Home Assistant anbieten, diese
öffentlichen App-Daten ebenfalls zu entfernen.

## `/share`: gemeinsamer Speicher

Schreibzuordnung:

```yaml
map:
  - type: share
    read_only: false
```

Ein fester Unterordner wie `/share/portainer` oder
`/share/homey-shs-config` ist unabhängig vom App-Slug. Dadurch können
unterschiedliche Varianten nach einem kontrollierten Wechsel auf denselben
Speicherort zugreifen.

Vorteile:

- bleibt bei App-Deinstallation erhalten;
- funktioniert über Slug- und Repository-Wechsel hinweg;
- benötigt keinen Zugriff auf Home Assistants Konfigurationsverzeichnis.

Zu beachten:

- `/share` gehört nicht automatisch zum Teilbackup einer einzelnen App;
- bei manuellen oder automatischen Backups muss der Ordner **Share**
  eingeschlossen werden;
- andere Apps mit Share-Zugriff können diese Daten ebenfalls lesen;
- zwei App-Instanzen dürfen denselben beschreibbaren Datenbestand nicht
  gleichzeitig verwenden.

## `/homeassistant`: Home-Assistant-Konfiguration

```yaml
map:
  - type: homeassistant_config
    read_only: false
```

Diese Zuordnung stellt Home Assistants gesamtes Konfigurationsverzeichnis im
Container unter `/homeassistant` bereit. Ein darin angelegter Unterordner ist
slug-unabhängig und wird mit Home Assistant gesichert.

Für reine Persistenz sollte diese Variante nicht verwendet werden: Die App
erhält damit Zugriff auf sensible Home-Assistant-Konfigurationen und
Zugangsdaten. `/share` oder `addon_config` sind enger begrenzt.

## `/media` und Container-Dateisystem

`/media` ist für Medieninhalte vorgesehen, nicht für Datenbanken oder
App-Konfigurationen. Daten außerhalb von `/data` und den explizit eingebundenen
Verzeichnissen liegen nur im Container-Layer. Sie sind nicht zuverlässig
persistent und können bei Update oder Deinstallation verloren gehen.

## Welche Daten enthält welches Backup?

| Backup-Auswahl | `/data` | App-`/config` | `/share` | `/homeassistant` |
|---|---:|---:|---:|---:|
| Vollständiges Backup mit allen Ordnern | Ja | Ja | Ja | Ja |
| Teilbackup mit ausgewählter App | Ja | Ja | Nein | Nein |
| Teilbackup mit ausgewähltem Ordner Share | Nein | Nein | Ja | Nein |
| Home Assistant ausgewählt | Nein | Nein | Nein | Ja |

Bei automatischen Backups gelten dieselben Regeln: Entscheidend ist, welche
Apps und Ordner in der Backup-Konfiguration ausgewählt wurden.

## Empfohlene Speicherwahl

| Anforderung | Empfehlung |
|---|---|
| Interne, nicht editierbare App-Daten | `/data` |
| Sichtbare Konfiguration mit App-Backup | `/config` über `addon_config` |
| Wechsel zwischen Editionen, Kanälen oder Slugs | Eigener Ordner unter `/share` |
| Medieninhalte | `/media` |
| Tatsächlicher Zugriff auf Home-Assistant-Dateien erforderlich | `/homeassistant` |

Eine App kann beispielsweise zwischen app-spezifischem und gemeinsamem
Speicher wählen:

```yaml
options:
  storage_mode: app

schema:
  storage_mode: "list(app|shared)"

map:
  - type: addon_config
    read_only: false
  - type: share
    read_only: false
```

Zuordnung:

```text
app     -> /config
shared  -> /share/<fester-name>
```

Beim Wechsel sollte eine App zuerst Quelle und Ziel prüfen, nur in ein leeres
Ziel kopieren und die Quelle erst nach erfolgreicher Prüfung entfernen. Die
Datei `/data/options.json` bleibt immer unter `/data`.

## Daten migrieren

### Bevorzugter Weg: Import und Export der App

Wenn die App eigene Import- und Exportoptionen anbietet, sollten diese
verwendet werden. Sie können laufende Dienste geordnet stoppen, Archive prüfen,
Versionen vergleichen und `/data/options.json` korrekt behandeln.

Für die Apps in diesem Repository gilt grundsätzlich:

1. Export beim Stoppen aktivieren.
2. Quell-App stoppen und den erfolgreichen Export im Protokoll prüfen.
3. Ziel-App auf den gewünschten Speicherort konfigurieren.
4. Automatischen oder manuellen Import auswählen.
5. Ziel-App starten und Funktion sowie Datenbestand prüfen.
6. Quell-App erst nach einem erfolgreichen Backup entfernen.

### Manuelle Migration über Advanced SSH & Web Terminal

Diese Methode benötigt Zugriff auf die Docker-API und einen deaktivierten
Schutzmodus der Terminal-App. Diese Rechte nur für die Migration verwenden.

#### 1. Container und Slug ermitteln

```bash
docker ps -a \
  --format 'Name={{.Names}}  Slug={{.Label "io.hass.slug"}}'
```

Beispiel:

```text
Name=addon_0897ef1c_portainer-agent-sts
Slug=0897ef1c_portainer-agent-sts
```

#### 2. Quell- und Ziel-App stoppen

```bash
ha apps stop 0897ef1c_portainer-agent-sts
ha apps stop 0897ef1c_portainer-agent-lts
```

Nur vorhandene Apps angeben. Der Zustand lässt sich kontrollieren mit:

```bash
ha apps info 0897ef1c_portainer-agent-sts
```

#### 3. Daten zunächst in einen leeren temporären Share-Ordner kopieren

```bash
mkdir -p /share/app-migration/portainer-agent-sts

docker cp \
  addon_0897ef1c_portainer-agent-sts:/data/. \
  /share/app-migration/portainer-agent-sts/
```

`options.json` darf nicht als Anwendungsdatenbestand übernommen werden:

```bash
rm -f /share/app-migration/portainer-agent-sts/options.json
```

Danach Inhalt und Dateirechte prüfen:

```bash
find /share/app-migration/portainer-agent-sts -mindepth 1
```

Von dort können die geprüften Daten in den vorgesehenen `/share`- oder
`/addon_configs`-Ordner kopiert werden. Existiert das Ziel bereits und enthält
Daten, zuerst ein separates Backup davon erstellen.

> `docker exec` funktioniert nur bei laufenden Containern. Für eine konsistente
> Migration bleibt die Quell-App gestoppt; zum Lesen wird `docker cp`
> verwendet.

### Manuelle Migration über HAOS-Host-SSH

Der SSH-Zugang auf Port `22222` gewährt vollständigen Root-Zugriff auf Home
Assistant OS und ist für Entwickler und Wiederherstellungsfälle vorgesehen.
Für normale Migrationen ist der app-eigene Export vorzuziehen.

#### SSH-Zugang offiziell aktivieren

1. Einen USB-Datenträger als FAT, ext4 oder NTFS formatieren.
2. Die Partition exakt `CONFIG` nennen.
3. Im Stammverzeichnis eine Datei `authorized_keys` ohne Endung anlegen.
4. Nur den öffentlichen SSH-Schlüssel eintragen. Die Datei muss LF-Zeilenenden
   verwenden.
5. Den Datenträger anschließen und `ha os import` ausführen oder HA OS mit
   angeschlossenem Datenträger neu starten.

Beispiel für einen Schlüssel unter Windows:

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\haos_ed25519"
Get-Content "$env:USERPROFILE\.ssh\haos_ed25519.pub"
```

Verbindung:

```powershell
ssh -i "$env:USERPROFILE\.ssh\haos_ed25519" `
  -p 22222 `
  root@HOME-ASSISTANT-IP
```

#### Beispiel: `/data` nach `/share` kopieren

```bash
ha apps stop 0897ef1c_portainer-agent-sts

mkdir -p /mnt/data/supervisor/share/portainer-agent

cp -a \
  /mnt/data/supervisor/apps/data/0897ef1c_portainer-agent-sts/. \
  /mnt/data/supervisor/share/portainer-agent/

rm -f \
  /mnt/data/supervisor/share/portainer-agent/options.json
```

#### Beispiel: `/data` nach App-`/config` kopieren

```bash
ha apps stop 0897ef1c_portainer-agent-sts

mkdir -p \
  /mnt/data/supervisor/app_configs/0897ef1c_portainer-agent-sts

cp -a \
  /mnt/data/supervisor/apps/data/0897ef1c_portainer-agent-sts/. \
  /mnt/data/supervisor/app_configs/0897ef1c_portainer-agent-sts/

rm -f \
  /mnt/data/supervisor/app_configs/0897ef1c_portainer-agent-sts/options.json
```

#### Kopie prüfen

```bash
find \
  /mnt/data/supervisor/apps/data/0897ef1c_portainer-agent-sts \
  -mindepth 1 ! -name options.json |
wc -l

find \
  /mnt/data/supervisor/share/portainer-agent \
  -mindepth 1 |
wc -l
```

Die Anzahl ist nur eine erste Plausibilitätsprüfung. Anschließend die Ziel-App
starten, ihr Protokoll kontrollieren und die tatsächliche Funktion testen.

## Sicherheitsregeln

- Vor direktem Zugriff ein vollständiges Backup erstellen.
- Quell- und Ziel-App vor dem Kopieren stoppen.
- Zuerst kopieren, niemals direkt verschieben.
- Nur in ein leeres oder zuvor gesichertes Ziel schreiben.
- `/data/options.json` nicht als Nutzdaten migrieren.
- Private SSH-Schlüssel niemals in App-Optionen eintragen.
- Host-SSH nur in einem vertrauenswürdigen lokalen Netzwerk aktivieren.
- Schutzmodus nur so lange wie erforderlich deaktivieren.
- Quelldaten erst nach Funktionsprüfung und neuem Backup löschen.

## Weiterführende Dokumentation

- [Home-Assistant-App-Konfiguration](https://developers.home-assistant.io/docs/apps/configuration/)
- [Öffentliche App-Konfiguration mit `addon_config`](https://developers.home-assistant.io/blog/2023/11/06/public-addon-config/)
- [Backups erstellen und Inhalte auswählen](https://www.home-assistant.io/common-tasks/general/#backups)
- [Offizieller HAOS-Debug-SSH-Zugang](https://developers.home-assistant.io/docs/operating-system/debugging/)
