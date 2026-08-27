# Pangolin CLI Client – Documentation

The app runs the official Pangolin CLI on Home Assistant OS. After the
When you log in, it creates a WireGuard tunnel and keeps it in the foreground
active. This means that services in the Home Assistant network and - depending on the
Pangolin configuration – remote private resources can be reached safely.

## Requirements

- Pangolin Cloud or an accessible self-hosted Pangolin instance
- a **Machine Client** created in the Pangolin dashboard
- its client ID and client secret
- Home Assistant OS or Home Assistant Supervised with support for apps

## Create machine client in Pangolin

1. Open Pangolin dashboard and go to the clients area.
2. Create a new Machine Client.
3. Copy endpoint, client ID and client secret.
4. Enter the values directly into the app configuration and do not include the secret
   Store notes, minutes or additional arguments.

## Facility

1. Create a Machine Client in Pangolin.
2. Copy Endpoint, Client ID and Client Secret to the app configuration.
3. Start the app and check the protocol.

The app permanently starts `pangolin-cli up --attach`. It uses host network, `/dev/net/tun` and `NET_ADMIN` to allow the client to manage the WireGuard interface and routes.

`Additional arguments` is intended solely for options supported by the installed CLI version. Access data should not be repeated there.

Upstream documentation: https://docs.pangolin.net/manage/clients/install-client#pangolin-cli-linux

## Configuration options

| option | duty | Default | Description |
|---|:---:|---|---|
| `endpoint` | yes | `https://app.pangolin.net` | Pangolin instance HTTPS URL |
| `client_id` | yes | empty | ID of the machine client |
| `client_secret` | yes | empty | Secret of the Machine Client |
| `extras.log_level` | no | `info` | `trace`, `debug`, `info`, `warn` or `error` |
| `extras.additional_args` | no | empty | further arguments for `pangolin-cli up` |

### Example

```yaml
endpoint: "https://pangolin.example.com"
client_id: "pc_0123456789"
client_secret: "MY SECRET SECRET"
extras:
  log_level: "info"
  additional_args: ""
```

Changes will only take effect after restarting the app. Use
`additional_args` only for options provided by the respective installed
CLI version are documented. Incorrect arguments prevent the start.

## Network and ports

The app uses the host network. Allow `/dev/net/tun` and `NET_ADMIN`
creating the WireGuard interface and setting routes.

| Port | Purpose | Publication necessary? |
|---:|---|---|
| `2112/tcp` | optional Admin/Prometheus endpoint of the CLI | usually no |

Port mapping is only necessary if the admin or metrics endpoint is aware
should be queried from the local network.

## Functional test

Once started the log should show a successful login and setup
of the tunnel. Then check a resource shared in Pangolin.
The Docker healthcheck checks the CLI process directly, without a TCP port.
It does not confirm reachability of every individual resource.

## Data, backups and migration

The app does not store a standalone application database. Access data and options are in the Home Assistant app configuration and are taken into account in the Home Assistant backup. Your own import or export is not necessary.

## Security

Enable only required features and ports. Access data belongs exclusively in the app configuration and not in protocols or additional command arguments. The actually required permissions are in the respective config.yaml.

## Known issues and limitations

- **Login fails:** Endpoint without additional path and client ID
  and Secret of the same Machine Client.
- **Tunnel does not start:** Deactivate protection mode and check whether
  `/dev/net/tun` is available on the host.
- **Resource not reachable:** Shares, destination address and routes in
  Check Pangolin Dashboard; Also pay attention to overlaps in local networks.
- **DNS resolution incorrect:** first test IP access and then
  Check the DNS configuration of Pangolin and the target network.- For detailed analysis `extras.log_level` temporarily set to `debug`
  or set `trace` and then reduce it again.

## Support

- App integration: [Issues in the Home Assistant app repository](https://github.com/sandmaennchen5/ha-repo/issues)
- Program function: [Upstream Project](https://github.com/fosrl/cli)
