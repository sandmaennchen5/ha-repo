ARG UPSTREAM_VERSION=3.89.11.20260918-0a5aa39
FROM ghcr.io/openccu/openccu:3.89.11.20260918-0a5aa39@sha256:094d17e26edc4a9f9cafc54eaee917ee5b1cb6d017feaabb6cd763f8c7582c98
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
