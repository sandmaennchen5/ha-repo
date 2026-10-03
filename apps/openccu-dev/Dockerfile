ARG UPSTREAM_VERSION=3.89.11.20261003-6dad8f7
FROM ghcr.io/openccu/openccu:3.89.11.20261003-6dad8f7@sha256:398cad5e30cafc09763e1d4bcb1949da0a3bc2817cd5a60cdad6f097aedcb130
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
