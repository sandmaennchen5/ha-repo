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

USER root
COPY rootfs/usr/local/lib/drydock-ha /usr/local/lib/drydock-ha
RUN node /usr/local/lib/drydock-ha/patch-ui.mjs

ENV DD_STORE_PATH=/data/drydock \
    DD_ANONYMOUS_AUTH_CONFIRM=true \
    DD_SERVER_TRUSTPROXY=1

# Keep upstream signal forwarding, socket checks and privilege drop.
ENTRYPOINT ["tini", "-g", "--", "node", "/usr/local/lib/drydock-ha/launcher.mjs"]
CMD []
