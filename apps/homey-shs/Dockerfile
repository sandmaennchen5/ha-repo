ARG UPSTREAM_VERSION=latest
FROM ghcr.io/athombv/homey-shs:${UPSTREAM_VERSION}

ARG BUILD_VERSION
ARG UPSTREAM_VERSION
ARG BUILD_ARCH
ARG BUILD_DATE

LABEL \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.name="homey-shs" \
    org.opencontainers.image.base.name="ghcr.io/athombv/homey-shs:${UPSTREAM_VERSION}" \
    org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo" \
    org.opencontainers.image.vendor="Athom B.V."

COPY rootfs/usr/local/bin/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
COPY rootfs/usr/local/bin/migration.sh /usr/local/bin/migration.sh
COPY rootfs/usr/local/bin/rrdcached /usr/local/bin/rrdcached
COPY rootfs/usr/local/bin/healthcheck.mjs /usr/local/bin/healthcheck.mjs
COPY rootfs/usr/local/bin/homey-ingress-proxy.mjs /usr/local/bin/homey-ingress-proxy.mjs

RUN chmod a+x \
    /usr/local/bin/entrypoint-wrapper.sh \
    /usr/local/bin/migration.sh \
    /usr/local/bin/rrdcached

ENV HOMEY_SHS_VERSION="${UPSTREAM_VERSION}"

# The original image CMD is passed to this wrapper as arguments.
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["node", "/usr/local/bin/healthcheck.mjs"]
