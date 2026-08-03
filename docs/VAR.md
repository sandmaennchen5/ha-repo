# `.var.yaml`-Referenz

Die Datei `apps/<app>/.var.yaml` enthält Repository-Metadaten, die nicht Teil der Home-Assistant-App-Konfiguration sind.

## Beispiel

```yaml
hidden: false
icon: "🛰️"
stage: "stable"

hide_root_readme: false
hide_app_readme: false
hide_badges: []
hide_groups: []

badge_overrides: {}
group_overrides: {}

upstream_version: "1.2.3"
upstream_repo: "github.com/owner/repository"
upstream_commit: "abc1234"
autoupdater: true

build: "passing"
lint: "passing"
yaml_lint: "passing"
code_quality: "A"
image_size: "45MB"

custom_shield: ""
custom_flag: ""

updated: "2026-07-22"
source: "github.com/owner/repository"
```

## Felder

| Feld | Typ | Beschreibung |
|---|---|---|
| `hidden` | bool | App allgemein ausblenden |
| `icon` | string | Symbol für Listen und Dashboard |
| `stage` | string | `stable`, `beta`, `lab` oder leer |
| `hide_root_readme` | bool | App aus der Haupt-README ausblenden |
| `hide_app_readme` | bool | Badge-Aktualisierung der App-README deaktivieren |
| `hide_badges` | list | Einzelne Badge-IDs ausblenden |
| `hide_groups` | list | Komplette Badge-Gruppen ausblenden |
| `badge_overrides` | object | Darstellung einzelner Badges überschreiben |
| `group_overrides` | object | Darstellung ganzer Badge-Gruppen überschreiben |
| `upstream_version` | string | Zuletzt ermittelte Upstream-Version |
| `upstream_repo` | string | Primäre Quelle für den Autoupdater |
| `upstream_commit` | string | Git-Commit oder Docker-Image-Digest |
| `autoupdater` | bool | App beim täglichen Updater-Lauf berücksichtigen |
| `build` | string | Build-Status für Badges |
| `lint` | string | Lint-Status für Badges |
| `yaml_lint` | string | YAML-Lint-Status für Badges |
| `code_quality` | string | Code-Qualitätswert |
| `image_size` | string | Automatisch ermittelte komprimierte Größe der größten Plattformvariante |
| `custom_shield` | string | Benutzerdefinierte shields.io-URL |
| `custom_flag` | string | Benutzerdefinierter Badge-Wert |
| `updated` | string | Upstream-Aktualisierungsdatum als `YYYY-MM-DD` |
| `source` | string | Quelle; dient als Fallback, wenn `upstream_repo` leer ist |

## Unterstützte Upstream-Quellen

GitHub:

```yaml
upstream_repo: "github.com/fosrl/newt"
```

Docker Hub:

```yaml
upstream_repo: "docker.io/fosrl/newt"
upstream_repo: "docker.io/library/alpine"
```

`upstream_repo` hat Vorrang vor `source`. Beim täglichen Lauf muss zusätzlich `autoupdater: true` gesetzt sein. Ein manueller Lauf kann unterstützte Apps auch ohne dieses Flag verarbeiten.
