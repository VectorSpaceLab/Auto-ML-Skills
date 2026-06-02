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


def emit(data: dict[str, Any], indent: int = 0) -> list[str]:
    out: list[str] = []
    pad = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            out.append(f"{pad}{key}:")
            out.extend(emit(value, indent + 2))
        else:
            out.append(f"{pad}{key}: {scalar(value)}")
    return out


def load_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    return data if isinstance(data, list) else [data]


def version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not installed"


def version_tuple(text: str) -> tuple[int, ...]:
    head = text.split("+", 1)[0]
    parts: list[int] = []
    for chunk in head.split("."):
        digits = "".join(ch for ch in chunk if ch.isdigit())
        if digits == "":
            break
        parts.append(int(digits))
    return tuple(parts)


def import_file(name: str) -> str:
    try:
        return getattr(importlib.import_module(name), "__file__", "imported")
    except Exception as exc:
        return f"import failed: {type(exc).__name__}: {exc}"


def prepend_pythonpath(paths: list[str] | None) -> None:
    if not paths:
        return
    for raw in reversed(paths):
        path = str(Path(raw).resolve())
        if path not in sys.path:
            sys.path.insert(0, path)
    existing = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = os.pathsep.join(paths + ([existing] if existing else []))


def env_for(package_root: Path | None = None, extra_pythonpath: list[str] | None = None) -> dict[str, str]:
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
    env.pop("USE_V1", None)
    return env


def run(cmd: list[str], cwd: Path, env: dict[str, str], log: Path | None) -> int:
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


def inspect_output(path: Path, adapter: bool = False) -> int:
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
    results = path / "train_results.json"
    if results.exists():
        print("train_results: " + json.dumps(json.loads(results.read_text(encoding="utf-8")), ensure_ascii=False))
    log = path / "trainer_log.jsonl"
    if log.exists():
        rows = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
        print(f"trainer_log_rows: {len(rows)}")
        if rows:
            print("last_log: " + json.dumps(rows[-1], ensure_ascii=False))
    print(f"valid: {str(ok).lower()}")
    return 0 if ok else 1


def check_env(package_root: Path | None = None, extra_pythonpath: list[str] | None = None) -> int:
    prepend_pythonpath(extra_pythonpath)
    print(f"python: {sys.executable}")
    if package_root is not None:
        print(f"package_root: {package_root.resolve()}")
    errors: list[str] = []
    warnings: list[str] = []
    for pkg in ["llamafactory", "torch", "transformers", "datasets", "accelerate", "peft", "trl", "torchao"]:
        status = import_file(pkg)
        print(f"{pkg}: {version(pkg)}; {status}")
        if pkg == "llamafactory" and status.startswith("import failed"):
            errors.append("llamafactory package is not importable")
        if pkg == "trl" and status.startswith("import failed"):
            errors.append("DPO default trainer imports trl; install an importable trl package")
    peft_ver = version("peft")
    torchao_ver = version("torchao")
    datasets_ver = version("datasets")
    if peft_ver.startswith("0.19") and torchao_ver not in {"not installed"}:
        warnings.append("LoRA may fail with peft 0.19 and old torchao; use peft<=0.18.1 or torchao>=0.16")
    if datasets_ver != "not installed" and not ((2, 16, 0) <= version_tuple(datasets_ver) <= (4, 0, 0)):
        warnings.append("default trainer version check requires datasets>=2.16.0,<=4.0.0; fix the version or use --disable-version-check for smoke tests")
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
