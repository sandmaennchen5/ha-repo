# Portainer Agent

The app runs the official standard Portainer Agent. The selector chooses the LTS or STS channel; the fixed apps contain one channel only. The Agent has no Web UI and stores no application state, so storage selection and import/export are intentionally omitted.

Connect Portainer Server to `<Home-Assistant-IP>:9001` without a protocol prefix. The connection is encrypted by the agent. A newly started Agent must be claimed promptly by Portainer; otherwise restart the app and connect again.

Set the same `agent_secret` on Server and Agent when using a shared secret. Additional documented Agent variables can be entered under `environment`. The Docker socket is supplied through Home Assistant's Docker API permission.

Documentation: <https://docs.portainer.io/admin/environments/add/docker/agent>

## Data, backups and migration

The app does not store a standalone application database. Access data and options are in the Home Assistant app configuration and are taken into account in the Home Assistant backup. Your own import or export is not necessary.

## Security

Enable only required features and ports. Access data belongs exclusively in the app configuration and not in protocols or additional command arguments. The actually required permissions are in the respective config.yaml.

## Known issues and limitations

If you have problems, first check the app protocol, the availability of the upstream service and the configured ports. Architecture and upstream restrictions apply according to the linked manufacturer documentation.

## Support

- App integration: [Issues in the Home Assistant app repository](https://github.com/sandmaennchen5/ha-repo/issues)
- Program function: [Upstream Project](https://docs.portainer.io/admin/environments/add/docker/agent)