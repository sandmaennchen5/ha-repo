### Home Assistant Repository – sandmaennchen5
## Documentation - Newt Client for Pangolin reverse proxy tunnel

The [Fossorial System - with Pangolin](https://docs.fossorial.io/) as the core component - is a self-hosted, tunneled reverse proxy with identity and access management designed to securely deliver private resources to userspace via encrypted WireGuard tunnels. Think of it like self-hosted Cloudflare tunnels.

Newt is the main client that connects to Pangolin and allows access to services on the same network as Newt. Install this and connect to your Pangolin instance to enable remote access to Home Assistant via secure WireGuard tunnels

## Home Assistant as a resource..

1. Go to your Pangolin dashboard and add a new resource called `Home Assistant`. Select the correct site related to the Home Assistant Newt instance that you defined in the prerequisites and give your resource a subdomain.
2. Make sure the “Enable SSL” option is checked so that you receive an automatically generated SSL certificate to encrypt browser connections.
3. In the Target Configuration section, add a target with method `HTTP`, domain `homeassistant.local.hass.io` and port `8123`. Click “Add Target” and save the settings.
5. Visit the [Home Assistant documentation](https://www.home-assistant.io/integrations/http) and follow the instructions to add a `trusted_proxy` to your `configuration.yaml` file. This is probably `172.30.33.0/24`. Make sure you also set `use_x_forwarded_for: true` so that the client's IP address appears in your logs and not the reverse proxy's IP address. Restart Home Assistant.
7. (Optional) If you want a resource that points to a Home Assistant add-on, use the add-on's slug in the domain section or Target configuration section. You can find this on the add-on configuration page in Home Assistant. In this example, the slug is “a0d7b954_tailscale”. If a `_` is present, as in this example, it must be replaced with a `-`. So the correct domain for this example would be `a0d7b954-tailscale`. Your port depends on the add-on; You will need to consult the add-on's documentation or configuration.

## Configuration

| option | Required field | Description |
|---|---|---|
| `endpoint` | ✅ | URL of your Pangolin server, e.g. E.g. `https://app.pangolin.net` |
| `id` | ✅ | Newt ID from Pangolin Dashboard |
| `secret` | ✅ | Newt-Secret from the Pangolin Dashboard |
| `log_level` | ❌ | Log level: `trace`, `debug`, `info`, `warn`, `error` (default: `info`) |
| `docker_socket` | ❌ | Docker socket path for label scraping, e.g. E.g. `/var/run/docker.sock` – see [Documentation](https://docs.pangolin.net/manage/sites/configure-site#docker-socket-integration) |
| `docker_enforce_network_validation` | ❌ | Force Docker network validation (default: `false`) |
| `dns` | ❌ | DNS server to resolve the endpoint. (Default: `9.9.9.9`) |
| `disable_clients` | ❌ | Disable clients on the WireGuard interface. (Default: `false`) |
| `disable_ssh` | ❌ | Disable SSH authentication daemons and native SSH mode (default: `false`) |
| `no_cloud` | ❌ | One cannot transition to the cloud when using managed nodes in Pangolin Cloud (default: `false`) |
| `ping_interval` | ❌ | Interval to ping the server (default: `15s`) |
| `ping_timeout` | ❌ | Timeout for each ping (default: `7s`) |
| `tls_client_cert_file` | ❌ | Path to the client certificate file (PEM/DER format) for mTLS |
| `tls_client_key` | ❌ | Path to the client private key file (PEM/DER format) for mTLS |
| `tls_client_ca` | ❌ | Path to the CA certificate file for validating remote certificates (can be specified multiple times) |
| `udp_proxy_idle_timeout string` | ❌ | Idle timeout for UDP proxy client flows before cleanup (equivalent to ). (Default: `90s`) |
| `interface` | ❌ | WireGuard interface name (default: `newt`) |
| `mtu` | ❌ | MTU for the internal WireGuard interface. (Default: `1280`) |
| `native` | ❌ | Use native WireGuard interface (default: `false`) || `metrics` | ❌ | Enable Prometheus /metrics exporter (default: `false`) |
| `metrics_admin_addr` | ❌ | Admin/Metrics bind an address (default: `127.0.0.1:2112`) |
| `metrics_async_bytes` | ❌ | Enable asynchronous byte counting (background flushing; lower hot path overhead, equivalent) (default: `false`) |
| `health_file` | ❌ | Path to health file for connection monitoring |
| `prefer_endpoint` | ❌ | Prefer this endpoint for the connection (if set, will override the endpoint from the server) |
| `region` | ❌ | Optional region resource attribute for telemetry and metrics |
| `name` | ❌ | Site name when provisioning with a provisioning key |
| `blueprint_file` | ❌ | Path to Blueprint file for defining Pangolin resources and configurations |
| `provisioning_blueprint_file` | ❌ | Path to a Bootstrap-only blueprint file |
| `config_file` | ❌ | Path to the JSON configuration file where Newt loads and saves settings |
| `ad_ca_cert_path` | ❌ | Path to CA certificate file for Auth Daemon (default: `/etc/ssh/ca.pem`) |
| `ad_generate_random_password` | ❌ | Generate a random password for authenticated users (default: `false`) |
| `ad_pre_shared_key` | ❌ | Pre-shared key for auth daemon authentication. |
| `ad_principals_file` | ❌ | Path to principals file for Auth Daemon (default: `/var/run/auth-daemon/principals`) |
| `enforce_hc_cert` | ❌ | Force certificate validation for health checks (default: `false`) |
| `port` | ❌ | Port for the peers to connect to Newt |
| `prof` | ❌ | Enable pprof debug endpoints on admin server (default: `false`) |
| `otlp` | ❌ | Enable OTLP exporters (metrics/traces) (default: `false`) |
| `updown` | ❌ | Path to updown script for target add/remove events (default: `false`) |


### Example configuration

```yaml
endpoint: "https://app.pangolin.net"
id: "my-newt-id"
secret: "my-newt-secret"
client:
  disable_clients: false
  disable_ssh: false
docker:
  docker_socket: "/var/run/docker.sock"
  docker_enforce_network_validation: false
extras:
  log_level: "info"
```

Note on options processing

- String options are passed to `newt` as `--flag value`.
- Boolean options are set as a flag (`--flag`) if they are `true`.

TLS CA(s)

`tls_client_ca` can be specified either as a single string or as a YAML list. Examples:

```yaml
# single file
tls_client_ca: "/etc/ssl/ca.pem"

# multiple files
tls_client_ca:
	- "/etc/ssl/ca.pem"
	- "/etc/ssl/extra-ca.pem"
```

The entries are passed to `newt` as a `--tls-client-ca` flag.

## Requirements

- A running [Pangolin](https://github.com/fosrl/pangolin) server
- A site registered in Pangolin with Newt ID and Secret
- Host network access and WireGuard permissions on the Home Assistant Host

## How to find `newt_id` and `newt_secret`

1. Open the Pangolin dashboard.
2. Select the desired site or create a new one.
3. Copy the generated `id` and `secret` from the site credentials.
4. Use the same `endpoint` configured in your Pangolin installation.

## Notes

- The add-on uses `host_network` so that the tunnel can be operated directly over the host network.
- It requires `NET_ADMIN` and `SYS_MODULE` permissions.
- After making changes to the configuration, the add-on must be restarted.
- `id` and `secret` must belong to the same Pangolin site.
- Do not share `secret` with unauthorized people.

## How it works

Newt connects to the Pangolin server via WebSocket and creates a WireGuard tunnel in user space. All proxied TCP/UDP connections are forwarded to local services without the need for kernel WireGuard or complex NAT routing rules.

## Troubleshooting

- Check add-on logs if startup fails.
- Make sure `endpoint` is reachable and uses a valid TLS certificate.
- Make sure `id` and `secret` are correctly from the same Pangolin site.
- Set `extras.log_level` to `debug` to get more detailed information.
- If you change the configuration, stop the add-on completely and restart it.

## More information

- [Pangolin Site Configuration](https://docs.pangolin.net/manage/sites/configure-site)- [Newt GitHub Repository](https://github.com/fosrl/newt)

## Portless healthcheck

The Docker healthcheck checks the local Newt process and `/tmp/newt_healthy`.
The existing health service continues checking endpoint reachability.
No HTTP health server or dedicated health port is required.
