## 3.89.8.20260719-ha3

- Restore expired sessions through the WebUI login form and verify the resulting WebUI session before redirecting.
- Rate-limit automatic login per HA user on the server, including when browser storage is blocked.
- Automatische Wiederanmeldung nach ungültiger SID: keine dauerhafte Sperre im Browser-Tab.
- Login-Formular auch unter /index.htm erkennen; Schleifenschutz nach erfolgreichem Seitenstart zurücksetzen.
- Bewusstes Abmelden löscht weiterhin Sitzung und gespeicherte Zugangsdaten.
- Original: `ghcr.io/openccu/openccu:3.89.8.20260719`.
- Pinned image and checked overlay; original runtime retained.
