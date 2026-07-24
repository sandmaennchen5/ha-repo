ARG BUILD_VERSION
FROM ghcr.io/athombv/homey-shs:${BUILD_VERSION}

ARG BUILD_VERSION
ARG BUILD_ARCH
ARG BUILD_DATE

LABEL \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.name="homey-shs" \
    org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo" \
    org.opencontainers.image.vendor="Athom B.V."

COPY rootfs/usr/local/bin/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
COPY rootfs/usr/local/bin/rrdcached /usr/local/bin/rrdcached
COPY rootfs/usr/local/bin/healthcheck.mjs /usr/local/bin/healthcheck.mjs

RUN chmod a+x \
    /usr/local/bin/entrypoint-wrapper.sh \
    /usr/local/bin/rrdcached

# The original image CMD is passed to this wrapper as arguments.
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["node", "/usr/local/bin/healthcheck.mjs"]
