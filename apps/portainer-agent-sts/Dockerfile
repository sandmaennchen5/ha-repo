ARG BUILD_ARCH=amd64
ARG UPSTREAM_VERSION=2.44.0
FROM portainer/agent:${UPSTREAM_VERSION}-alpine AS upstream
FROM ghcr.io/hassio-addons/base/${BUILD_ARCH}:16.0.0
COPY --from=upstream /app/agent /opt/portainer-agent/sts/agent
COPY rootfs/ /
RUN chmod +x /usr/local/bin/portainer-agent-entrypoint /opt/portainer-agent/sts/agent
ENV FIXED_CHANNEL=sts
ENTRYPOINT ["/usr/local/bin/portainer-agent-entrypoint"]
ARG BUILD_VERSION BUILD_ARCH BUILD_NAME
LABEL io.hass.version="${BUILD_VERSION}" io.hass.arch="${BUILD_ARCH}" io.hass.type="addon" io.hass.name="${BUILD_NAME}"
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD ["nc", "-z", "127.0.0.1", "9001"]

