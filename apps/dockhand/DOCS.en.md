# Dockhand

This Home Assistant app runs the official Dockhand image. Dockhand provides
container, image, network, volume and Compose stack management, live logs,
terminal access, Git deployments and multiple Docker environments.

Open **Web UI** and create the first user. Add the local engine as a **Unix
Socket** environment; Home Assistant supplies `/var/run/docker.sock`. Dockhand's
database, stacks and Git repositories persist under `/data/dockhand` by default.

## Storage

`storage_location` selects `data` (`/data/dockhand`), `config`
(`/config/dockhand`) or `share` (`/share/<share_storage_directory>`).
Stop managed stacks before switching and choose an empty destination.
The last active data is copied before startup; existing destination data is never
overwritten. Legacy `/data` installations are copied without Home Assistant's
options or Ingress sessions. Originals remain as a recovery copy and are no longer
updated. To switch back, back up and empty the previous destination manually.
Check and redeploy stack bind mounts after moving storage: running containers may
still reference the old host paths. Do not remove those files prematurely.
App backups do not back up the volumes of managed containers.

## Ingress and login retention

A Supervisor-only proxy on internal port 1337 rewrites root-relative URLs and
forwards SSE and WebSockets. Direct port 3000 remains independent.

`remember_ingress_users` defaults to false. After a normal Dockhand login, enabling
it stores the session under `/data/ingress-sessions`, separately for each
Supervisor-provided HA user ID. No passwords are recorded. Sessions survive app
restarts but remain subject to Dockhand expiry and logout. Disabling the option
and restarting deletes stored sessions. Direct-port clients cannot use them.
Protect backups: they can contain session tokens.

“No environments configured” still requires adding a Docker environment manually.

Port `3000/tcp` is not published by default. Assign it only when access outside
Home Assistant Ingress is required. Docker socket access grants broad control of
the host; disable protection mode only when Home Assistant requires it for
`docker_api`. The upstream license does not permit commercial hosted-service use.

Documentation: <https://dockhand.pro/manual/>
