#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Start a vLLM OpenAI-compatible server and record PID/log files.

Usage:
  start_openai_server.sh --model MODEL --out-dir DIR [--host HOST] [--port PORT] [--extra-arg ARG ...]

The script does not choose a model for you. Use a public model id such as
Qwen/Qwen3-0.6B for small generation smoke tests when available.
EOF
}

MODEL=""
OUT_DIR=""
HOST="127.0.0.1"
PORT="8000"
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) MODEL="$2"; shift 2 ;;
    --out-dir) OUT_DIR="$2"; shift 2 ;;
    --host) HOST="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    --extra-arg) EXTRA_ARGS+=("$2"); shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$MODEL" || -z "$OUT_DIR" ]]; then
  usage >&2
  exit 2
fi

mkdir -p "$OUT_DIR"
LOG="$OUT_DIR/server.log"
PID_FILE="$OUT_DIR/server.pid"
CMD_FILE="$OUT_DIR/server.cmd"

printf '%q ' vllm serve "$MODEL" --host "$HOST" --port "$PORT" "${EXTRA_ARGS[@]}" > "$CMD_FILE"
printf '\n' >> "$CMD_FILE"

nohup vllm serve "$MODEL" --host "$HOST" --port "$PORT" "${EXTRA_ARGS[@]}" > "$LOG" 2>&1 &
PID=$!
echo "$PID" > "$PID_FILE"
echo "pid=$PID"
echo "log=$LOG"
echo "base_url=http://$HOST:$PORT"
