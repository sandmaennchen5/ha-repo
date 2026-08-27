# Drydock

Drydock überwacht Container-Images und kann konfigurierte Updates ausführen.
Öffne die Oberfläche über Home Assistant Ingress. Ab 1.6.0.4 berücksichtigt
der Ingress-Proxy den Home-Assistant-Pfad auch für Vue-Routen, Assets und Live-Verbindungen.
Der optionale Direktzugriff bleibt auf Port 3000; Ingress verwendet intern Port 1337.

## Speicher

- `storage_location: data` (Standard): `/data/drydock`.
- `storage_location: config`: `/config/drydock` im App-Konfigurationsordner.
- `storage_location: share`: `/share/<share_storage_directory>`, standardmäßig `drydock-config`.

Beim Wechsel werden vorhandene Daten vor dem Start kopiert. Das Ziel muss leer sein;
bestehende Daten werden nicht überschrieben. Der bisherige Ordner bleibt als
Rückfallkopie erhalten und wird anschließend nicht mehr aktualisiert.
Ein Wechsel zurück auf einen bereits gefüllten Ordner wird deshalb abgelehnt.
Vor Speicherwechseln ein Backup anlegen. Freigabeordner können auch für andere Apps zugänglich sein.

Ältere Installationen übernehmen einmalig `/data/dd.json`, sofern noch kein
aktueller Store unter `/data/drydock` vorhanden ist. Die Rechte von `/data`
und `options.json` bleiben unverändert.

## Anmeldung merken

`remember_ingress_users: true` speichert gültige Drydock-Sitzungen getrennt
pro Home-Assistant-Benutzer unter `/data/ingress-sessions`, ohne Passwort.
Dazu beim Drydock-Login **Remember me** aktivieren. Ohne dieses Häkchen bleibt
die Anmeldung eine normale Browser-Sitzung und wird nicht dauerhaft gespeichert.
Drydocks Ablaufdatum bleibt maßgeblich; Abmelden entfernt die gespeicherte Sitzung.
Das Deaktivieren der Option entfernt gespeicherte Sitzungen beim nächsten App-Start.
Wer Zugriff auf dein HA-Konto hat, kann damit auch deine Drydock-Sitzung nutzen.

## Authentifizierung und weitere Optionen

Standardmäßig ist Drydocks anonymer Modus aktiviert, geschützt durch HA Ingress.
Für einen eigenen Drydock-Login `auth_username` und einen von Drydock unterstützten
Argon2id-Passworthash in `auth_password_hash` setzen. Dadurch wird anonymer Zugriff
deaktiviert. Keinen Klartext als Hash eintragen.

Weitere Drydock-Einstellungen lassen sich über `environment` als Liste von
`name`/`value`-Paaren mit `DD_`-Präfix setzen. Speicherpfad, interner Port,
TLS und Proxy-Vertrauen werden von der App festgelegt und sind hier nicht überschreibbar.
OIDC und externe Weiterleitungen wurden nicht im Ingress getestet.

Der Direktport umgeht HA Ingress: Ohne konfigurierte Drydock-Authentifizierung
nicht in ungeschützten Netzen veröffentlichen. Docker-Socket-Zugriff ermöglicht
weitreichende Änderungen am Host. Schutzmodus nur deaktivieren, wenn für
`docker_api` erforderlich.

[Drydock-Dokumentation](https://getdrydock.com/docs/)
