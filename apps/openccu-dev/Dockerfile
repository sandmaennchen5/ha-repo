ARG UPSTREAM_VERSION=3.89.11.20260922-54354e5
FROM ghcr.io/openccu/openccu:3.89.11.20260922-54354e5@sha256:2cbdd071716adcdcc292bcd74756a25c1092bb998b016bdd1ef822846570b200
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
