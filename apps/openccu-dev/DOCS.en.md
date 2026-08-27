# openccu-dev

Experimental ha-repo packaging of the original OpenCCU app. The stable and
snapshot CCU and the proxy include the pinned ingress-loginsave overlay; the
HAP/DRAP helper does not have Ingress and is left without that patch.

## Updates

Original app versions and hardware settings come from OpenCCU/OpenCCU. Images
are pinned by digest. The dedicated daily **OpenCCU Update** workflow checks the
patch, builds both architectures and only then advertises new app versions.
Conflicts stop publication. The fork branch is not followed automatically.

## Login retention

For the three Ingress apps, `remember_ingress_users` and
`remember_ingress_credentials` default to false. Credential storage requires
session retention. Keep-alive defaults to 250 seconds and extends idle sessions.
Credentials are encrypted using AES-256-GCM, with the key alongside the records;
backups containing both allow decryption. Protect backups. Disabling retention
does not automatically delete stored records. WebUI logout removes that user's
saved record. Access to an HA account can grant access to its saved CCU session.

## Migration

This repository creates a separate HA app identity and data area. There is no
automatic migration. Back up OpenCCU from its WebUI and create an HA backup first.
Stop the previous CCU before starting the replacement with the same radio device.
Never run two CCUs against one radio. Restore the backup and check the Homematic
integration, addresses and ports. Set the proxy target again. Check the helper's
`openccu_slug` against the new full HA app ID. To roll back, stop the new CCU
before starting the old one. No existing data is removed by this repository.

Full HA, radio and WebUI login verification is required before production use.
Snapshots are development builds. These are not official OpenCCU releases.

[Original](https://github.com/OpenCCU/OpenCCU) ·
[Patch](https://github.com/sandmaennchen5/fork_OpenCCU/tree/ingress-loginsave)
