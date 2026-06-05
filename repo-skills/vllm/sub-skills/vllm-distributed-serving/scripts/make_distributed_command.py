#!/usr/bin/env python3
"""Generate a vLLM distributed serve command."""

from __future__ import annotations

import argparse
import json
import shlex


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--pipeline-parallel-size", type=int, default=1)
    parser.add_argument("--data-parallel-size", type=int, default=None)
    parser.add_argument("--backend", choices=["ray", "mp", "uni", "external_launcher"], default=None)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--nnodes", type=int, default=None)
    parser.add_argument("--node-rank", type=int, default=None)
    parser.add_argument("--master-addr", default=None)
    parser.add_argument("--master-port", type=int, default=None)
    parser.add_argument("--enable-dbo", action="store_true")
    parser.add_argument("--dbo-decode-token-threshold", type=int, default=None)
    parser.add_argument("--dbo-prefill-token-threshold", type=int, default=None)
    parser.add_argument("--kv-connector", choices=["NixlConnector", "MooncakeConnector", "MoRIIOConnector"], default=None)
    parser.add_argument("--kv-role", choices=["kv_producer", "kv_consumer", "kv_both"], default=None)
    parser.add_argument("--kv-load-failure-policy", choices=["fail", "recompute"], default=None)
    parser.add_argument("--kv-extra-json", default=None, help="JSON object merged into kv_connector_extra_config.")
    parser.add_argument("--ray-serve", action="store_true", help="Print a note for Ray Serve LLM instead of pretending vllm serve is Ray Serve.")
    args = parser.parse_args()
    if args.ray_serve:
        print("# Ray Serve LLM uses a Ray Serve deployment file or Python app; use this command only for the underlying vllm serve shape.")
    cmd = ["vllm", "serve", args.model, "--host", args.host, "--port", str(args.port)]
    cmd += ["--tensor-parallel-size", str(args.tensor_parallel_size)]
    cmd += ["--pipeline-parallel-size", str(args.pipeline_parallel_size)]
    if args.data_parallel_size:
        cmd += ["--data-parallel-size", str(args.data_parallel_size)]
    if args.backend:
        cmd += ["--distributed-executor-backend", args.backend]
    if args.nnodes is not None:
        cmd += ["--nnodes", str(args.nnodes)]
    if args.node_rank is not None:
        cmd += ["--node-rank", str(args.node_rank)]
    if args.master_addr:
        cmd += ["--master-addr", args.master_addr]
    if args.master_port is not None:
        cmd += ["--master-port", str(args.master_port)]
    if args.enable_dbo:
        cmd += ["--enable-dbo"]
    if args.dbo_decode_token_threshold is not None:
        cmd += ["--dbo-decode-token-threshold", str(args.dbo_decode_token_threshold)]
    if args.dbo_prefill_token_threshold is not None:
        cmd += ["--dbo-prefill-token-threshold", str(args.dbo_prefill_token_threshold)]
    if args.kv_connector:
        if not args.kv_role:
            parser.error("--kv-role is required when --kv-connector is set")
        kv_config = {
            "kv_connector": args.kv_connector,
            "kv_role": args.kv_role,
        }
        if args.kv_load_failure_policy:
            kv_config["kv_load_failure_policy"] = args.kv_load_failure_policy
        if args.kv_extra_json:
            kv_config["kv_connector_extra_config"] = json.loads(args.kv_extra_json)
        cmd += ["--kv-transfer-config", json.dumps(kv_config, separators=(",", ":"))]
    print(" ".join(shlex.quote(part) for part in cmd))


if __name__ == "__main__":
    main()
