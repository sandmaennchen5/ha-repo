ARG BUILD_ARCH=amd64
ARG AGENT_LTS_IMAGE=portainer/agent:alpine
ARG AGENT_STS_IMAGE=portainer/agent:alpine-sts
FROM ${AGENT_LTS_IMAGE} AS lts
FROM ${AGENT_STS_IMAGE} AS sts
FROM ghcr.io/hassio-addons/base/${BUILD_ARCH}:16.0.0
COPY --from=lts /app/agent /opt/portainer-agent/lts/agent
COPY --from=sts /app/agent /opt/portainer-agent/sts/agent
COPY rootfs/ /
RUN chmod +x /usr/local/bin/portainer-agent-entrypoint /opt/portainer-agent/*/agent
ENTRYPOINT ["/usr/local/bin/portainer-agent-entrypoint"]
ARG BUILD_VERSION BUILD_ARCH BUILD_NAME
LABEL io.hass.version="${BUILD_VERSION}" io.hass.arch="${BUILD_ARCH}" io.hass.type="addon" io.hass.name="${BUILD_NAME}"
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD nc -z 127.0.0.1 9001 || exit 1
