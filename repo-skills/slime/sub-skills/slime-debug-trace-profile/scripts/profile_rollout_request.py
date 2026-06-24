#!/usr/bin/env python3
"""Start or stop SGLang profiling for a slime rollout router."""

from __future__ import annotations

import argparse
import json
import urllib.request


def post_json(url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 - user-provided internal router
        return json.loads(resp.read().decode() or "{}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--router-url", required=True)
    parser.add_argument("--action", choices=["start", "stop"], default="start")
    parser.add_argument("--output-dir", default="/tmp/sglang_profile")
    parser.add_argument("--num-steps", type=int, default=3)
    args = parser.parse_args()

    endpoint = "/start_profile" if args.action == "start" else "/stop_profile"
    payload = {"output_dir": args.output_dir, "num_steps": args.num_steps}
    print(post_json(args.router_url.rstrip("/") + endpoint, payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
