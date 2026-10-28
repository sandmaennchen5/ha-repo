ARG UPSTREAM_VERSION=3.89.11.20261028-a703ccc
FROM ghcr.io/openccu/openccu:3.89.11.20261028-a703ccc@sha256:4daacea9365f485ea4d3f792744b237c33bf78bc384ec63de4d639f7ea3e31fb
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
