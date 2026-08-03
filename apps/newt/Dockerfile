# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
# Base image
ARG BUILD_FROM=ghcr.io/home-assistant/base:3.23
FROM $BUILD_FROM

ARG BUILD_VERSION
ARG BUILD_ARCH
ARG BUILD_DATE
ARG UPSTREAM_VERSION

LABEL \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.name="newt" \
    org.opencontainers.image.source=https://github.com/sandmaennchen5/ha-repo

# Install dependencies
RUN apk --no-cache add ca-certificates tzdata iputils curl socat

# Set newt version
ENV NEWT_VERSION="${UPSTREAM_VERSION}"

# Download the pre-built newt binary for the appropriate architecture
RUN \
  case "${BUILD_ARCH}" in \
    aarch64) NEWT_ARCH="arm64" ;; \
    amd64)   NEWT_ARCH="amd64" ;; \
    armv7)   NEWT_ARCH="armv7" ;; \
    armhf)   NEWT_ARCH="armv6" ;; \
    *)       echo "Unsupported arch: ${BUILD_ARCH}" && exit 1 ;; \
  esac \
  && curl -fsSL \
    "https://github.com/fosrl/newt/releases/download/${NEWT_VERSION}/newt_linux_${NEWT_ARCH}" \
    -o /usr/local/bin/newt \
  && chmod +x /usr/local/bin/newt

# Copy root filesystem
COPY rootfs /

RUN chmod 0755 \
    /usr/local/bin/newt-health-response \
    /etc/s6-overlay/s6-rc.d/newt-health-http/run

# Mark as HA add-on container
ENV NEWT_SYSTEM_SUBSTRATE="CONTAINER"

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["sh", "-c", "test -f /tmp/newt_healthy && pgrep -x newt >/dev/null"]
