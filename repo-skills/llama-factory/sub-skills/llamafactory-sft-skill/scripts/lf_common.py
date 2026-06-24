#!/usr/bin/env python3
"""Shared helpers for LLaMA-Factory skill scripts."""

from __future__ import annotations

import importlib
import importlib.metadata as metadata
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or text.lower() in {"true", "false", "null"}:
        return repr(text)
    if any(ch in text for ch in ":#{}[],&*?|-<>=!%@`\"'"):
        return repr(text)
    return text


def emit_yaml(data: dict[str, Any], indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            lines.extend(emit_yaml(value, indent + 2))
        else:
            lines.append(f"{pad}{key}: {yaml_scalar(value)}")
    return lines


def parse_scalar(text: str) -> Any:
    text = text.strip()
    if text in {"", "null", "None", "~"}:
        return None
    if text in {"true", "True"}:
        return True
    if text in {"false", "False"}:
        return False
    if (text.startswith("'") and text.endswith("'")) or (text.startswith('"') and text.endswith('"')):
        return text[1:-1]
    try:
        if any(ch in text for ch in ".eE"):
            return float(text)
        return int(text)
    except ValueError:
        return text.split(" #", 1)[0].strip()


def simple_yaml_load(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = parse_scalar(value)
    return root


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        data = simple_yaml_load(path)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def load_json_or_jsonl(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return [data]
    raise ValueError(f"unsupported JSON root in {path}")


def package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not installed"


def import_status(name: str) -> str:
    try:
        module = importlib.import_module(name)
    except Exception as exc:
        return f"import failed: {type(exc).__name__}: {exc}"
    return getattr(module, "__file__", "imported")


def prepend_pythonpath(paths: list[str] | None) -> None:
    if not paths:
        return
    for raw in reversed(paths):
        path = str(Path(raw).resolve())
        if path not in sys.path:
            sys.path.insert(0, path)
    existing = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = os.pathsep.join(paths + ([existing] if existing else []))


def build_env(package_root: Path | None = None, use_v1: bool = False, extra_pythonpath: list[str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    paths: list[str] = []
    if package_root is not None:
        root = package_root.resolve()
        src = root / "src"
        paths.append(str(src if src.is_dir() else root))
    if extra_pythonpath:
        paths = extra_pythonpath + paths
    if env.get("PYTHONPATH"):
        paths.append(env["PYTHONPATH"])
    if paths:
        env["PYTHONPATH"] = os.pathsep.join(paths)
    if use_v1:
        env["USE_V1"] = "1"
    return env


def run_streaming(cmd: list[str], cwd: Path, env: dict[str, str], log: Path | None) -> int:
    log_handle = None
    if log is not None:
        log.parent.mkdir(parents=True, exist_ok=True)
        log_handle = log.open("a", encoding="utf-8")
        log_handle.write("+ " + " ".join(cmd) + "\n")
        log_handle.flush()
    print("+ " + " ".join(cmd), flush=True)
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None
    try:
        for line in proc.stdout:
            print(line, end="")
            if log_handle:
                log_handle.write(line)
    finally:
        if log_handle:
            log_handle.close()
    return proc.wait()


def check_output_dir(path: Path, adapter: bool = False) -> int:
    print(f"output_dir: {path.resolve()}")
    if not path.is_dir():
        print("valid: false")
        print("- output directory does not exist")
        return 1
    names = {p.name for p in path.iterdir()}
    for name in sorted(names):
        print(f"- {name}")
    if adapter:
        ok = bool(names.intersection({"adapter_config.json", "adapter_model.safetensors", "adapter_model.bin"}))
    else:
        ok = bool(names.intersection({"config.json", "model.safetensors", "pytorch_model.bin"})) or any(
            name.startswith("checkpoint-") for name in names
        )
    if not ok:
        print("valid: false")
        print("- expected model, adapter, or checkpoint artifact not found")
        return 1
    log = path / "trainer_log.jsonl"
    if log.exists():
        rows = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
        print(f"trainer_log_rows: {len(rows)}")
        if rows:
            print("last_log: " + json.dumps(rows[-1], ensure_ascii=False))
    print("valid: true")
    return 0


def main_env_check(
    package_root: Path | None = None, require_v0: bool = False, require_v1: bool = False, extra_pythonpath: list[str] | None = None
) -> int:
    prepend_pythonpath(extra_pythonpath)
    print(f"python: {sys.executable}")
    if package_root is not None:
        print(f"package_root: {package_root.resolve()}")
        print(f"package_root_exists: {package_root.is_dir()}")
    print(f"cuda_visible_devices: {os.getenv('CUDA_VISIBLE_DEVICES', '') or 'unset'}")
    for package in ["torch", "transformers", "datasets", "accelerate", "peft", "trl", "torchdata", "torchao"]:
        print(f"{package}: {package_version(package)}; {import_status(package)}")
    errors: list[str] = []
    warnings: list[str] = []
    if "import failed" in import_status("llamafactory"):
        errors.append("llamafactory package is not importable")
    if require_v1 and "import failed" in import_status("torchdata"):
        errors.append("v1 SFT/RM requires importable torchdata")
    if require_v0 and "import failed" in import_status("trl"):
        errors.append("default v0 trainer imports trl at model loader import time")
    if require_v0:
        peft_ver = package_version("peft")
        torchao_ver = package_version("torchao")
        if peft_ver.startswith("0.19") and torchao_ver not in {"not installed"}:
            warnings.append("peft 0.19 with old torchao can break LoRA injection; use peft<=0.18.1 or torchao>=0.16")
    peft_ver = package_version("peft")
    torchao_ver = package_version("torchao")
    if require_v1 and peft_ver.startswith("0.19") and torchao_ver not in {"not installed"}:
        warnings.append("LoRA may fail with peft 0.19 and old torchao; full tuning is unaffected")
    if errors:
        print("valid: false")
        for error in errors:
            print(f"- {error}")
        return 1
    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"- {warning}")
    print("valid: true")
    return 0
