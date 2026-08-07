ARG BUILD_ARCH=amd64
FROM ghcr.io/home-assistant/${BUILD_ARCH}-base:3.23

ARG BUILD_VERSION
ARG BUILD_ARCH
ARG UPSTREAM_VERSION=1.8.2

LABEL \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.arch="${BUILD_ARCH}" \
  io.hass.type="addon" \
  io.hass.name="olm" \
  org.opencontainers.image.source="https://github.com/fosrl/olm"

RUN apk --no-cache add ca-certificates curl iputils socat tzdata

RUN case "${BUILD_ARCH}" in \
      aarch64) asset="olm_linux_arm64" ;; \
      amd64) asset="olm_linux_amd64" ;; \
      *) echo "Unsupported architecture: ${BUILD_ARCH}" >&2; exit 1 ;; \
    esac \
    && curl -fsSL "https://github.com/fosrl/olm/releases/download/${UPSTREAM_VERSION}/${asset}" -o /usr/local/bin/olm \
    && chmod 0755 /usr/local/bin/olm

COPY rootfs /

RUN chmod 0755 \
    /usr/local/bin/olm-health-response \
    /etc/s6-overlay/s6-rc.d/olm-health/run

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["wget", "-q", "--spider", "http://127.0.0.1:8096/health"]
