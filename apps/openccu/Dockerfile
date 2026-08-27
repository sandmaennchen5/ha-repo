ARG UPSTREAM_VERSION=3.89.8.20260719
FROM ghcr.io/openccu/openccu:3.89.8.20260719@sha256:b2de2ff6e8e0f3d323714aecf20fb4c634f6aa114fd3e8404bae24f8e84db9b4
RUN echo "51d4e1ab0250fb25f950e2f83499c9f2bdc04ee3ac9d783cb0b8007c29fc56d0  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "1c2d12f000f5c9923b8f8cda21bf18ea29f1927662d2a5effd3aa9b6ace3e6a4  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
