ARG UPSTREAM_VERSION=3.89.8.20260901-56ed0b2
FROM ghcr.io/openccu/openccu:3.89.8.20260901-56ed0b2@sha256:52b8ff49e668d10c0be7f8365fa0a6908b365b88eef0d56055332f632c51778a
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
