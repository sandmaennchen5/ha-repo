# Dockhand

This Home Assistant app runs the official Dockhand image. Dockhand provides
container, image, network, volume and Compose stack management, live logs,
terminal access, Git deployments and multiple Docker environments.

Open **Web UI** and create the first user. Add the local engine as a **Unix
Socket** environment; Home Assistant supplies `/var/run/docker.sock`. Dockhand's
database, stacks and Git repositories persist under `/data`.

Port `3000/tcp` is not published by default. Assign it only when access outside
Home Assistant Ingress is required. Docker socket access grants broad control of
the host; disable protection mode only when Home Assistant requires it for
`docker_api`. The upstream license does not permit commercial hosted-service use.

Documentation: <https://dockhand.pro/manual/>

