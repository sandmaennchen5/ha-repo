# Changelog


## [1.0.56.1] - 2026-10-30

### Upstream Release Notes

## What's new in v1.0.56

- 🐛 bitwarden bulk pull skips a key that is not a valid environment variable name (#1831)
- ✨ Spanish interface translation (PR#1811, @hugomon)
- ✨ Russian interface translation (PR#1809, @Kirill901)
- ✨ stack redeploy can respect each service's pull_policy and pull newer base images (#1800)
- 🐛 backups list shows a schedule's snapshots from every destination it has used (#1783)
- 🐛 scheduled updates retry a rate-limited pull (toomanyrequests) and honour the registry's retry-after (#1268)
- 🐛 pruning unused images works on older Docker engines (#1490)
- 🐛 the stacks page update check counts only containers that belong to a stack (#1803)
- 🐛 git stack deploys notify channels subscribed to stack events, once per deploy (#1295)
- 🐛 the git stack editor no longer lists a SOPS env file's metadata as variables (#1815)
- ✨ wildcard search (* and ?) in the containers and stacks search boxes (#1814)
- 🐛 self-update keeps a pinned IP and the MAC derived from it (#1816)
- 🐛 editing a container's env var no longer corrupts a command with embedded quotes (#1821)
- ✨ release notes for a held update are available during the cooldown (#1824)
- 🐛 git stacks over ssh keep the username from the repo url so they log in as the right user (#1828)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.56
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.55.3] - 2026-10-23

### Manuelles Update

Manuell aktualisierte Version.

Weitere Informationen: https://github.com/Finsys/dockhand

---

## [1.0.54.2] - 2026-10-23

- Add configurable DISABLE_WHATS_NEW, COMPOSE_TIMEOUT, TRUST_FORWARDED_HEADERS and ORIGIN environment variables with German and English descriptions and documentation.


## [1.0.55.1] - 2026-10-23

### Upstream Release Notes

## What's new in v1.0.55

- ✨ start and stop a container on a schedule (#1178)
- ✨ the interface language is kept on the server, so it survives a browser that clears its data (#1795)
- 🐛 the actions column can be resized in every data grid (#1777, PR#1787, @Totopo27)
- 🐛 newer version tags are found on GHCR repositories with tens of thousands of tags (#1792)
- 🐛 a stack that bind-mounts a single file restores, also onto a host where the file is missing (#1793)
- 🐛 the log view's live streaming toggle shows its state like the other toggles (#1654)
- 🐛 backup history shows the destination each run used, not the schedule's current one (#1783)
- ✨ moved-digest reports on pinned images are now configurable, globally or per container (#1780)
- ✨ terminal button in the container details view (#1754, PR#1768, @Totopo27)
- 🐛 mobile layouts for the containers list and environment tabs (PR#1758, @ddeitterick)
- ✨ Psono bulk pull and inline references now read Environment Variables secrets (#1784)
- ✨ decrypt a git stack's SOPS-encrypted env file with a new SOPS (age) secret provider (#386, PR#1781, @oha-4)
- 🐛 update docker-compose to 5.6.0-r2 to pick up its CVE fixes
- 🐛 update Node.js to 24.22.1 to pick up its October 21, 2026 security fixes
- ✨ EXPORT_METRICS_PUBLIC makes /metrics endpoint public, off by default (#1698)
- ✨ -lsNNN and -rN tag bumps count as newer versions, with tag.transform and link.template labels (#1703)
- ✨ minimum image age visual improvements and dockhand.skip.cooldown label (#1725)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.55
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.54.1] - 2026-10-17

### Upstream Release Notes

## What's new in v1.0.54

- 🐛 a version pattern with four or five parts is no longer refused, and an ignored pattern says why (#1702)
- 🐛 reading pages no longer fails behind an nginx reverse proxy that uses an upstream block (#1707)
- 🐛 image scans work again when the Docker daemon compresses its logs (PR#1715, @santacruz-usa)
- 🐛 a container with a long stop_grace_period updates instead of being left stopped
- ✨ the interface follows your language - translation engine and German (#494, PR#1706, PR#1709, PR#1718, PR#1719, PR#1722, PR#1726, PR#1734, PR#1736, PR#1738, PR#1742, @Hellraiser28)
- ✨ Simplified Chinese translation (#494, PR#1708, PR#1716, PR#1720, PR#1721, PR#1730, PR#1733, PR#1741, PR#1749, @maicent)
- ✨ French translations, for France and Canada (#494, PR#1714, PR#1717, PR#1727, PR#1728, PR#1729, PR#1732, PR#1735, PR#1746, PR#1747, PR#1748, @MagnanGG)
- ✨ Polish translation (#494)
- 🐛 a wider sidebar so translated labels fit (PR#1731, @MagnanGG)
- 🐛 a scheduled update is no longer blocked by a failed scan of an image the registry cannot name (#1737)
- ✨ Psono as a secret provider, with bulk pull and inline psono:// references
- ✨ the secret-provider banner collapses its key list when a stack loads many secrets (#1771)
- ✨ filter containers and stacks by "Untagged" (#1704, PR#1763, @Totopo27)
- 🐛 bulk operations on stacks over the API no longer fail every item (#1745)
- 🐛 a quoted value from a .env file no longer keeps its quotes in the form (#1750)
- 🐛 a dockhand.tags label stays on the container that carries it (#1740, PR#1743, @Totopo27)
- 🐛 the update check now reports a newer release on Kubernetes instead of giving up (#1710)
- 🐛 a moved digest on a pinned tag is now reported instead of silently ignored (#1755)
- 🐛 an unreachable environment no longer fills the log with errors for its own health checks (#1739, PR#1752, @Totopo27)
- 🐛 a git stack no longer recreates every container when a commit only touched files that do not affect them (#1761, #419, #364)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.54
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.53.1] - 2026-10-10

### Upstream Release Notes

## What's new in v1.0.53

- 🐛 remove the 1.0.52 PUID change that could alter stack file ownership on upgrade (#1700, #1701)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.53
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.52.1] - 2026-10-10

### Upstream Release Notes

## What's new in v1.0.52

- ✨ back up to an SFTP server with a dedicated SSH key and verified host keys (#1478, PR#1693, @ddeitterick)
- 🐛 a container started with PUID=1001 runs as that user instead of root (#1669)
- ✨ offer the compose file detected from container labels when adopting an external stack (#1612, PR#1617, @ondras)
- ✨ hold off automatic updates until a new image is older than a configurable minimum image age (#918, #1365, PR#1643, @TheDuffman85)
- ✨ a dockhand.name label sets the name a container is shown under (#1623)
- ✨ redeploy a stack without recreating every service, and choose how it redeploys (#148)
- ✨ sign in with a passkey instead of a password (#1431, PR#1431, @StefanSa, @timcappalli)
- 🐛 skip newer-version tags whose image is older than the one running (#1673)
- ✨ filter newer-version candidates per container (#1674)
- ✨ read per-stack resource totals from the API (#1626)
- ✨ show stack health on the stacks page, and filter by it (#1678)
- 🐛 find the stack folder when a nested bind shares a name with one at the root (#1679)
- 🐛 ordering one container with dockhand.order now moves it ahead of the unlabelled ones (#1117)
- 🐛 restore preview no longer reports an empty target for a stack whose files are there (#1681)
- 🐛 updating a Podman container started by podman-compose no longer leaves it stopped (#1692)
- 🐛 the next compose deploy no longer recreates a container Dockhand just updated (#1687)
- 🐛 a stack's bind directories are no longer left out of a backup when no volume covers them (#1696)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.52
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.51.1] - 2026-10-03

### Upstream Release Notes

## What's new in v1.0.51

- ✨ drag to reorder environments (#1638)
- ✨ drag to reorder tags, and the grid groups follow that order (#1651)
- 🐛 compose validate no longer reports a volume path built from a variable as undefined (#1653)
- 🐛 sorting containers by uptime now orders an hour-old container correctly (#1652)
- 🐛 the vulnerability scan retention schedule saves and reloads correctly
- 🐛 the stack editor no longer re-queries the secret provider while it sits idle (#1646)
- 🐛 keepass:// and azurekv:// references are recognised in the stack editor
- 🐛 a git stack whose deploy fails is retried on the next sync instead of being marked in sync (#1660)
- 🐛 the scanner check now finds newer grype and trivy releases, not just a rebuild of the pinned tag (#1658)
- 🐛 default scanner images bumped to grype v0.119.0 and trivy 0.75.0 (#1658)
- ✨ containers can be tagged with a dockhand.tags label, with a colour and icon (#1655)
- ✨ containers optionally show the tags their stack carries (#1665)
- ✨ drag files onto the file browser to upload them (#1661, PR#1662, @Wardrop)
- 🐛 update docker-compose 5.5.1-r2, undici 7.30.0, devalue 5.9.3 and nodemailer 10.0.10 for security fixes

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.51
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.50.1] - 2026-09-30

### Upstream Release Notes

## What's new in v1.0.50

- ✨ update a container straight from its details view when a newer image is available (#1588)
- ✨ duplicate a backup schedule to reuse its settings for another destination (#1578)
- ✨ mark a secret provider as default so new stacks start with it selected (#1609)
- ✨ optionally skip the login form, and sign out at the identity provider (#563, #562, #1318)
- ✨ dashboard disk usage segments link straight to images, volumes or containers (#1314)
- ✨ the container file browser opens at the container's working directory (#1285)
- ✨ mattermost notifications arrive as colour-coded cards, like the discord ones (#1607)
- ✨ container icons fall back to the image namespace when the name has none (#1624)
- ✨ tag groups are ordered alphabetically by tag name (#1625)
- 🐛 oidc sign-in survives a restart and works across multiple replicas (#1601)
- 🐛 cleaner image scan logs, and the real registry error (#1486, #1628, #1629)
- 🐛 compose validate no longer flags variables a secret provider supplies (#1621)
- 🐛 updating a container through the API keeps its secondary networks and their aliases
- 🐛 recreating a container no longer reuses its old auto-assigned MAC address (#1618)
- 🐛 podman's default bridge is no longer shown as an extra network on containers (#1619)
- 🐛 a scheduled container update clears its pending row, so update all no longer fails on it (#1632)
- 🐛 image prune no longer times out after 30s when filters are set (#1630)
- 🐛 exporting an image whose name contains a slash no longer fails (#1635)
- 🐛 percentage disk warnings are marked as unusable on hosts that report no total (#1631)
- 🐛 https now starts with certificates that have no subject, like newer let's encrypt ones (#1622)
- 🐛 dashboard keeps its top containers and recent events after a container event (#1608)
- 🐛 the secret provider selector is no longer lost on save in the env text view (#1620)
- 🐛 a git stack .env value can be quoted and refer to another variable (#1018)
- 🐛 update docker-compose 5.5.1-r1, devalue 5.9.2 and nodemailer 9.1.1 for security fixes

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.50
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.49.1] - 2026-09-23

### Upstream Release Notes

## What's new in v1.0.49

- 🐛 select-all checkbox shows a partial state, not a full tick, for a partial selection (#1605)
- 🐛 a long backup no longer crashes the app when its log stream goes quiet (#1610)
- ✨ tag containers and stacks, then filter and group the grid by tag (#781, #870)
- 🐛 removing all of a stack's environment variables no longer leaves stale entries (#1598)
- 🐛 templates with duplicate names no longer stop the templates page from rendering
- 🐛 the container toolbar no longer clips its buttons on mobile (#1586)
- 🐛 use webp or png for selfh.st icons that have no svg (#1596)
- 🐛 don't report a newer version tag that resolves to the image you already run (#1572)
- 🐛 fix vulnerability scans failing on the containerd image store (#1569, #1350)
- 🐛 show CPU and memory for containers on Windows Docker hosts (#1574)
- 🐛 don't send container died/killed notifications for a container being updated (#68)
- 🐛 stop, start, restart and remove stacks that use secret providers, e.g. stop-during-backup (#1579)
- 🐛 check for image updates on a plain-HTTP registry (#1580)
- 🐛 send you to the login page when your session expires (#1577)
- 🐛 skip hidden folders like .snapshots when scanning for stacks to adopt (#1251)
- 🐛 updating a Podman container managed by a systemd Quadlet unit now works (#1529, #1559)
- 🐛 option to skip bind mounts when scheduling backups for a whole environment (#1570)
- 🐛 git stack env vars stay visible in the editor after saving (#1112)
- ✨ search and filter containers by label (#1372)
- ✨ editor themes: select from 40 themes with live preview (#1309)
- ✨ command palette searches stacks and containers across all hosts (#670)
- ✨ clear a search field with the X button in it (#1321)
- 🐛 clearing a container's command now reverts it to the image default (#1489)
- ✨ one-shot container exec API returning stdout, stderr and exit code (#1380)
- ✨ set and change file ownership in the container file browser (#224)
- 🐛 cut backup read transactions on S3/B2 by caching the restic index between runs (#1600)
- 🐛 dashboard no longer flashes zero running containers on a remote host (#1608)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.49
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.48.1] - 2026-09-14

### Upstream Release Notes

## What's new in v1.0.48

- ✨ bulk-delete snapshots, and optionally forget a config's snapshots when you delete it (#1556)
- ✨ option to choose which stack operations show the full log (#1558)
- ✨ show the stack icon and name in stack action popups (#1526)
- 🐛 log in to registries over TLS on remote HTTPS environments (#1557)
- 🐛 vulnerability scans and alerts show the image tag, not just its digest (#1528)
- 🐛 resolve secret provider references when restoring a stack from a backup (#1521)
- 🐛 stop password managers from offering to save stack secret env-var fields (#1517)
- 🐛 repository stats no longer fail on the backups screen (#1561)
- 🐛 dashboard image disk usage no longer counts shared layers multiple times (PR#1461, @omggga)
- ✨ add a docker attach terminal mode (#1078, PR#1377, @ivanjx)
- 🐛 stack action buttons show for stopped and freshly created stacks, regression (#1565)
- 🐛 the update dialog no longer shows an unreleased version as the target (#1566)
- 🐛 update Go 1.26.8, docker-compose 5.5.0-r5, nodemailer 9.1.0, js-yaml 4.3.2 for security fixes

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.48
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.47.1] - 2026-09-12

### Upstream Release Notes

## What's new in v1.0.47

- ✨ live compose output during deploys, plus a per-stack deploy history tab (#506, #1292, #1540, PR#1499, @strausmann)
- 🐛 back up stacks whose folder is bind-mounted over the data volume (#1533)
- 🐛 backup restore preview now works for view-only roles (#1534)
- ✨ warn before saving a stack whose compose file location won't survive a container recreate (#1524)
- 🐛 OpenAPI spec accuracy fixes (#1531, #1530, PR#1532, @strausmann)
- 🐛 "always redeploy" git stacks now force-recreate so config changes take effect (#1523)
- 🐛 resolve secret references (op://, keepass://, ...) pasted with surrounding quotes (#1521)
- 🐛 deleting a secret provider now warns which stacks it unbinds (#1522)
- 🐛 deploy a 1:1-mounted local stack by file so its compose path label is preserved (#1514)
- 🐛 store the compose path when a stack is created via the API without one (#1515)
- 🐛 Microsoft Teams (via Workflows) accepts the new Power Automate webhook URL format (#1512)
- 🐛 container shell sessions each keep their own live terminal when you switch between them (#1516)
- 🐛 sort container uptimes under a minute correctly instead of tying them (PR#1395, @wrlee)
- 🐛 load the web manifest through a Cloudflare tunnel by sending credentials (PR#1513, @Macleykun)
- 🐛 copy the restic password over plain HTTP (#1488)
- 🐛 scope stack backup snapshots to their own environment (#1546)
- 🐛 theme defaults in General settings now save and display correctly when auth is on (#1547)
- ✨ warn when a host's kernel has cgroup memory accounting disabled (#1549)
- 🐛 self-update no longer fails at the updater step on baseline (old x86_64) images (#1500)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.47
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.46.1] - 2026-09-02

### Upstream Release Notes

## What's new in v1.0.46

- ✨ restart a stack in depends_on order, keeping the same containers (#1480)
- ✨ allow secret-less git webhooks via the ALLOW_WEBHOOKS_WITHOUT_SECRET env var
- ✨ optional STACKS_DIR flat layout for local stacks (#514, #778, PR#1482, @xd003)
- 🐛 faster incremental backups when multiple stacks share one repository (#1494)
- 🐛 "disable build cache" no longer errors on deploy (#1479, PR#1020, @He-Is-HaZaRdOuS)
- 🐛 test connection on a saved environment without re-entering the token (#1483)
- 🐛 populate environment variables again finds the repo's .env file (#1495)
- 🐛 POST /api/stacks honors the target environment in the body (#1491)
- 🐛 large image scans no longer fail when the scanner log rotates (#1496)
- 🐛 Compose Validate no longer false-flags a valid env_file (#1497)
- 🐛 cache app icons in one request so the containers and stacks pages load faster
- 🐛 upgrade svelte to 5.56.10 (#1476, PR#1477, @ThanatosDi)
- 🐛 refresh the bundled docker-compose (5.5.0-r2)
- 🐛 stricter per-environment access and permission checks across the API
- 🐛 redact secret values from compose command output and restrict backup restore targets
- 🐛 local-path backup destinations now reject a host path that isn't a Dockhand bind mount (#1506)
- 🐛 escape $ in env values when generating a compose file from a container (#1507)
- 🐛 clearer git permission errors that match the credential type (token vs SSH key) (#1509)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.46
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.45.1] - 2026-08-27

### Upstream Release Notes

## ⚠️This is important security upgrade with a number of API hardenings. 

## What's new in v1.0.45

- 🐛 security hardening across the API
- ✨ KeePassXC as a secret provider - pull secrets from a .kdbx via keepassxc-cli, bulk or inline refs (#1460)
- ✨ compose generated from a container now captures network config and resource limits (#1464)
- ✨ compose validate flags a service with no healthcheck and a defined-but-unused named volume
- ✨ optional Webhook column on the stacks list with a git stack's webhook id and copy-URL button (#845)
- ✨ sort by Disk I/O and Net I/O - the header cycles read/write and down/up (#1111)
- ✨ option to disable the session timeout (#1302)
- 🐛 pausing or resuming a backup schedule no longer clears the retention policy (#1462)
- 🐛 emergency script to relocate stack paths after moving DATA_DIR (#651, #904)
- 🐛 git stacks can now set a custom icon (#1473)

## Docker image

```bash
docker pull fnsys/dockhand:v1.0.45
```

Also available as `fnsys/dockhand:latest`

[View on Docker Hub](https://hub.docker.com/r/fnsys/dockhand)

Weitere Informationen: https://github.com/Finsys/dockhand/releases/latest

---

## [1.0.44.6] - 2026-08-27

- Ingress-Menülinks laden Seiten serverseitig, damit der für `/` gebaute Client-Router keine HA-Ingress-Unterpfade als unbekannte Routen behandelt.
- Gilt auch für dynamisch eingefügte Links; Direktzugriff auf Port 3000 bleibt unverändert.
- Seitenwechsel laden die Oberfläche neu. Gespeicherte Anmeldungen bleiben unverändert.
- App-Revision für einen vollständigen Neuaufbau um eins erhöht.
- Ingress-Proxy mit Unterpfad-Unterstützung für Assets, Navigation, API, SSE und WebSockets.
- Speicherwahl zwischen `/data/dockhand`, `/config/dockhand` und einem Unterordner von `/share`; sichere Übernahme in leere Ziele.
- Optionale, je Home-Assistant-Benutzer getrennte Speicherung der Dockhand-Sitzung ohne Passwortspeicherung. Ablauf und Abmeldung bleiben wirksam.
- Direkter Zugriff bleibt auf Port 3000 verfügbar und verwendet keine gespeicherten Ingress-Sitzungen.
- Erste Home-Assistant-App für Dockhand 1.0.44.
- Home Assistant Ingress, optionaler Direktport und persistente Daten unter `/data`.
- Lokale Docker- und Compose-Verwaltung über die Supervisor-Docker-API.
