# Drydock

This Home Assistant app runs the official Drydock image. Drydock monitors
container images, reports available updates and can update or roll back
containers when configured to do so.

Open **Web UI** after startup. The local Docker engine is discovered through the
Docker socket supplied by Home Assistant, and persistent state is stored in
`/data/drydock`. The app prepares this subdirectory for `node` before the upstream
privilege drop, leaving `/data` and `options.json` unchanged. Starting with
`1.6.0.2`, an existing `/data/dd.json` is copied only if the destination database
does not exist. The original remains as a recovery copy and is no longer updated.

The app confirms Drydock's anonymous mode because Home Assistant Ingress already
protects access. Publishing `3000/tcp` bypasses that protection; only expose it on
a trusted network or configure Basic Auth or OIDC in Drydock.

Docker socket access grants broad control of the host. Disable the app protection
mode only when Home Assistant requires it for `docker_api`.

Documentation: <https://getdrydock.com/docs/>
