ARG BUILD_ARCH=amd64
ARG UPSTREAM_VERSION=2.39.5
FROM portainer/portainer-ee:${UPSTREAM_VERSION}-alpine AS upstream
FROM ghcr.io/hassio-addons/base/${BUILD_ARCH}:16.0.0
RUN apk add --no-cache nginx nodejs tar
COPY --from=upstream /portainer /opt/portainer/ee-lts/portainer
COPY --from=upstream /public /opt/portainer/ee-lts/public
COPY rootfs/ /
RUN chmod +x /usr/local/bin/portainer-entrypoint /usr/local/bin/portainer-migration /opt/portainer/ee-lts/portainer
ENV FIXED_EDITION=ee FIXED_CHANNEL=lts
ENTRYPOINT ["/usr/local/bin/portainer-entrypoint"]
ARG BUILD_VERSION BUILD_ARCH BUILD_NAME BUILD_DESCRIPTION
LABEL io.hass.version="${BUILD_VERSION}" io.hass.arch="${BUILD_ARCH}" io.hass.type="addon" io.hass.name="${BUILD_NAME}"
HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 CMD curl -fsS http://127.0.0.1:9000/api/system/status >/dev/null || exit 1
