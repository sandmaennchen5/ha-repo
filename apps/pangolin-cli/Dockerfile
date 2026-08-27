ARG BUILD_ARCH=amd64
FROM ghcr.io/home-assistant/${BUILD_ARCH}-base:3.23

ARG BUILD_VERSION
ARG BUILD_ARCH
ARG UPSTREAM_VERSION=0.16.0

LABEL \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.arch="${BUILD_ARCH}" \
  io.hass.type="addon" \
  io.hass.name="pangolin-cli" \
  org.opencontainers.image.source="https://github.com/fosrl/cli"

RUN apk --no-cache add ca-certificates curl iputils tzdata

RUN case "${BUILD_ARCH}" in \
      aarch64) asset="pangolin-cli_linux_arm64" ;; \
      amd64) asset="pangolin-cli_linux_amd64" ;; \
      *) echo "Unsupported architecture: ${BUILD_ARCH}" >&2; exit 1 ;; \
    esac \
    && curl -fsSL "https://github.com/fosrl/cli/releases/download/${UPSTREAM_VERSION}/${asset}" -o /usr/local/bin/pangolin-cli \
    && chmod 0755 /usr/local/bin/pangolin-cli

COPY rootfs /

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD ["sh", "-c", "pgrep -x pangolin-cli >/dev/null"]
