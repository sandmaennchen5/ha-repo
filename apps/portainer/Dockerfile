ARG BUILD_ARCH=amd64
ARG PORTAINER_CE_LTS_IMAGE=portainer/portainer-ce:alpine
ARG PORTAINER_CE_STS_IMAGE=portainer/portainer-ce:alpine-sts
ARG PORTAINER_EE_LTS_IMAGE=portainer/portainer-ee:alpine
ARG PORTAINER_EE_STS_IMAGE=portainer/portainer-ee:alpine-sts
FROM ${PORTAINER_CE_LTS_IMAGE} AS ce_lts
FROM ${PORTAINER_CE_STS_IMAGE} AS ce_sts
FROM ${PORTAINER_EE_LTS_IMAGE} AS ee_lts
FROM ${PORTAINER_EE_STS_IMAGE} AS ee_sts
FROM ghcr.io/hassio-addons/base/${BUILD_ARCH}:16.0.0
RUN apk add --no-cache nginx nodejs tar
COPY --from=ce_lts /portainer /opt/portainer/ce-lts/portainer
COPY --from=ce_lts /public /opt/portainer/ce-lts/public
COPY --from=ce_sts /portainer /opt/portainer/ce-sts/portainer
COPY --from=ce_sts /public /opt/portainer/ce-sts/public
COPY --from=ee_lts /portainer /opt/portainer/ee-lts/portainer
COPY --from=ee_lts /public /opt/portainer/ee-lts/public
COPY --from=ee_sts /portainer /opt/portainer/ee-sts/portainer
COPY --from=ee_sts /public /opt/portainer/ee-sts/public
COPY rootfs/ /
RUN chmod +x /usr/local/bin/portainer-entrypoint /usr/local/bin/portainer-migration && \
    chmod +x /opt/portainer/*/portainer
ENTRYPOINT ["/usr/local/bin/portainer-entrypoint"]
ARG BUILD_VERSION BUILD_ARCH BUILD_NAME BUILD_DESCRIPTION
LABEL io.hass.version="${BUILD_VERSION}" io.hass.arch="${BUILD_ARCH}" io.hass.type="addon" \
      io.hass.name="${BUILD_NAME}" io.hass.description="${BUILD_DESCRIPTION}"
HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 \
  CMD ["curl", "-fsS", "-o", "/dev/null", "http://127.0.0.1:9000/api/system/status"]
