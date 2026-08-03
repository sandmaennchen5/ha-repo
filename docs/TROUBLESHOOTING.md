# Troubleshooting

## Badges werden nicht aktualisiert

1. Prüfe die Marker `<!-- BADGES-START -->` und `<!-- BADGES-END -->` beziehungsweise `APPS-LIST`.
2. Starte `update_readme.yml` manuell.
3. Prüfe die Logs des Workflows.

Lokal:

```bash
pip install pyyaml
python .github/scripts/readme_generator.py
```

## Schema-Validierungsfehler

```bash
pip install pyyaml jsonschema
python .github/scripts/schema_validator.py
```

Prüfe insbesondere Pflichtfelder, Datentypen und unbekannte Felder.

## Health-Check-Warnungen

```bash
pip install pyyaml
python .github/scripts/health_check.py
```

## Dashboard wird nicht generiert

1. Prüfe `generate_dashboard.yml` und den vorausgehenden Workflow `Update README Badges`.
2. Prüfe, ob GitHub Pages den Branch `dashboard` veröffentlicht.
3. Starte `generate_dashboard.yml` bei Bedarf manuell.

## App wird nicht gebaut

1. Prüfe `apps/<slug>/config.yaml`, `Dockerfile` und `rootfs`.
2. Kontrolliere die in `arch` angegebenen Architekturen.
3. Bei automatischen Versionsupdates muss der explizite Dispatch von `hasos_app.yml` erfolgreich sein.
4. Bei manuellen Builds muss `publish: true` gesetzt sein, wenn ein Image veröffentlicht werden soll.

## App wird nicht automatisch aktualisiert

- `config.yaml` und `.var.yaml` müssen vorhanden und gültig sein.
- `.var.yaml` benötigt `autoupdater: true` für tägliche Läufe.
- `upstream_repo` oder ersatzweise `source` muss eine unterstützte GitHub- oder Docker-Hub-Quelle enthalten.
- GitHub erwartet `github.com/<owner>/<repo>`.
- Docker Hub erwartet `docker.io/<namespace>/<image>`.
- Prüfe die `AUTO`- und `SKIP`-Einträge im Step Summary von `update-apps.yaml`.

## Übersetzungen funktionieren nicht

- Unterstützte Quellen heißen exakt `README.md`, `DOCS.md`, `translations/de.yaml`, `de.yml` oder `de.json`.
- Ziel ist aktuell Englisch.
- Mit `DEEPL_API_KEY` wird DeepL bevorzugt. HTTP 456 bedeutet, dass das DeepL-Kontingent aufgebraucht ist.
- Ohne verwendbares DeepL fällt das Skript auf Google Translate über `deep-translator` zurück.
- Der No-Key-Fallback benötigt Internetzugriff und kann externen Rate-Limits unterliegen.
- `.github/translation-state.json` speichert Quelltext-Hashes. Lösche einen Eintrag nur, wenn eine unveränderte Quelle bewusst neu übersetzt werden soll.

## YAML- oder Docker-Lint verwendet falsche Konfiguration

- YAML-Lint: `.github/.yamllint`
- Hadolint: `.github/.hadolint.yaml`
