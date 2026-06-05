#!/usr/bin/env python3
"""Start a vLLM server, optionally wait for health and run a smoke check."""

from __future__ import annotations

import argparse
import subprocess
import time
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(ROOT))
from vllm_skill_common import find_free_port, http_json, print_json, wait_for_http  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0, help="0 chooses a free port.")
    parser.add_argument("--arg", action="append", default=[], help="Extra vllm serve arg; repeat.")
    parser.add_argument("--wait", action="store_true")
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    port = args.port or find_free_port(args.host)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    log = out / "server.log"
    pid_file = out / "server.pid"
    cmd = ["vllm", "serve", args.model, "--host", args.host, "--port", str(port)] + args.arg
    (out / "server.cmd").write_text(" ".join(cmd) + "\n", encoding="utf-8")
    handle = log.open("w", encoding="utf-8")
    proc = subprocess.Popen(cmd, stdout=handle, stderr=subprocess.STDOUT, text=True, start_new_session=True)
    pid_file.write_text(str(proc.pid) + "\n", encoding="utf-8")
    base_url = f"http://{args.host}:{port}"
    result = {"pid": proc.pid, "base_url": base_url, "log": str(log), "cmd": cmd}
    if args.wait:
        ok = wait_for_http(f"{base_url}/health", timeout_s=args.timeout)
        result["health_ready"] = ok
        result["models"] = http_json(f"{base_url}/v1/models") if ok else None
        if not ok:
            proc.terminate()
            time.sleep(2)
    if args.json:
        print_json(result)
    else:
        print(f"pid={proc.pid}")
        print(f"base_url={base_url}")
        print(f"log={log}")


if __name__ == "__main__":
    main()
