"""Shared helpers for vLLM repo skill scripts."""

from __future__ import annotations

import importlib
import importlib.metadata as metadata
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def json_dump(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def package_version(name: str = "vllm") -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def console_scripts(name: str = "vllm") -> list[str]:
    return [
        f"{ep.name}={ep.value}"
        for ep in metadata.entry_points(group="console_scripts")
        if ep.name == name
    ]


def import_status(module: str) -> dict[str, Any]:
    try:
        importlib.import_module(module)
        return {"module": module, "ok": True}
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {
            "module": module,
            "ok": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }


def command_exists(command: str) -> bool:
    return any(
        os.access(Path(path) / command, os.X_OK)
        for path in os.environ.get("PATH", "").split(os.pathsep)
        if path
    )


def run_short_command(argv: list[str], timeout: float = 10.0) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            argv,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        return {
            "argv": argv,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {
            "argv": argv,
            "returncode": None,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }


def find_free_port(host: str = "127.0.0.1") -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def http_json(
    url: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 10.0,
) -> dict[str, Any]:
    body = None
    merged_headers = {"Content-Type": "application/json"}
    if headers:
        merged_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    req = Request(url, data=body, headers=merged_headers, method=method)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                parsed: Any = json.loads(raw)
            except json.JSONDecodeError:
                parsed = raw
            return {"ok": True, "status": resp.status, "body": parsed}
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw
        return {"ok": False, "status": exc.code, "body": parsed}
    except URLError as exc:
        return {"ok": False, "status": None, "error": str(exc)}


def wait_for_http(url: str, timeout_s: float = 120.0, interval_s: float = 1.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        result = http_json(url, timeout=interval_s)
        if result.get("ok"):
            return True
        time.sleep(interval_s)
    return False


def write_json(path: str | Path, data: Any) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json_dump(data) + "\n", encoding="utf-8")


def print_json(data: Any) -> None:
    sys.stdout.write(json_dump(data) + "\n")
