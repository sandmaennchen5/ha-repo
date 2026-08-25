ARG UPSTREAM_VERSION=1.0.44
FROM fnsys/dockhand:v${UPSTREAM_VERSION}

ARG BUILD_VERSION
ARG UPSTREAM_VERSION
ARG BUILD_ARCH
ARG BUILD_DATE

LABEL \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.arch="${BUILD_ARCH}" \
  io.hass.type="addon" \
  io.hass.name="dockhand" \
  org.opencontainers.image.base.name="docker.io/fnsys/dockhand:v${UPSTREAM_VERSION}" \
  org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo" \
  org.opencontainers.image.vendor="Finsys"

ENV DATA_DIR=/data \
    PUID=0 \
    PGID=0
