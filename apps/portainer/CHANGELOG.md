# Changelog


## [2026.8.3] - 2026-08-27

### Enthaltene Upstream-Versionen

- LTS: `CE 2.45.0, EE 2.45.0`
- STS: `CE 2.45.0, EE 2.45.0`

### Änderungen

- LTS: `2.39.6` → `2.45.0`
- STS: `2.44.0` → `2.45.0`
- EE LTS: `2.39.6` → `2.45.0`
- EE STS: `2.44.0` → `2.45.0`

---

## [2026.8.2] - 2026-08-16

### Enthaltene Upstream-Versionen

- LTS: `CE 2.39.6, EE 2.39.6`
- STS: `CE 2.44.0, EE 2.44.0` (keine Änderung)

### Änderungen

- LTS: `2.39.5` → `2.39.6`
- EE LTS: `2.39.5` → `2.39.6`

---

## [2026.8.1] - 2026-08-02

- Neue Selector-App für Portainer CE/EE und LTS/STS.
- Ingress, Login-Speicher, Storage-Migration und Import/Export ergänzt.
- Ingress erzeugt beim einmaligen Portainer-Login einen dauerhaften Access Token, ohne das Passwort zu speichern.
- Die benutzerbezogene Anmeldung bleibt damit auch nach einem App-Neustart erhalten.
- Gleichzeitige JWT- und API-Key-Authentifizierung wird verhindert.

### Enthaltene Upstream-Versionen

- LTS: `CE 2.39.5, EE 2.39.5`
- STS: `CE 2.44.0, EE 2.44.0`
