# Workflows

## `hasos_app.yml` – App Builder

**Trigger:** Pull Request oder Push auf `main` bei Änderungen an App-Konfiguration, Dockerfile oder `rootfs`; außerdem manuell.

- Erkennt betroffene Apps automatisch.
- Baut Images für alle in `config.yaml` angegebenen Architekturen.
- Veröffentlicht Images bei Push-Läufen und bei manuellen Läufen mit `publish: true`.
- Ermittelt danach die komprimierte Layer-Größe aus dem Registry-Manifest und aktualisiert `image_size` automatisch.
- Verwendet den wiederverwendbaren Workflow `build-app.yaml`.

## `update-apps.yaml` – automatische App-Aktualisierung

**Trigger:** Täglich um 04:00 UTC oder manuell.

- Der tägliche Lauf berücksichtigt Apps mit `config.yaml`, `.var.yaml`, einer unterstützten Quelle und `autoupdater: true`.
- Beim manuellen Lauf wählt das Feld `app` ausdrücklich `all` oder einen einzelnen App-Slug für die Versionsprüfung aus.
- Die Option `rebuild_all` veröffentlicht anschließend alle buildbaren Apps erneut, auch wenn im Feld `app` nur eine einzelne App geprüft wurde oder keine neue Upstream-Version vorliegt.
- Die Option `bump_app_revision` erhöht nach der Versionsprüfung die Home-Assistant-App-Revision um eins und ergänzt den Changelog.
- `bump_app_revision` gilt für die im Feld `app` ausgewählte Prüfauswahl; `rebuild_all` beeinflusst diese Auswahl nicht.
- Neuaufbauten laufen als Build-Matrix innerhalb desselben `Update Apps`-Laufs; es werden keine separaten `HA App Creater`-Workflow-Läufe pro App gestartet.
- Unterstützt GitHub-Releases über `github.com/<owner>/<repo>`.
- Unterstützt Docker Hub über `docker.io/<namespace>/<image>`.
- Aktualisiert `version`, `upstream_version`, `upstream_commit`, `updated` und `source`.
- Stellt neue Release Notes in `CHANGELOG.md` voran.
- Validiert die App-YAML-Dateien und committet Änderungen automatisch.
- Startet anschließend die wiederverwendbaren App-Builds als Matrix innerhalb desselben Workflow-Laufs.

Bei Docker Hub wird bevorzugt der semantische Tag verwendet, dessen Digest dem Tag `latest` entspricht. Falls kein solcher Tag existiert, wird der höchste stabile semantische Versions-Tag verwendet. `upstream_commit` enthält bei Docker-Quellen den Image-Digest.

## `manual-app-update.yaml` – manuelle App-Metadaten

**Trigger:** Ausschließlich manuell.

- Dient Apps, deren Upstream-Daten nicht automatisch ermittelt werden können.
- Erwartet App-Slug, semantische Version und Aktualisierungsdatum als Pflichtfelder.
- Commit beziehungsweise Image-Digest, Quelle und Release Notes können zusätzlich angegeben werden.
- Leere optionale Werte für Commit/Digest und Quelle behalten den bisherigen Wert.
- Aktualisiert `version` in `config.yaml` sowie `upstream_version`, `upstream_commit`, `updated` und `source` in `.var.yaml`.
- Stellt einen manuellen Eintrag in `CHANGELOG.md` voran.
- Validiert YAML, committet und pusht die Änderungen.
- Startet anschließend `hasos_app.yml` mit `publish: true` für die ausgewählte App.

## `update_readme.yml` – README Badge-Generator

**Trigger:** Push auf `main` bei Änderungen an App-Metadaten, Badge-Konfiguration oder Generator-Skripten; außerdem manuell.

- Generiert Badges aus `config.yaml` und `.var.yaml`.
- Aktualisiert die Bereiche zwischen den `APPS-LIST`- beziehungsweise `BADGES`-Markern.
- Committet geänderte deutsche README-Dateien automatisch.

## `generate_dashboard.yml` – Dashboard-Generator

**Trigger:** Nach Abschluss von `Update README Badges`, bei Änderungen an Dashboard-Dateien oder manuell.

- Generiert Dashboard, Health-Daten und einen History-Snapshot.
- Veröffentlicht `.dashboard/` als `dashboard`-Branch für GitHub Pages.

## `badge-lint.yml` – Badge- und Schema-Validierung

**Trigger:** Pull Request, passende Pushes auf `main` oder manuell.

- Validiert `.github/config.yaml`, `apps/*/config.yaml` und `apps/*/.var.yaml`.
- Führt den Health-Check aus.

## `yaml-lint.yaml` – YAML-Lint

**Trigger:** Push auf `main`, täglich um 04:00 UTC oder manuell.

Verwendet `.github/.yamllint`.

## `docker-lint.yaml` – Dockerfile-Lint

**Trigger:** Push auf `main` bei Dockerfile-Änderungen, täglich um 04:00 UTC oder manuell.

Verwendet `.github/.hadolint.yaml`.

## `auto-translate.yml` – Übersetzungen

**Trigger:** Push auf `main` oder `master`; außerdem manuell.

- Übersetzt `README.md` nach `README.en.md` und `DOCS.md` nach `DOCS.en.md`.
- Übersetzt `translations/de.yaml`, `de.yml` und `de.json` in die entsprechenden englischen Dateien.
- Verwendet bevorzugt DeepL, wenn `DEEPL_API_KEY` vorhanden und verwendbar ist.
- Fällt ohne Key oder bei DeepL-Fehlern auf Google Translate über `deep-translator` zurück.
- Nutzt `.github/translation-state.json`, um unveränderte Quellen zu überspringen.
- Committet und pusht geänderte Übersetzungen direkt.

Der No-Key-Fallback ist ein inoffizieller Zugriff und kann durch externe Rate-Limits eingeschränkt werden.

## `update-workflow-options.yaml` – manuelle App-Liste

**Trigger:** Push auf `main` bei Änderungen unter `apps/`; außerdem manuell.

Aktualisiert die App-Auswahl in `hasos_app.yml` und `update-apps.yaml` und benötigt das Secret `WORKFLOW_PAT`, um Workflow-Dateien zu committen.
