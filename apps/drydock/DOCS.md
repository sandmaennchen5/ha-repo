# Drydock

Diese Home-Assistant-App startet das offizielle Drydock-Image. Drydock überwacht
Container-Images, meldet verfügbare Updates und kann – nach entsprechender
Konfiguration – Container aktualisieren oder zurückrollen.

## Verwendung

Öffne nach dem Start **Weboberfläche öffnen**. Die lokale Docker Engine wird über
den von Home Assistant bereitgestellten Docker-Socket erkannt. Der Zustand liegt
dauerhaft unter `/data/drydock`. Die App bereitet diesen Unterordner vor dem
Upstream-Benutzerwechsel für `node` vor; `/data` und `options.json` bleiben
unverändert. Ab Version `1.6.0.2` wird eine vorhandene `/data/dd.json` beim Start
kopiert, sofern noch keine Zieldatenbank existiert. Die Originaldatei bleibt als
Rückfallkopie erhalten und wird danach nicht mehr aktualisiert.

Die App bestätigt den anonymen Drydock-Modus, weil bereits Home Assistant Ingress
den Zugriff schützt. Wenn du Port `3000/tcp` direkt veröffentlichst, ist diese
zusätzliche Schutzschicht nicht vorhanden. Veröffentliche den Port daher nur in
einem vertrauenswürdigen Netz oder konfiguriere in Drydock Basic Auth beziehungsweise
OIDC.

Docker-Socket-Zugriff erlaubt weitreichende Änderungen am Host. Deaktiviere den
Schutzmodus der App nur, wenn Home Assistant dies für `docker_api` verlangt.

Dokumentation: <https://getdrydock.com/docs/>
