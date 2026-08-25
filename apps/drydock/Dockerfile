ARG UPSTREAM_VERSION=1.6.0
FROM codeswhat/drydock:${UPSTREAM_VERSION}

ARG BUILD_VERSION
ARG UPSTREAM_VERSION
ARG BUILD_ARCH
ARG BUILD_DATE

LABEL \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.arch="${BUILD_ARCH}" \
  io.hass.type="addon" \
  io.hass.name="drydock" \
  org.opencontainers.image.base.name="docker.io/codeswhat/drydock:${UPSTREAM_VERSION}" \
  org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo" \
  org.opencontainers.image.vendor="CodesWhat"

ENV DD_STORE_PATH=/data \
    DD_ANONYMOUS_AUTH_CONFIRM=true \
    DD_SERVER_TRUSTPROXY=1

