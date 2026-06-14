#!/usr/bin/env python3
"""Validate observability flags for SGLang command plans."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SGLang observability config choices.")
    parser.add_argument("--enable-metrics", action="store_true")
    parser.add_argument("--prometheus-port", type=int)
    parser.add_argument("--enable-trace", action="store_true")
    parser.add_argument("--otlp-traces-endpoint")
    parser.add_argument("--log-requests", action="store_true")
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    issues = []
    if args.enable_trace and not args.otlp_traces_endpoint:
        issues.append("--enable-trace should include --otlp-traces-endpoint")
    if args.prometheus_port is not None and not (1 <= args.prometheus_port <= 65535):
        issues.append("--prometheus-port must be 1..65535")
    if args.production and args.log_requests:
        issues.append("production request logging needs explicit retention/redaction review")
    print(json.dumps({"ok": not issues, "issues": issues}, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
