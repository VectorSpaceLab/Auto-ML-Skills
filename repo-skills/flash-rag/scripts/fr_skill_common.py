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
    if text == "" or any(ch in text for ch in ":#{}[],&*?|-<>=!%@`\"'"):
        return repr(text)
    return text


def list_value(values: list[Any]) -> str:
    return "[" + ", ".join(scalar(v) for v in values) + "]"


def emit_yaml(data: dict[str, Any], indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            lines.extend(emit_yaml(value, indent + 2))
        elif isinstance(value, list):
            lines.append(f"{pad}{key}: {list_value(value)}")
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
    """Read top-level YAML scalars/lists without requiring PyYAML.

    This is intentionally small and only supports the generated smoke configs.
    Real FlashRAG runs should still use FlashRAG's Config class.
    """
    data: dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" ") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = parse_scalar(value)
    return data


def import_status(name: str) -> str:
    try:
        return getattr(importlib.import_module(name), "__file__", "imported")
    except Exception as exc:
        return f"import failed: {type(exc).__name__}: {exc}"


def pkg_version(name: str) -> str:
    dist_name = {"yaml": "PyYAML"}.get(name, name)
    try:
        return metadata.version(dist_name)
    except metadata.PackageNotFoundError:
        return "not installed"


def env_for(package_root: Path | None = None) -> dict[str, str]:
    env = os.environ.copy()
    paths: list[str] = []
    if package_root is not None:
        paths.append(str(package_root.resolve()))
    if env.get("PYTHONPATH"):
        paths.append(env["PYTHONPATH"])
    if paths:
        env["PYTHONPATH"] = os.pathsep.join(paths)
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


def check_env(package_root: Path | None, packages: list[str]) -> int:
    print(f"python: {sys.executable}")
    if package_root is not None:
        print(f"package_root: {package_root.resolve()}")
    errors: list[str] = []
    package_list = packages if "flashrag" in packages else ["flashrag"] + packages
    for pkg in package_list:
        status = import_status(pkg)
        print(f"{pkg}: {pkg_version(pkg)}; {status}")
        if status.startswith("import failed") and pkg in {"flashrag", "datasets", "yaml", "numpy"}:
            errors.append(f"{pkg} is required")
    print(f"valid: {str(not errors).lower()}")
    for error in errors:
        print(f"- {error}")
    return 0 if not errors else 1


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows
