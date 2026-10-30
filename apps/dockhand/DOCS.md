# Dockhand

Diese Home-Assistant-App startet das offizielle Dockhand-Image. Dockhand bietet
Container-, Image-, Netzwerk-, Volume- und Compose-Stack-Verwaltung, Live-Logs,
Terminalzugriff, Git-Deployments und mehrere Docker-Umgebungen.

## Erster Start

Öffne **Weboberfläche öffnen** und lege den ersten Benutzer an. Die lokale Docker
Engine ist über `/var/run/docker.sock` erreichbar. Wähle beim Anlegen der lokalen
Umgebung den Verbindungstyp **Unix Socket**. Dockhand speichert Datenbank, Stacks
und Git-Repositories standardmäßig dauerhaft unter `/data/dockhand`.

## Speicherwahl

`storage_location` bietet `data` (`/data/dockhand`), `config`
(`/config/dockhand`) und `share` (`/share/<share_storage_directory>`).
Vor einem Wechsel verwaltete Stacks stoppen und ein leeres Ziel wählen.
Die App kopiert die zuletzt verwendeten Daten vor dem Start; vorhandene
Zieldaten werden niemals überschrieben. Eine vorhandene Installation unter
`/data` wird ebenfalls übernommen, ohne `options.json` oder Ingress-Sitzungen
zu kopieren. Die Originaldaten bleiben als nicht mehr aktualisierte Rückfallkopie.
Für einen Wechsel zurück muss das alte Ziel zuerst manuell gesichert und geleert
werden. Nach einem Speicherwechsel können Stack-Bind-Mounts noch auf den alten
Host-Pfad zeigen: Stacks prüfen und gegebenenfalls neu bereitstellen, bevor alte
Daten entfernt werden. Ein App-Backup ersetzt kein Backup der verwalteten Volumes.

## Ingress und Anmeldung

Ingress läuft über einen separaten Proxy auf internem Port 1337. Er korrigiert
Dockhands absolute Pfade und leitet SSE sowie WebSockets weiter. Dieser Port
ist nur für den Supervisor erreichbar und wird nicht als Host-Port angeboten.
Der Direktport 3000 bleibt davon unabhängig.

`remember_ingress_users` ist standardmäßig aus. Bei Aktivierung wird nach einem
normalen Dockhand-Login nur die Sitzung unter `/data/ingress-sessions` gespeichert,
getrennt nach der vom Supervisor bestätigten HA-Benutzer-ID. Passwörter werden
nicht aufgezeichnet. Die Anmeldung überlebt App-Neustarts, aber nicht den von
Dockhand vorgegebenen Sitzungsablauf oder eine Abmeldung. Deaktivieren und
Neustarten löscht die gespeicherten Ingress-Sitzungen. Direkter Portzugriff erhält
keine dieser Sitzungen. Schütze App-Backups, da sie Sitzungstoken enthalten können.

„No environments configured“ bedeutet, dass noch eine Docker-Umgebung angelegt
werden muss; die Ingress-Korrektur legt nicht automatisch eine Umgebung an.

Port `3000/tcp` ist standardmäßig nicht veröffentlicht. Weise ihn nur zu, wenn du
Dockhand außerhalb von Home Assistant Ingress erreichen möchtest.

Dockhand benötigt für lokale Verwaltung weitreichenden Docker-Socket-Zugriff.
Deaktiviere den Schutzmodus der App, falls Home Assistant dies für `docker_api`
verlangt. Der Betrieb als kommerzieller gehosteter Dienst ist gemäß Upstream-Lizenz
nicht gestattet.

Dokumentation: <https://dockhand.pro/manual/>

## Umgebungsvariablen

| Option | ENV | Default |
| --- | --- | --- |
| `disable_whats_new` | `DISABLE_WHATS_NEW` | `false` |
| `compose_timeout` | `COMPOSE_TIMEOUT` | `900` seconds |
| `minimum_release_age_hours` | `MINIMUM_RELEASE_AGE_HOURS` | unset (0–720 hours) |
| `registry_request_timeout` | `REGISTRY_REQUEST_TIMEOUT` | `10` seconds (1–600) |
| `disable_local_login` | `DISABLE_LOCAL_LOGIN` | `false` |
| `skip_df_collection` | `SKIP_DF_COLLECTION` | `false` |
| `trust_forwarded_headers` | `TRUST_FORWARDED_HEADERS` | `false` |
| `origin` | `ORIGIN` | unset / leer |

Nach Änderungen die App neu starten. Weitergeleiteten Headern nur hinter einem vertrauenswürdigen Reverse-Proxy vertrauen, auch bei direktem Zugriff auf Port 3000. ORIGIN enthält das öffentliche Schema und den Host (bei Bedarf mit Port), ohne Ingress-Pfad; Passkeys benötigen diese Angabe und HTTPS außer bei localhost.

## Hawser-Timeout bei Stack-Updates

Die App passt für HTTP-Stack-Aufrufe an `/_hawser/compose` zusätzlich die
Header- und Body-Zeitlimits von Node/Undici an `compose_timeout` an. Damit
bricht dieser HTTP-Client nicht schon nach 300 Sekunden ab, wenn zum Beispiel
1800 Sekunden eingestellt sind. Das vorhandene Abbruchsignal bleibt erhalten.
Hawsers eigenes `COMPOSE_TIMEOUT` muss ebenfalls ausreichend hoch sein.
Dieser Fix ändert keine separate Edge-WebSocket-Zeitgrenze.

`minimum_release_age_hours` ist optional: Ohne Wert bleiben Dockhands
UI-Einstellungen wirksam; ein gesetzter Wert überschreibt sie global.
`disable_local_login` sperrt die lokale Passwortanmeldung und sollte erst
nach einem erfolgreichen Test einer alternativen Anmeldung aktiviert werden.
`skip_df_collection` deaktiviert Speicherabfragen im Upstream-Collector;
Speicherstatistiken können fehlen. Bei false wird die ENV-Variable entfernt,
da der Collector jeden nicht leeren Wert als aktiviert interpretiert.
Dies behebt keine Verbindungsfehler zu unerreichbaren Agenten.
