ARG BUILD_ARCH=amd64
FROM ghcr.io/hassio-addons/base/${BUILD_ARCH}:16.0.0

ARG UPSTREAM_VERSION=2.5.0p13

RUN apk add --no-cache busybox-extras wget && \
    wget -qO /usr/local/bin/check_mk_agent \
      "https://raw.githubusercontent.com/Checkmk/checkmk/refs/heads/release/${UPSTREAM_VERSION}/agents/check_mk_agent.openwrt" && \
    chmod 0755 /usr/local/bin/check_mk_agent && \
    printf '%s\n' 'checkmk-agent 6556/tcp # Checkmk monitoring agent' >> /etc/services

COPY rootfs/ /
RUN chmod 0755 /etc/services.d/inetd/run /etc/services.d/inetd/finish

ARG BUILD_VERSION BUILD_ARCH BUILD_NAME BUILD_DESCRIPTION
LABEL io.hass.version="${BUILD_VERSION}" \
      io.hass.arch="${BUILD_ARCH}" \
      io.hass.type="addon" \
      io.hass.name="${BUILD_NAME}" \
      io.hass.description="${BUILD_DESCRIPTION}" \
      org.opencontainers.image.source="https://github.com/Checkmk/checkmk"

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD ["nc", "-z", "127.0.0.1", "6556"]
