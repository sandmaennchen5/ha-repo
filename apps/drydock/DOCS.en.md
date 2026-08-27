# Drydock

Drydock monitors container images and can perform configured updates.
Open the UI through Home Assistant Ingress. Version 1.6.0.4 handles the HA
prefix for Vue routes, assets and live connections. Optional direct access
remains on port 3000; internal Ingress uses port 1337.

## Storage

- `storage_location: data` (default): `/data/drydock`.
- `storage_location: config`: `/config/drydock` in the app configuration folder.
- `storage_location: share`: `/share/<share_storage_directory>`, default `drydock-config`.

Switching copies existing state before startup. The destination must be empty;
existing files are never overwritten. The previous folder remains as a recovery
copy and is no longer updated. Switching back to an already populated folder is
therefore rejected. Back up before switching. Shared folders may be accessible
to other apps.

Legacy `/data/dd.json` is copied once if no current store exists under
`/data/drydock`. Permissions on `/data` and `options.json` remain unchanged.

## Remember Ingress login

Enable `remember_ingress_users` and check **Remember me** when signing in to
Drydock. Valid sessions are saved per HA user under `/data/ingress-sessions`;
passwords are never saved. Without the checkbox, login remains a browser session
and is not persisted by the proxy. Drydock expiry is respected; logout clears
the saved session. Disabling the option clears saved sessions on the next start.
Anyone with access to your HA account can also use its saved Drydock session.

## Authentication and additional settings

Anonymous Drydock access is enabled by default behind HA Ingress. For a separate
Drydock login, set `auth_username` and a Drydock-compatible Argon2id password
hash in `auth_password_hash`. This disables anonymous access. Do not enter a
plaintext password as a hash.

`environment` accepts a list of `name`/`value` pairs with a `DD_` prefix.
Storage path, internal port, TLS and proxy trust are fixed by this app.
OIDC and external redirects have not been tested through Ingress.

Direct port access bypasses HA authentication. Do not expose it to untrusted
networks without Drydock authentication. Docker socket access grants extensive
host control. Disable protection mode only if required for `docker_api`.

[Drydock documentation](https://getdrydock.com/docs/)
