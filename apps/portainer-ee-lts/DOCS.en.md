# Portainer

This Home Assistant app runs the official Portainer Server and exposes it through Home Assistant Ingress. The selector app lets you choose Community (`ce`) or Business (`ee`) Edition and the `lts` or `sts` release channel. The four fixed apps contain only their named variant.

## First start

Open the app through **Open Web UI** and create the administrator within five minutes. Alternatively, set `advanced.admin_password` before the first start. Portainer only uses this option while creating the first administrator; changing it later does not reset the existing account.

`remember_ingress_users` retains the Portainer login separately for each Home Assistant user. After the first normal Portainer login, the app creates and stores a persistent Portainer access token so that the login also survives an app restart. The password is used only for Portainer's token-creation request and is never written to disk or to the app options. Use this only on a trusted Home Assistant installation because the retained token grants the same Portainer permissions as its Portainer account.

##Storage

- `data`: app-private `/data` (included in an app backup).
- `config`: shared app configuration `/config` through `addon_config` (not part of this app's private data backup).
- `share`: `/share/<share_storage_directory>` for manually accessible files.

On a storage change, existing Portainer state is moved to the selected location and removed from inactive locations. `/data/options.json` and `/data/ingress-sessions` are retained.

## Import and export

The **Import / Export** section can export the selected Portainer data to `/share` when the app stops. Imports can select the newest compatible archive automatically or use a manually entered path relative to `/share`. Existing data is only replaced when `overwrite_existing_data` is enabled. Version downgrade protection and deletion of a successfully imported archive are separate opt-in settings.

## Direct access

Ingress needs no assigned host port. Assign `9000/tcp` for direct HTTP access, `9443/tcp` for direct HTTPS access, or `8000/tcp` for the Edge Agent tunnel only when required. Portainer uses a self-signed certificate on 9443 unless custom certificates are configured within its data.

## Advanced options

The advanced group maps to documented Portainer CLI flags. `disable_content_security_policy` weakens browser protection and should remain disabled. `license_key` is only used by Business Edition. Arbitrary environment variables are supported for documented or future Portainer settings; duplicate variables override explicit app values.

Documentation: <https://docs.portainer.io/advanced/cli>

## Versioning and automatic updates

The selector uses calendar versions in the form `YYYY.M.N`. Its changelog lists the bundled CE/EE LTS and STS versions and marks an unchanged channel with `no change`. Fixed-edition apps use `<Portainer upstream version>.<app revision>`, for example `2.39.5.1`.

## Data, backups and migration

For persistent data, Home Assistant backups, storage locations, and manual restore, see the shared guide [Locations and Data Migration](../../docs/app-storage-and-migration.md). App-specific import/export options are described in the previous sections.

## Security

Enable only required features and ports. Access data belongs exclusively in the app configuration and not in protocols or additional command arguments. The actually required permissions are in the respective config.yaml.

## Known issues and limitations

If you have problems, first check the app protocol, the availability of the upstream service and the configured ports. Architecture and upstream restrictions apply according to the linked manufacturer documentation.

## Support

- App integration: [Issues in the Home Assistant app repository](https://github.com/sandmaennchen5/ha-repo/issues)
- Program function: [Upstream Project](https://docs.portainer.io/)