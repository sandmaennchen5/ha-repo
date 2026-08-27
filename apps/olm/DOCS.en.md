### Home Assistant Repository – sandmaennchen5
## Documentation - OLM Client for Pangolin Reverse Proxy Tunnel

The [Fossorial System - with Pangolin](https://docs.fossorial.io/) as the core component - is a self-hosted, tunneled reverse proxy with identity and access management designed to securely deliver private resources to userspace via encrypted WireGuard tunnels. Think of it like self-hosted Cloudflare tunnels.

Newt is the main client that connects to Pangolin and allows access to services on the same network as Newt. Install this and connect to your Pangolin instance to enable remote access to Home Assistant via secure WireGuard tunnels

## Home Assistant as a resource..

1. Go to your Pangolin dashboard and add a new resource called `Home Assistant`. Select the correct site related to the Home Assistant Newt instance that you defined in the prerequisites and give your resource a subdomain.
2. Make sure the “Enable SSL” option is checked so that you receive an automatically generated SSL certificate to encrypt browser connections.
3. In the Target Configuration section, add a target with method `HTTP`, domain `homeassistant.local.hass.io` and port `8123`. Click “Add Target” and save the settings.
5. Visit the [Home Assistant documentation](https://www.home-assistant.io/integrations/http) and follow the instructions to add a `trusted_proxy` to your `configuration.yaml` file. This is probably `172.30.33.0/24`. Make sure you also set `use_x_forwarded_for: true` so that the client's IP address appears in your logs and not the reverse proxy's IP address. Restart Home Assistant.
7. (Optional) If you want a resource that points to a Home Assistant add-on, use the add-on's slug in the domain section or Target configuration section. You can find this on the add-on configuration page in Home Assistant. In this example, the slug is “a0d7b954_tailscale”. If a `_` is present, as in this example, it must be replaced with a `-`. So the correct domain for this example would be `a0d7b954-tailscale`. Your port depends on the add-on; You will need to consult the add-on's documentation or configuration.

## Facility

1. Create an Olm client in Pangolin.
2. Enter Pangolin endpoint, Olm ID and Secret in the app configuration.
3. Start the app and check the protocol.

The app uses host network, `/dev/net/tun`, `NET_ADMIN` and `SYS_MODULE` to allow Olm to manage the WireGuard interface and required routes.

Olm is now only recommended by fosrl for advanced scenarios. For new installations, the Pangolin CLI is the preferred variant.

Upstream documentation: https://docs.pangolin.net/manage/clients/understanding-clients

## Configuration

| option | duty | Default | Description |
|---|:---:|---|---|
| `endpoint` | yes | `https://app.pangolin.net` | Pangolin instance URL |
| `id` | yes | empty | Olm client ID from Pangolin |
| `secret` | yes | empty | client secret key |
| `network.mtu` | no | `1280` | MTU of the WireGuard interface |
| `network.dns` | no | `8.8.8.8` | DNS server for the tunnel |
| `network.upstream_dns` | no | `8.8.8.8:53` | parent DNS server with port |
| `network.interface` | no | `olm` | WireGuard interface name |
| `extras.log_level` | no | `INFO` | `DEBUG`, `INFO`, `WARN`, `ERROR` or `FATAL` |
| `extras.disable_holepunch` | no | `false` | disable direct peer connection |
| `extras.disable_relay` | no | `false` | Disable relay connection |
| `extras.prefer_local_routes` | no | `false` | prefer existing local routes |
| `extras.override_dns` | no | `true` | Let Olm manage DNS settings |
| `extras.tunnel_dns` | no | `false` | Route DNS requests through the tunnel |

### Example configuration

```yaml
endpoint: "https://pangolin.example.com"
id: "olm-client-id"
secret: "MY-SECRET-SECRET"
networks:
  mtu: 1280
  dns: "8.8.8.8"
  upstream_dns: "8.8.8.8:53"
  interface: "olm"
extras:
  log_level: "INFO"
  disable_holepunch: false
  disable_relay: false
  prefer_local_routes: falseoverride_dns: true
  tunnel_dns: false
```

After making changes, the app must be restarted. Change MTU, DNS and
Routing only for a specific network problem and individually so that the
The impact remains understandable.

## Network and health check

The app uses host networking and can affect the Home Assistant host's routes.
The Docker healthcheck checks the app process directly, without a TCP port,
and detects a failed app process
but does not check every remote pangolin resource.

Hole punching allows for a direct connection whenever possible. A relay
serves as a fallback path if direct connections through NAT or firewall are not possible
are possible. If both functions are deactivated, the tunnel can become dependent
the network fails completely.

## Requirements

- A running [Pangolin](https://github.com/fosrl/pangolin) server
- Host network access and WireGuard permissions on the Home Assistant Host

## Data, backups and migration

The app does not store a standalone application database. Access data and options are in the Home Assistant app configuration and are taken into account in the Home Assistant backup. Your own import or export is not necessary.

## Security

Enable only required features and ports. Access data belongs exclusively in the app configuration and not in protocols or additional command arguments. The actually required permissions are in the respective config.yaml.

## Known issues and limitations

- **Authentication faulty:** check `endpoint`, `id` and `secret`; ID and
  Secret must belong to the same Olm client.
- **No WireGuard interface:** Disable protection mode and `/dev/net/tun`
  and check the required permissions.
- **Connection unstable:** first check the accessibility of the end point, then
  Reduce MTU as a test.
- **DNS issues:** Test behavior with `override_dns` and `tunnel_dns` individually
  and check `upstream_dns` including port.
- **Route conflict:** avoid overlapping local and remote subnets;
  Only activate `prefer_local_routes` consciously.
- Use `extras.log_level: DEBUG` for diagnostics and then again
  reset to `INFO`.

## More information

- [Pangolin Configuration](https://docs.pangolin.net)
- [Newt GitHub Repository](https://github.com/fosrl/olm)
