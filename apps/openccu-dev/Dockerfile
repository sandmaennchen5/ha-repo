ARG UPSTREAM_VERSION=3.89.8.20260826-dfd4f38
FROM ghcr.io/openccu/openccu:3.89.8.20260826-dfd4f38@sha256:1acedc3698d9a053b8b37d8779f2ed67a9c2727d1350dd4498f258d442fc5ea4
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "1c2d12f000f5c9923b8f8cda21bf18ea29f1927662d2a5effd3aa9b6ace3e6a4  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
