FROM debian:bookworm-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# Official upstream Bookworm repository, including ARM64 packages.
RUN printf '#!/bin/sh\nexit 101\n' > /usr/sbin/policy-rc.d \
    && chmod 755 /usr/sbin/policy-rc.d \
    && apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates curl gnupg \
    && curl -fsSL https://luarvique.github.io/ppa/openwebrx-plus.gpg \
       | gpg --dearmor -o /usr/share/keyrings/openwebrx-plus.gpg \
    && echo 'deb [signed-by=/usr/share/keyrings/openwebrx-plus.gpg] https://luarvique.github.io/ppa/bookworm ./' \
       > /etc/apt/sources.list.d/openwebrx-plus.list \
    && apt-get update \
    && apt-get install --no-install-recommends -y openwebrx multimon-ng rtl-sdr tini \
    && command -v openwebrx \
    && command -v rtl_connector \
    && mv /usr/bin/rtl_connector /usr/bin/rtl_connector.real \
    && dpkg-query -W > /usr/share/openwebrx-build-packages.txt \
    && rm -rf /var/lib/apt/lists/*

COPY rootfs/ /
RUN chmod 755 /usr/local/bin/run-openwebrx /usr/bin/rtl_connector \
    && python3 /opt/ha-openwebrx/check_runtime.py

EXPOSE 8073
WORKDIR /tmp
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/run-openwebrx"]
