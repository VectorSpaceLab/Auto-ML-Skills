#!/usr/bin/env python3
"""Validate a small vLLM serve YAML config without loading a model."""

from __future__ import annotations

import argparse
from pathlib import Path

from vllm_skill_common import print_json

ALLOWED_TOP_LEVEL = {
    "model",
    "served-model-name",
    "host",
    "port",
    "uvicorn-log-level",
    "dtype",
    "max-model-len",
    "tensor-parallel-size",
    "pipeline-parallel-size",
    "data-parallel-size",
    "gpu-memory-utilization",
    "quantization",
    "enable-lora",
    "lora-modules",
    "max-loras",
    "max-lora-rank",
    "generation-config",
    "chat-template",
    "trust-remote-code",
    "disable-log-requests",
    "enable-prefix-caching",
    "speculative-config",
    "api-key",
}


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except Exception as exc:
        return load_flat_yaml(path, exc)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("Config must be a YAML mapping.")
    return data


def load_flat_yaml(path: Path, original_exc: Exception) -> dict:
    data = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise SystemExit(
                f"PyYAML is unavailable ({original_exc}); fallback parser only "
                f"supports flat key: value lines. Invalid line {lineno}: {raw}"
            )
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.lower() in {"true", "false"}:
            parsed = value.lower() == "true"
        elif value.startswith('"') and value.endswith('"'):
            parsed = value[1:-1]
        else:
            try:
                parsed = int(value)
            except ValueError:
                try:
                    parsed = float(value)
                except ValueError:
                    parsed = value
        data[key] = parsed
    return data


def validate(data: dict) -> dict:
    issues = []
    warnings = []
    if not data.get("model"):
        issues.append("Missing required 'model'.")
    if "port" in data:
        try:
            port = int(data["port"])
            if port < 1 or port > 65535:
                issues.append("'port' must be between 1 and 65535.")
        except Exception:
            issues.append("'port' must be an integer.")
    for key in ["tensor-parallel-size", "pipeline-parallel-size", "data-parallel-size"]:
        if key in data and int(data[key]) < 1:
            issues.append(f"'{key}' must be >= 1.")
    if "gpu-memory-utilization" in data:
        value = float(data["gpu-memory-utilization"])
        if value <= 0 or value > 1:
            issues.append("'gpu-memory-utilization' must be in (0, 1].")
    unknown = sorted(set(data) - ALLOWED_TOP_LEVEL)
    if unknown:
        warnings.append(f"Unknown keys for this validator: {unknown}")
    return {"valid": not issues, "issues": issues, "warnings": warnings, "config": data}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="Path to YAML config.")
    parser.add_argument("--json", action="store_true", help="Print JSON.")
    args = parser.parse_args()
    result = validate(load_yaml(Path(args.config)))
    if args.json:
        print_json(result)
    else:
        print(f"valid: {result['valid']}")
        for issue in result["issues"]:
            print(f"issue: {issue}")
        for warning in result["warnings"]:
            print(f"warning: {warning}")
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
