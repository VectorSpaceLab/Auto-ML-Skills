#!/usr/bin/env python3
from __future__ import annotations

import importlib
import importlib.metadata as metadata
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or text.lower() in {"true", "false", "null"} or any(ch in text for ch in ":#{}[],&*?|-<>=!%@`\"'"):
        return repr(text)
    return text


def emit_yaml(data: dict[str, Any], indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            lines.extend(emit_yaml(value, indent + 2))
        elif isinstance(value, list):
            if not value:
                lines.append(f"{pad}{key}: []")
            else:
                lines.append(f"{pad}{key}:")
                for item in value:
                    lines.append(f"{pad}  - {scalar(item)}")
        else:
            lines.append(f"{pad}{key}: {scalar(value)}")
    return lines


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(emit_yaml(data)) + "\n", encoding="utf-8")
    print(path)


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "None", "~"}:
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item.strip()) for item in inner.split(",")]
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def read_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" ") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = parse_scalar(value)
    return data


def load_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    return data if isinstance(data, list) else [data]


def pkg_version(name: str) -> str:
    dist_name = {"yaml": "PyYAML"}.get(name, name)
    try:
        return metadata.version(dist_name)
    except metadata.PackageNotFoundError:
        return "not installed"


def import_status(name: str) -> str:
    try:
        return getattr(importlib.import_module(name), "__file__", "imported")
    except Exception as exc:
        return f"import failed: {type(exc).__name__}: {exc}"


def env_for(package_root: Path | None = None, extra_pythonpath: list[str] | None = None, use_v1: bool = False) -> dict[str, str]:
    env = os.environ.copy()
    paths: list[str] = []
    if package_root is not None:
        root = package_root.resolve()
        src = root / "src"
        paths.append(str(src if src.is_dir() else root))
    if extra_pythonpath:
        paths = [str(Path(p).resolve()) for p in extra_pythonpath] + paths
    if env.get("PYTHONPATH"):
        paths.append(env["PYTHONPATH"])
    if paths:
        env["PYTHONPATH"] = os.pathsep.join(paths)
    if use_v1:
        env["USE_V1"] = "1"
    else:
        env.pop("USE_V1", None)
    return env


def run_stream(cmd: list[str], cwd: Path, env: dict[str, str], log: Path | None = None) -> int:
    print("+ " + " ".join(cmd), flush=True)
    handle = None
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        handle = log.open("a", encoding="utf-8")
        handle.write("+ " + " ".join(cmd) + "\n")
    proc = subprocess.Popen(cmd, cwd=str(cwd), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert proc.stdout is not None
    try:
        for line in proc.stdout:
            print(line, end="")
            if handle:
                handle.write(line)
    finally:
        if handle:
            handle.close()
    return proc.wait()


def check_basic_env(package_root: Path | None = None, packages: list[str] | None = None) -> int:
    print(f"python: {sys.executable}")
    if package_root is not None:
        print(f"package_root: {package_root.resolve()}")
    errors: list[str] = []
    required = {"llamafactory", "torch", "transformers", "datasets"}
    package_list = packages or ["llamafactory", "torch", "transformers", "datasets", "accelerate", "peft", "trl"]
    if "llamafactory" not in package_list:
        package_list = ["llamafactory"] + package_list
    for pkg in package_list:
        status = import_status(pkg)
        print(f"{pkg}: {pkg_version(pkg)}; {status}")
        if status.startswith("import failed") and pkg in required:
            errors.append(f"{pkg} is required")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


def inspect_train_output(path: Path, adapter: bool = False) -> int:
    print(f"output_dir: {path.resolve()}")
    if not path.is_dir():
        print("valid: false")
        print("- output directory does not exist")
        return 1
    names = {p.name for p in path.iterdir()}
    for name in sorted(names):
        print(f"- {name}")
    ok = any(n.startswith("checkpoint-") for n in names) or bool(names.intersection({"config.json", "model.safetensors"}))
    if adapter:
        ok = ok or bool(names.intersection({"adapter_config.json", "adapter_model.safetensors"}))
    for filename in ["train_results.json", "all_results.json"]:
        p = path / filename
        if p.exists():
            print(f"{filename}: " + json.dumps(json.loads(p.read_text(encoding="utf-8")), ensure_ascii=False))
    log = path / "trainer_log.jsonl"
    if log.exists():
        rows = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
        print(f"trainer_log_rows: {len(rows)}")
        if rows:
            print("last_log: " + json.dumps(rows[-1], ensure_ascii=False))
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1
