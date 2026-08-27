ARG UPSTREAM_VERSION=0.7.0
FROM ghcr.io/openccu/openccu-proxy:0.7.0@sha256:4ea40c4b0bfa2cfdbb531d4eb2b721d532bc1964bb497a434f8f4aecc233c733
RUN echo "ea7277d9a07766f388f38852d6892df4ee59b28d5b62a13fd1b35894ca473006  /app/ha-proxy.js.gtpl" | sha256sum -c -
COPY --chmod=644 rootfs/app/ha-proxy.js.gtpl /app/ha-proxy.js.gtpl
RUN echo "a49423d9ee0746a463ed64c20aecb037e9a810b639ca115efdeb7c9df986279e  /app/ha-proxy.js.gtpl" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
