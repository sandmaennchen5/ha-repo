ARG UPSTREAM_VERSION=3.89.14.20261122-d7a047d
FROM ghcr.io/openccu/openccu:3.89.14.20261122-d7a047d@sha256:4cf943773c9ffee13ff9ec820df15436e9c20f1935fbf8dddc2dfbe894dc4f65
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
