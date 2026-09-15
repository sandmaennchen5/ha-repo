ARG UPSTREAM_VERSION=3.89.9.20260915-0e13407
FROM ghcr.io/openccu/openccu:3.89.9.20260915-0e13407@sha256:9c382b37dcbf11f06de26e9fbe1ff8e8a0c48b67c1562b971565955c14916419
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
