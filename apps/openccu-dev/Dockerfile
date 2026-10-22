ARG UPSTREAM_VERSION=3.89.11.20261022-5569aa3
FROM ghcr.io/openccu/openccu:3.89.11.20261022-5569aa3@sha256:52ccff83b7eb4915331801693be870fbdc8939b44ca34ab20fa24141b1028693
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
