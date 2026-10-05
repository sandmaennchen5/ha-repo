# Pangolin CLI Client and Site – Documentation

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
| `mode` | no | `client` | `client`, `site` or `dual` |
| `site_id` | in site mode | empty | Site ID; alternatively provisioning or JSON |
| `site_secret` | in site mode | empty | Site secret; alternatively provisioning or JSON |
| `client_id` | in client mode | empty | ID of the machine client |
| `client_secret` | in client mode | empty | Secret of the machine client |
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

## Site mode (Newt successor)

Set `mode: site` to run `pangolin-cli up site`. Client credentials are not
required in this mode. Existing configurations without `mode` keep running as
machine clients.

```yaml
mode: site
endpoint: https://pangolin.example.com
site_id: YOUR-NEWT-ID
site_secret: YOUR-NEWT-SECRET
site:
  disable_clients: false
  disable_ssh: false
  metrics: true
  metrics_admin_addr: 127.0.0.1:2112
extras:
  log_level: info
  additional_args: ""
```

To migrate from Pangolin Newt, copy its `id` and `secret` into `site_id` and
`site_secret`. Stop the old Newt app before starting this app to avoid connecting
the same site twice. Advanced Newt options are available under `site`.

Alternatively set `site.provisioning_key` and leave both site credentials empty.
Provisioned credentials persist in `/data/pangolin-site.json` by default and are
included in app backups. Use `site.config_file` to load an existing JSON file.
Place custom blueprints, certificates and scripts in `/config` (the app config
directory); all paths refer to the app container.

These site options apply in `site` and `dual` modes. Only configured values are exported,
including explicit `false`. Priority: CLI > ENV > JSON > upstream defaults.
Site log level `trace` maps to `DEBUG`. `tls_client_ca` and
`local_endpoint_interfaces` accept comma-separated values. Docker discovery
requires a reachable external Docker socket proxy; this app does not mount the
Supervisor Docker socket. Upstream network validation does not work with host
networking. `otlp_endpoint` sets the OTLP destination; `otlp: true` enables export.
The process healthcheck stays active; `health_file` additionally indicates
connection health and is not evaluated by the Docker healthcheck.

| Option | ENV / Flag |
|---|---|
| `site.provisioning_key` | `SITE_PROVISIONING_KEY` |
| `site.name` | `SITE_NAME` |
| `site.config_file` | `CONFIG_FILE` |
| `site.dns` | `DNS` |
| `site.ping_interval` | `PING_INTERVAL` |
| `site.ping_timeout` | `PING_TIMEOUT` |
| `site.udp_proxy_idle_timeout` | `SITE_UDP_PROXY_IDLE_TIMEOUT` |
| `site.docker_socket` | `DOCKER_SOCKET` |
| `site.docker_enforce_network_validation` | `DOCKER_ENFORCE_NETWORK_VALIDATION` |
| `site.disable_clients` | `DISABLE_CLIENTS` |
| `site.disable_ssh` | `DISABLE_SSH` |
| `site.health_file` | `HEALTH_FILE` |
| `site.blueprint_file` | `BLUEPRINT_FILE` |
| `site.provisioning_blueprint_file` | `PROVISIONING_BLUEPRINT_FILE` |
| `site.updown` | `UPDOWN_SCRIPT` |
| `site.no_cloud` | `NO_CLOUD` |
| `site.metrics` | `SITE_METRICS_PROMETHEUS_ENABLED` |
| `site.otlp` | `SITE_METRICS_OTLP_ENABLED` |
| `site.otlp_endpoint` | `OTEL_EXPORTER_OTLP_ENDPOINT` |
| `site.metrics_admin_addr` | `SITE_ADMIN_ADDR` |
| `site.metrics_async_bytes` | `SITE_METRICS_ASYNC_BYTES` |
| `site.pprof` | `SITE_PPROF_ENABLED` |
| `site.region` | `SITE_REGION` |
| `site.enforce_hc_cert` | `ENFORCE_HC_CERT` |
| `site.tls_client_cert_file` | `TLS_CLIENT_CERT` |
| `site.tls_client_key` | `TLS_CLIENT_KEY` |
| `site.tls_client_ca` | `TLS_CLIENT_CAS` |
| `site.tls_client_cert` | `TLS_CLIENT_CERT_PKCS12` |
| `site.ad_pre_shared_key` | `AD_KEY` |
| `site.ad_principals_file` | `AD_PRINCIPALS_FILE` |
| `site.ad_ca_cert_path` | `AD_CA_CERT_PATH` |
| `site.ad_generate_random_password` | `AD_GENERATE_RANDOM_PASSWORD` |
| `site.interface` | `INTERFACE` |
| `site.port` | `PORT` |
| `site.mtu` | `MTU` |
| `site.native` | `USE_NATIVE_INTERFACE` |
| `site.native_main` | `USE_NATIVE_MAIN_INTERFACE` |
| `site.interface_main` | `INTERFACE_MAIN` |
| `site.local_endpoint_interfaces` | `LOCAL_ENDPOINT_INTERFACES` |
| `site.prefer_endpoint` | `--prefer-endpoint` |

[Upstream Site configuration](https://docs.pangolin.net/manage/sites/configure-site)

## Dual mode: client and site together

Set `mode: dual` to run the machine client and site connector simultaneously as
two separate s6 services. Each restarts independently when its process exits.
The process healthcheck requires both CLI processes in dual mode.

```yaml
mode: dual
endpoint: https://pangolin.example.com
client_id: YOUR-CLIENT-ID
client_secret: YOUR-CLIENT-SECRET
site_id: YOUR-SITE-ID
site_secret: YOUR-SITE-SECRET
site: {}
extras:
  log_level: info
  additional_args: ""
  client_additional_args: ""
  site_additional_args: ""
```

Each ID/secret pair belongs to its respective machine client or site. Both use
the same `endpoint`. Site provisioning and persisted JSON credentials also work
in dual mode. Entering both IDs does not automatically enable dual mode; select
`mode: dual` explicitly.

Dual defaults: client interface `pangolin-client`, site client tunnel interface
`pangolin-site`, native site main tunnel interface `pangolin-main`. Custom names
via `client.interface_name`, `site.interface`, and `site.interface_main` must be
distinct. The site interface names apply to native interfaces.

`client.http_addr` optionally enables the client HTTP API, e.g. `127.0.0.1:2113`.
If omitted, the client retains its upstream configuration. Site metrics default
to `127.0.0.1:2112`; use different bind addresses/ports if both HTTP servers are
active.

In dual mode `extras.additional_args` applies only to the client. Use
`extras.client_additional_args` and `extras.site_additional_args` for additional
role-specific arguments, also available in single modes. Arguments are separated
by whitespace; shell quoting is not evaluated.

Stop the old Newt app before connecting the same site. Both tunnels share the
host network; destination networks and VPN routes must match your Pangolin setup.
