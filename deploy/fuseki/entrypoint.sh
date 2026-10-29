#!/bin/sh
# Container entrypoint: start Fuseki (server with UI + localhost-only admin)
# on the read-only datasets baked into the image.
#
# Honoured environment:
#   JAVA_OPTIONS  JVM options (default -Xmx512m), passed as the launcher's JVM_ARGS
#   FUSEKI_PORT   HTTP port (default 3030)
# Fixed by the image: FUSEKI_HOME=/opt/fuseki, FUSEKI_BASE=/fuseki.
set -eu

FUSEKI_HOME=${FUSEKI_HOME:-/opt/fuseki}
FUSEKI_BASE=${FUSEKI_BASE:-/fuseki}
JAVA_OPTIONS=${JAVA_OPTIONS:--Xmx512m}
FUSEKI_PORT=${FUSEKI_PORT:-3030}

case "$FUSEKI_PORT" in
  ''|*[!0-9]*) echo "entrypoint: FUSEKI_PORT must be a number, got '$FUSEKI_PORT'" >&2; exit 1 ;;
esac

# The fuseki-server launcher reads JVM_ARGS (its own default is -Xmx4G).
export FUSEKI_HOME FUSEKI_BASE
export JVM_ARGS="$JAVA_OPTIONS"

# --shiro is explicit: the Shiro module is prepared before the admin module
# that would otherwise point it at $FUSEKI_BASE/shiro.ini, and without a Shiro
# file the admin API would not be restricted to localhost.
# Any extra arguments given to `docker run IMAGE ...` are appended.
exec "$FUSEKI_HOME/fuseki-server" \
  --config="$FUSEKI_BASE/config.ttl" \
  --shiro="$FUSEKI_BASE/shiro.ini" \
  --port="$FUSEKI_PORT" \
  "$@"
