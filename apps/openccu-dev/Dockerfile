ARG UPSTREAM_VERSION=3.89.13.20261120-576ce4b
FROM ghcr.io/openccu/openccu:3.89.13.20261120-576ce4b@sha256:42e957869e92320d1b099017bafe4f4a60731deade45a3855a26f15b38ac4a95
RUN echo "e4aa50ade7dec5ea0c2678c33bd6b90157baec7086a3043df0914c8d9c4108c5  /bin/ha-proxy.js" | sha256sum -c -
COPY --chmod=755 rootfs/bin/ha-proxy.js /bin/ha-proxy.js
RUN echo "45296948ffe25454ee33ed7eadfe06e2dd53067cbedfe976a951f4f4c1b431a2  /bin/ha-proxy.js" | sha256sum -c -
LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"
