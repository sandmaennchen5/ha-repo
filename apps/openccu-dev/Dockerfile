ARG UPSTREAM_VERSION=3.89.8.20260911-87abd1d
FROM ghcr.io/openccu/openccu:3.89.8.20260911-87abd1d@sha256:02dad8844e7308cbe449fd705f46ba6c4ff4097b2601197f5f91ce93eaa35948
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
