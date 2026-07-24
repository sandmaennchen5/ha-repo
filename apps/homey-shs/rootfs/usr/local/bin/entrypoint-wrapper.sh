#!/bin/sh
set -eu

echo "Setting up Homey Self-Hosted Server environment..."

mkdir -p /data/rrd /homey

# Home Assistant persists /data, while Homey expects its state in /homey/user.
if [ -L /homey/user ]; then
    target="$(readlink -f /homey/user 2>/dev/null || readlink /homey/user 2>/dev/null || true)"
    if [ "${target}" != "/data" ]; then
        rm -f /homey/user
        ln -s /data /homey/user
    fi
elif [ -d /homey/user ]; then
    # Migrate data created by an earlier image before replacing the directory.
    if [ -n "$(ls -A /homey/user 2>/dev/null)" ] && [ -z "$(ls -A /data 2>/dev/null)" ]; then
        echo "Migrating existing Homey data to /data..."
        cp -a /homey/user/. /data/
    fi
    rm -rf /homey/user
    ln -s /data /homey/user
elif [ ! -e /homey/user ]; then
    ln -s /data /homey/user
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
exec "$@"
