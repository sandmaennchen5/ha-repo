# Checkmk Agent

This Home Assistant app provides the official Checkmk agent via TCP port `6556`. It has no web interface and requires no configuration options.

## Facility

1. Install and start the app.
2. Make sure port `6556/tcp` is assigned to the host.
3. Add the Home Assistant host with the IP address of Home Assistant to Checkmk.
4. Test the agent connection on port `6556` and then run service discovery.

## Security

The classic Checkmk agent always delivers its data on port 6556 in plain text. The port should therefore only be accessible in a trustworthy local network. For access via other networks, traffic should be protected by a firewall, VPN or an encrypted connection supported by Checkmk. Port 6556 must not be forwarded unprotected to the Internet.

## Scope of data

The agent runs within the app container. It therefore primarily reports the system information visible in the container and not automatically all files or processes of the Home Assistant host.

Upstream: <https://github.com/Checkmk/checkmk>

## Versioning

Home Assistant does not reliably recognize Checkmk's `p` notation. Therefore, `X.Y.ZpN` is released as a purely numerical app version `X.Y.Z.N.R`. `R` is the revision of our app. Example: Checkmk `2.5.0p6`, first app build = `2.5.0.6.1`.

## Data, backups and migration

The app does not store a standalone application database. Access data and options are in the Home Assistant app configuration and are taken into account in the Home Assistant backup. Your own import or export is not necessary.

## Known issues and limitations

If you have problems, first check the app protocol, the availability of the upstream service and the configured ports. Architecture and upstream restrictions apply according to the linked manufacturer documentation.

## Support

- App integration: [Issues in the Home Assistant app repository](https://github.com/sandmaennchen5/ha-repo/issues)
- Program function: [Upstream Project](https://checkmk.com/)