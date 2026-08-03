#!/bin/sh
set -eu

echo "Setting up Homey Self-Hosted Server environment..."

read_option() {
    node -e '
        const fs = require("node:fs");
        const [path, fallback] = process.argv.slice(1);
        try {
            const options = JSON.parse(fs.readFileSync("/data/options.json", "utf8"));
            const value = path.split(".").reduce(
                (current, key) => current?.[key],
                options,
            );
            process.stdout.write(String(value ?? fallback));
        } catch {
            process.stdout.write(fallback);
        }
    ' "$1" "$2"
}

. /usr/local/bin/migration.sh

set_optional_env() {
    value="$(read_option "$1" "$3")"
    if [ -n "${value}" ]; then
        export "$2=${value}"
    else
        unset "$2"
    fi
}

set_boolean_env() {
    value="$(read_option "$1" "$3")"
    case "${value}" in
        1|true)
            export "$2=1"
            ;;
        *)
            unset "$2"
            ;;
    esac
}

export PORT_SERVER_HTTP="$(read_option port_server_http "${PORT_SERVER_HTTP:-4859}")"
export PORT_SERVER_HTTPS="$(read_option port_server_https "${PORT_SERVER_HTTPS:-4860}")"
export PORT_SERVER_BRIDGE_V1="$(read_option port_server_bridge_v1 "${PORT_SERVER_BRIDGE_V1:-4861}")"
export PORT_SERVER_BRIDGE_V2="$(read_option port_server_bridge_v2 "${PORT_SERVER_BRIDGE_V2:-4862}")"
export PORT_SERVER_WEBRTC="$(read_option extras.port_server_webrtc "${PORT_SERVER_WEBRTC:-8555}")"

echo "Configured ports: HTTP=${PORT_SERVER_HTTP}, HTTPS=${PORT_SERVER_HTTPS}, Bridge v1=${PORT_SERVER_BRIDGE_V1}, Bridge v2=${PORT_SERVER_BRIDGE_V2}, WebRTC=${PORT_SERVER_WEBRTC}"

homey_local_address="$(read_option extras.homey_local_address "${HOMEY_LOCAL_ADDRESS:-}")"
if [ -n "${homey_local_address}" ]; then
    export HOMEY_LOCAL_ADDRESS="${homey_local_address}"
    echo "Configured local address: ${HOMEY_LOCAL_ADDRESS}"
else
    unset HOMEY_LOCAL_ADDRESS
    echo "Local address: automatic detection"
fi

set_optional_env extras.matter_mdns_interfaces MATTER_MDNS_INTERFACES "${MATTER_MDNS_INTERFACES:-}"
set_boolean_env extras.homey_app_log_to_console HOMEY_APP_LOG_TO_CONSOLE "${HOMEY_APP_LOG_TO_CONSOLE:-}"
set_optional_env extras.homey_web_app_proxy_url HOMEY_WEB_APP_PROXY_URL "${HOMEY_WEB_APP_PROXY_URL:-}"
set_boolean_env extras.homey_app_devmode HOMEY_APP_DEVMODE "${HOMEY_APP_DEVMODE:-}"
set_optional_env extras.delegation_token_public_key DELEGATION_TOKEN_PUBLIC_KEY "${DELEGATION_TOKEN_PUBLIC_KEY:-}"
set_boolean_env remember_ingress_users HOMEY_INGRESS_REMEMBER_USERS false

storage_location="$(read_option storage_location data)"
share_storage_relative="$(normalize_share_relative \
    "$(read_option share_storage_directory homey-shs-config)")"
if ! migration_validate_relative "${share_storage_relative}"; then
    echo "ERROR: Invalid share_storage_directory" >&2
    exit 1
fi
HOMEY_SHARE_DATA_DIR="$(migration_share_directory "${share_storage_relative}")"

export_relative="$(normalize_share_relative \
    "$(read_option import_export.export_directory homey-shs-backups)")"
import_search_relative="$(normalize_share_relative \
    "$(read_option import_export.import_search_directory homey-shs-backups)")"
if migration_paths_overlap "${share_storage_relative}" "${export_relative}" ||
    migration_paths_overlap "${share_storage_relative}" "${import_search_relative}"; then
    echo "ERROR: Homey share storage must not overlap export or import search directories" >&2
    exit 1
fi

case "${storage_location}" in
    data) HOMEY_DATA_DIR="/data" ;;
    config) HOMEY_DATA_DIR="/config" ;;
    share) HOMEY_DATA_DIR="${HOMEY_SHARE_DATA_DIR}" ;;
    *)
        echo "ERROR: Unsupported storage_location: ${storage_location}" >&2
        exit 1
        ;;
esac
export HOMEY_DATA_DIR

mkdir -p "${HOMEY_DATA_DIR}" /homey

if ! reconcile_homey_storage \
    "${storage_location}" "${HOMEY_DATA_DIR}" "${HOMEY_SHARE_DATA_DIR}"; then
    echo "ERROR: Unable to reconcile Homey storage locations" >&2
    exit 1
fi

if ! migration_import "${HOMEY_DATA_DIR}" "${HOMEY_SHS_VERSION:-unknown}"; then
    echo "ERROR: Homey import failed; refusing to start with empty storage" >&2
    exit 1
fi

# Import may have populated an empty target. Keep all inactive locations empty.
for candidate in /data /config "${HOMEY_SHARE_DATA_DIR}"; do
    [ "${candidate}" = "${HOMEY_DATA_DIR}" ] && continue
    clear_homey_state "${candidate}"
done

mkdir -p "${HOMEY_DATA_DIR}/rrd"

# Homey expects its state in /homey/user.
if [ -L /homey/user ]; then
    target="$(readlink -f /homey/user 2>/dev/null || readlink /homey/user 2>/dev/null || true)"
    if [ "${target}" != "${HOMEY_DATA_DIR}" ]; then
        rm -f /homey/user
        ln -s "${HOMEY_DATA_DIR}" /homey/user
    fi
elif [ -d /homey/user ]; then
    # Migrate data created by an earlier image before replacing the directory.
    if [ -n "$(ls -A /homey/user 2>/dev/null)" ] &&
        ! directory_has_homey_state "${HOMEY_DATA_DIR}"; then
        echo "Migrating existing Homey data to ${HOMEY_DATA_DIR}..."
        cp -a /homey/user/. "${HOMEY_DATA_DIR}/"
    fi
    rm -rf /homey/user
    ln -s "${HOMEY_DATA_DIR}" /homey/user
elif [ ! -e /homey/user ]; then
    ln -s "${HOMEY_DATA_DIR}" /homey/user
fi

if ! touch /homey/user/.write-test 2>/dev/null; then
    echo "ERROR: /homey/user is not writable" >&2
    exit 1
fi
rm -f /homey/user/.write-test

echo "Persistent storage ready: /homey/user -> $(readlink /homey/user)"

if [ "$#" -eq 0 ]; then
    set -- \
        node \
        --conditions=typescript \
        --import=./apps/homey-shs/stdio-log.mts \
        apps/homey-shs/index.mts
fi

echo "Starting Homey Self-Hosted Server..."
"$@" &
homey_pid="$!"

echo "Starting experimental Homey ingress proxy..."
node /usr/local/bin/homey-ingress-proxy.mjs &
ingress_pid="$!"

shutdown() {
    trap - TERM INT
    kill -TERM "${ingress_pid}" 2>/dev/null || true
    wait "${ingress_pid}" 2>/dev/null || true
    echo "Stopping Homey before optional export..."
    kill -TERM "${homey_pid}" 2>/dev/null || true
    wait "${homey_pid}" 2>/dev/null || true
    migration_export "${HOMEY_DATA_DIR}" "${HOMEY_SHS_VERSION:-unknown}"
    exit 0
}

trap shutdown TERM INT

status=0
wait "${homey_pid}" || status="$?"
kill -TERM "${ingress_pid}" 2>/dev/null || true
wait "${ingress_pid}" 2>/dev/null || true
migration_export "${HOMEY_DATA_DIR}" "${HOMEY_SHS_VERSION:-unknown}"
exit "${status}"
