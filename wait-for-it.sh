#!/usr/bin/env bash

set -e

TIMEOUT=15
QUIET=0
PROGNAME=$(basename "$0")

echoerr() {
  if [ "$QUIET" -ne 1 ]; then
    printf "%s\n" "$*" 1>&2;
  fi
}

usage() {
  exitcode="$1"
  cat << USAGE >&2
Usage:
  $PROGNAME host:port [-t timeout] [-- command args]
  -q | --quiet                          Do not output any status messages
  -t TIMEOUT | --timeout=timeout        Timeout in seconds, zero for no timeout
  -- COMMAND ARGS                       Execute command with args after the test finishes
USAGE
  exit "$exitcode"
}

wait_for() {
  if [ "$TIMEOUT" -gt 0 ]; then
    echoerr "$PROGNAME: waiting $TIMEOUT seconds for $HOST:$PORT"
  else
    echoerr "$PROGNAME: waiting for $HOST:$PORT without a timeout"
  fi
  start_ts=$(date +%s)
  while :
  do
    if [ "$ISBUSY" -eq 1 ]; then
      nc -z "$HOST" "$PORT" && break
    else
      (echo > /dev/tcp/"$HOST"/"$PORT") >/dev/null 2>&1 && break
    fi
    sleep 1
  done
  end_ts=$(date +%s)
  echoerr "$PROGNAME: $HOST:$PORT is available after $((end_ts - start_ts)) seconds"
}

wait_for_wrapper() {
  if [ "$QUIET" -eq 1 ]; then
    timeout "$BUSYTIMEFLAG" "$TIMEOUT" "$0" "$HOST:$PORT" --quiet -- "$@" &
  else
    timeout "$BUSYTIMEFLAG" "$TIMEOUT" "$0" "$HOST:$PORT" -- "$@" &
  fi
  child=$!
  trap "kill -s TERM $child" INT TERM
  wait $child
}

while [ $# -gt 0 ]
do
  case "$1" in
    *:* )
    HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
    PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
    shift 1
    ;;
    -q | --quiet)
    QUIET=1
    shift 1
    ;;
    -t)
    TIMEOUT="$2"
    if [ "$TIMEOUT" = "" ]; then break; fi
    shift 2
    ;;
    --timeout=*)
    TIMEOUT=$(printf "%s\n" "$1"| cut -d = -f 2)
    shift 1
    ;;
    --)
    shift
    break
    ;;
    --help)
    usage 0
    ;;
    *)
    echoerr "Unknown argument: $1"
    usage 1
    ;;
  esac
done

if [ "$HOST" = "" ] || [ "$PORT" = "" ]; then
  echoerr "Error: you need to provide a host and port to test."
  usage 2
fi

ISBUSY=0
if command -v timeout >/dev/null 2>&1; then
  BUSYTIMEFLAG=""
elif command -v busybox >/dev/null 2>&1; then
  BUSYTIMEFLAG="-t"
  ISBUSY=1
else
  echoerr 'Error: you need "timeout" or "busybox" in your PATH.'
  exit 3
fi

if [ $# -gt 0 ]; then
  wait_for_wrapper "$@"
else
  wait_for
fi

exit 0
