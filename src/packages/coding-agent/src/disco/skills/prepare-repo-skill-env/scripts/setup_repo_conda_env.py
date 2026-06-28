#!/usr/bin/env python3
"""
Create or reuse an isolated Python environment, install a local repo package,
and verify it.

This helper is intentionally conservative:
  * It never deletes an existing prefix.
  * It never installs into conda base.
  * It writes a private JSON report with commands, facts, warnings, failures,
    and a handoff block for create-repo-skill.
  * It exits non-zero unless verification proves the environment is usable.

The script uses only the Python standard library so it can run before the target
environment exists. Conda is preferred when available; otherwise the helper can
fall back to `venv` using the host Python that launched this script.
"""
from __future__ import annotations

import argparse
import configparser
import datetime as _dt
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import traceback
import urllib.parse
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover - Python <3.11 fallback.
    tomllib = None  # type: ignore[assignment]


EXCLUDED_TOP_LEVEL = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "data",
    "dist",
    "doc",
    "docs",
    "example",
    "examples",
    "notebook",
    "notebooks",
    "scripts",
    "site",
    "tests",
    "test",
    "tools",
    "venv",
}


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def command_text(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 300,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    started = utc_now()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "command": command_text(cmd),
            "cwd": str(cwd) if cwd else None,
            "started_at": started,
            "finished_at": utc_now(),
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command_text(cmd),
            "cwd": str(cwd) if cwd else None,
            "started_at": started,
            "finished_at": utc_now(),
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "timed_out": True,
            "timeout_seconds": timeout,
        }
    except Exception as exc:  # Keep reporting useful even on unexpected host errors.
        return {
            "command": command_text(cmd),
            "cwd": str(cwd) if cwd else None,
            "started_at": started,
            "finished_at": utc_now(),
            "returncode": None,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
            "exception": traceback.format_exc(),
            "timed_out": False,
        }


def ok(result: dict[str, Any]) -> bool:
    return result.get("returncode") == 0 and not result.get("timed_out")


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_pyproject(repo: Path) -> dict[str, Any]:
    path = repo / "pyproject.toml"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    if tomllib is not None:
        try:
            with path.open("rb") as fh:
                return tomllib.load(fh)
        except Exception:
            pass

    # Small fallback for older host Python. This is not a full TOML parser, but
    # it catches the fields most useful for planning.
    project: dict[str, Any] = {}
    in_project = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_project = line == "[project]"
            continue
        if not in_project or "=" not in line:
            continue
        key, value = [p.strip() for p in line.split("=", 1)]
        if key in {"name", "requires-python"}:
            m = re.match(r"""['"]([^'"]+)['"]""", value)
            if m:
                project[key] = m.group(1)
    return {"project": project} if project else {}


def load_setup_cfg(repo: Path) -> dict[str, Any]:
    path = repo / "setup.cfg"
    if not path.exists():
        return {}
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    data: dict[str, Any] = {}
    if parser.has_section("metadata") and parser.has_option("metadata", "name"):
        data["name"] = parser.get("metadata", "name").strip()
    if parser.has_section("options") and parser.has_option("options", "python_requires"):
        data["requires_python"] = parser.get("options", "python_requires").strip()
    return data


def load_setup_py_name(repo: Path) -> str | None:
    path = repo / "setup.py"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    patterns = [
        r"setup\s*\([^)]*?name\s*=\s*['\"]([^'\"]+)['\"]",
        r"name\s*=\s*['\"]([^'\"]+)['\"]",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.DOTALL)
        if match:
            return match.group(1).strip()
    return None


def normalize_dist_to_import(name: str) -> str:
    return re.sub(r"[-.]+", "_", name).strip("_")


def python_major_minor(version: str) -> str:
    parts = version.split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else version


def is_identifier(name: str) -> bool:
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name))


def discover_import_roots(repo: Path, dist_names: list[str]) -> list[str]:
    candidates: list[str] = []
    roots = [repo]
    if (repo / "src").is_dir():
        roots.insert(0, repo / "src")

    def add(name: str) -> None:
        if is_identifier(name) and name not in candidates and name not in EXCLUDED_TOP_LEVEL:
            candidates.append(name)

    for root in roots:
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir(), key=lambda p: p.name):
            if child.name.startswith(".") or child.name in EXCLUDED_TOP_LEVEL:
                continue
            if child.is_dir() and (child / "__init__.py").exists():
                add(child.name)
            elif child.is_file() and child.suffix == ".py" and child.stem != "setup":
                add(child.stem)

    normalized = [normalize_dist_to_import(name) for name in dist_names]
    preferred = [name for name in candidates if name in normalized]
    return preferred or candidates


def inspect_repo(repo: Path, explicit_packages: list[str], explicit_imports: list[str]) -> dict[str, Any]:
    pyproject = load_pyproject(repo)
    setup_cfg = load_setup_cfg(repo)
    setup_py_name = load_setup_py_name(repo)

    project = pyproject.get("project", {}) if isinstance(pyproject, dict) else {}
    tool_poetry = (
        pyproject.get("tool", {}).get("poetry", {})
        if isinstance(pyproject.get("tool"), dict)
        else {}
    )

    metadata_names: list[str] = []
    for name in (
        project.get("name"),
        setup_cfg.get("name"),
        tool_poetry.get("name") if isinstance(tool_poetry, dict) else None,
        setup_py_name,
    ):
        if isinstance(name, str) and name.strip() and name.strip() not in metadata_names:
            metadata_names.append(name.strip())

    package_names = list(dict.fromkeys([*explicit_packages, *metadata_names]))
    import_roots = list(dict.fromkeys([*explicit_imports, *discover_import_roots(repo, package_names)]))

    optional_deps = project.get("optional-dependencies", {})
    if not isinstance(optional_deps, dict):
        optional_deps = {}

    scripts: dict[str, Any] = {}
    for key in ("scripts", "gui-scripts"):
        value = project.get(key, {})
        if isinstance(value, dict):
            scripts[key] = value

    return {
        "pyproject_present": (repo / "pyproject.toml").exists(),
        "setup_cfg_present": (repo / "setup.cfg").exists(),
        "setup_py_present": (repo / "setup.py").exists(),
        "metadata_names": metadata_names,
        "package_names": package_names,
        "import_roots": import_roots,
        "requires_python": project.get("requires-python") or setup_cfg.get("requires_python"),
        "dependencies": project.get("dependencies", []),
        "optional_dependency_groups": sorted(optional_deps.keys()),
        "entry_points": scripts,
        "build_backend": pyproject.get("build-system", {}).get("build-backend")
        if isinstance(pyproject.get("build-system"), dict)
        else None,
    }


def find_python(prefix: Path) -> Path | None:
    candidates = [
        prefix / "bin" / "python",
        prefix / "bin" / "python3",
        prefix / "python",
        prefix / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists() and os.access(candidate, os.X_OK):
            return candidate
    return None


def find_conda(conda_exe: str) -> str | None:
    discovered = shutil.which(conda_exe)
    if discovered:
        return discovered
    explicit = Path(conda_exe).expanduser()
    if explicit.exists():
        return str(explicit)
    return None


def host_probe(conda_exe: str | None) -> dict[str, Any]:
    probe: dict[str, Any] = {
        "os": platform.platform(),
        "system": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "host_python": sys.version.replace("\n", " "),
        "host_python_executable": sys.executable,
        "conda_executable": conda_exe,
    }

    commands: dict[str, list[str]] = {
        "nvidia_smi": ["nvidia-smi"],
        "nvcc_version": ["nvcc", "--version"],
        "rocm_smi": ["rocm-smi", "--showproductname"],
        "rocminfo": ["rocminfo"],
    }
    if conda_exe:
        commands["conda_version"] = [conda_exe, "--version"]
        commands["conda_info_json"] = [conda_exe, "info", "--json"]
    else:
        probe["conda_version"] = None
        probe["conda_info_json"] = None

    for name, cmd in commands.items():
        if shutil.which(cmd[0]):
            timeout = 15 if name in {"nvidia_smi", "rocminfo"} else 8
            result = run(cmd, timeout=timeout)
            probe[name] = {
                "returncode": result["returncode"],
                "stdout": result["stdout"],
                "stderr": result["stderr"],
                "timed_out": result["timed_out"],
            }
        else:
            probe[name] = None

    if shutil.which("nvidia-smi"):
        query_with_cc = run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version,compute_cap",
                "--format=csv,noheader,nounits",
            ],
            timeout=8,
        )
        if ok(query_with_cc):
            probe["nvidia_query"] = {
                "returncode": query_with_cc["returncode"],
                "stdout": query_with_cc["stdout"],
                "stderr": query_with_cc["stderr"],
                "timed_out": query_with_cc["timed_out"],
                "fields": ["name", "memory.total", "driver_version", "compute_cap"],
            }
        else:
            query_without_cc = run(
                [
                    "nvidia-smi",
                    "--query-gpu=name,memory.total,driver_version",
                    "--format=csv,noheader,nounits",
                ],
                timeout=8,
            )
            probe["nvidia_query"] = {
                "returncode": query_without_cc["returncode"],
                "stdout": query_without_cc["stdout"],
                "stderr": query_without_cc["stderr"],
                "timed_out": query_without_cc["timed_out"],
                "fields": ["name", "memory.total", "driver_version"],
                "fallback_reason": query_with_cc["stdout"] or query_with_cc["stderr"],
            }
    else:
        probe["nvidia_query"] = None

    info = probe.get("conda_info_json")
    if isinstance(info, dict) and info.get("stdout"):
        try:
            parsed = json.loads(info["stdout"])
            probe["conda_root_prefix"] = (
                parsed.get("root_prefix")
                or parsed.get("root_prefix_name")
                or parsed.get("default_prefix")
            )
        except Exception:
            probe["conda_root_prefix"] = None

    return probe


def make_install_target(repo: Path, extras: list[str]) -> str:
    if not extras:
        return str(repo)
    return f"{repo}[{','.join(extras)}]"


def pip_install_command(python: Path, install_args: str) -> list[str]:
    return [str(python), "-m", "pip", "install", *shlex.split(install_args)]


def python_json(python: Path, code: str, args: list[str] | None = None, timeout: int = 120) -> dict[str, Any]:
    cmd = [str(python), "-c", code, *(args or [])]
    result = run(cmd, timeout=timeout)
    parsed: Any = None
    if result.get("stdout"):
        try:
            parsed = json.loads(result["stdout"])
        except Exception:
            parsed = None
    result["json"] = parsed
    return result


def discover_repo_distributions(python: Path, repo: Path) -> dict[str, Any]:
    code = r"""
import importlib.metadata as md
import json
import pathlib
import sys
import urllib.parse

repo = pathlib.Path(sys.argv[1]).resolve()
matches = []
for dist in md.distributions():
    name = dist.metadata.get("Name")
    version = dist.version
    direct = None
    try:
        direct = dist.read_text("direct_url.json")
    except Exception:
        direct = None
    if direct:
        try:
            data = json.loads(direct)
            url = data.get("url")
            if url and url.startswith("file:"):
                path = pathlib.Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).resolve()
                if path == repo:
                    matches.append({
                        "name": name,
                        "version": version,
                        "direct_url": data,
                    })
        except Exception:
            pass
print(json.dumps(matches))
"""
    return python_json(python, code, [str(repo)], timeout=120)


def verify_distributions(python: Path, packages: list[str]) -> dict[str, Any]:
    code = r"""
import importlib.metadata as md
import json
import sys

out = []
for name in sys.argv[1:]:
    item = {"name": name, "ok": False}
    try:
        dist = md.distribution(name)
        item.update({
            "ok": True,
            "metadata_name": dist.metadata.get("Name"),
            "version": dist.version,
            "summary": dist.metadata.get("Summary"),
        })
        top_level = dist.read_text("top_level.txt")
        if top_level:
            item["top_level"] = [line.strip() for line in top_level.splitlines() if line.strip()]
    except Exception as exc:
        item["error"] = f"{type(exc).__name__}: {exc}"
    out.append(item)
print(json.dumps(out))
"""
    return python_json(python, code, packages, timeout=120)


def verify_imports(python: Path, imports: list[str]) -> dict[str, Any]:
    code = r"""
import importlib
import json
import sys
import traceback

out = []
for name in sys.argv[1:]:
    item = {"module": name, "ok": False}
    try:
        mod = importlib.import_module(name)
        item.update({
            "ok": True,
            "file": getattr(mod, "__file__", None),
            "version": getattr(mod, "__version__", None),
        })
    except Exception as exc:
        item["error"] = f"{type(exc).__name__}: {exc}"
        item["traceback"] = traceback.format_exc(limit=8)
    out.append(item)
print(json.dumps(out))
"""
    return python_json(python, code, imports, timeout=180)


def list_console_scripts(python: Path, packages: list[str]) -> dict[str, Any]:
    code = r"""
import importlib.metadata as md
import json
import sys

names = {name.lower().replace("_", "-") for name in sys.argv[1:]}
out = []
for dist in md.distributions():
    dist_name = (dist.metadata.get("Name") or "").lower().replace("_", "-")
    if names and dist_name not in names:
        continue
    for ep in dist.entry_points:
        if ep.group == "console_scripts":
            out.append({
                "distribution": dist.metadata.get("Name"),
                "name": ep.name,
                "value": ep.value,
            })
print(json.dumps(out))
"""
    return python_json(python, code, packages, timeout=120)


def torch_backend_check(python: Path, hardware: str, require_cuda: bool) -> dict[str, Any]:
    code = r"""
import json

out = {"torch_imported": False}
try:
    import torch
    out["torch_imported"] = True
    out["torch_version"] = getattr(torch, "__version__", None)
    out["torch_cuda_version"] = getattr(torch.version, "cuda", None)
    out["cuda_available"] = bool(torch.cuda.is_available())
    out["cuda_device_count"] = int(torch.cuda.device_count()) if hasattr(torch, "cuda") else 0
    if out["cuda_available"]:
        out["cuda_device_name_0"] = torch.cuda.get_device_name(0)
        out["cuda_capability_0"] = list(torch.cuda.get_device_capability(0))
        torch.empty((1,), device="cuda")
        out["cuda_tensor_allocated"] = True
    out["mps_available"] = bool(
        getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()
    )
except Exception as exc:
    out["error"] = f"{type(exc).__name__}: {exc}"
print(json.dumps(out))
"""
    result = python_json(python, code, timeout=180)
    data = result.get("json") or {}
    result["required"] = {"hardware": hardware, "require_torch_cuda": require_cuda}
    return result


def run_smoke_code(python: Path, snippets: list[str], timeout: int) -> list[dict[str, Any]]:
    checks = []
    for idx, snippet in enumerate(snippets, start=1):
        result = run([str(python), "-c", snippet], timeout=timeout)
        result["smoke_index"] = idx
        result["code"] = snippet
        checks.append(result)
    return checks


def fail(report: dict[str, Any], phase: str, message: str, evidence: Any | None = None) -> None:
    report.setdefault("failures", []).append(
        {
            "phase": phase,
            "message": message,
            "evidence": evidence,
        }
    )


def warn(report: dict[str, Any], message: str, evidence: Any | None = None) -> None:
    report.setdefault("warnings", []).append({"message": message, "evidence": evidence})


def enrich_env_create_failure(env_manager: str, result: dict[str, Any]) -> dict[str, Any]:
    evidence = dict(result)
    if env_manager == "venv":
        stderr = str(result.get("stderr") or "")
        stdout = str(result.get("stdout") or "")
        combined = f"{stdout}\n{stderr}".lower()
        evidence["recommended_action"] = (
            "Rerun through bootstrap_python.mjs with --require-venv so DisCo can use a private standalone "
            "host Python, use conda, or install the OS venv package for the host Python."
        )
        if "ensurepip" in combined or "venv" in combined:
            evidence["likely_cause"] = (
                "The host Python exists but does not provide the venv/ensurepip modules needed to create a venv."
            )
    return evidence


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create/reuse an isolated Python environment, install a local repo package, and verify it.",
    )
    parser.add_argument("--repo", required=True, help="Local repository path.")
    parser.add_argument(
        "--conda-prefix",
        required=True,
        help="Target environment prefix/path. Kept for compatibility; may be a conda prefix or venv path.",
    )
    parser.add_argument(
        "--env-manager",
        choices=["auto", "conda", "venv"],
        default="auto",
        help="Environment manager to use. auto prefers conda and falls back to venv.",
    )
    parser.add_argument("--python-version", default="3.11", help="Python version for new prefix.")
    parser.add_argument("--conda", default="conda", help="Conda executable name/path.")
    parser.add_argument("--package", action="append", default=[], help="Distribution name to verify.")
    parser.add_argument("--import", dest="imports", action="append", default=[], help="Import module to verify.")
    parser.add_argument("--extra", action="append", default=[], help="Package extra to install from the repo.")
    parser.add_argument("--requirements", action="append", default=[], help="Requirements file to install.")
    parser.add_argument(
        "--include-scope",
        action="append",
        default=[],
        help="Confirmed directory/workflow included in create-repo-skill extraction scope.",
    )
    parser.add_argument(
        "--exclude-scope",
        action="append",
        default=[],
        help="Directory/workflow intentionally excluded from create-repo-skill extraction scope.",
    )
    parser.add_argument(
        "--install-scope-note",
        action="append",
        default=[],
        help="Reasoning note for dependency choices made from the confirmed extraction scope.",
    )
    parser.add_argument(
        "--pre-pip-install",
        action="append",
        default=[],
        help="Arguments after 'python -m pip install' to run before installing the repo.",
    )
    parser.add_argument(
        "--post-pip-install",
        action="append",
        default=[],
        help="Arguments after 'python -m pip install' to run after installing the repo.",
    )
    parser.add_argument(
        "--install-mode",
        choices=["editable", "normal"],
        default="editable",
        help="Install the local repo with pip install -e or pip install.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Do not install; only verify an existing prefix.",
    )
    parser.add_argument(
        "--hardware",
        default="auto",
        choices=["auto", "none", "cpu", "cuda", "rocm", "mps", "tpu", "ascend", "cambricon", "metax"],
        help="Requested backend expectation.",
    )
    parser.add_argument(
        "--require-torch-cuda",
        action="store_true",
        help="Fail verification unless torch imports and torch.cuda works.",
    )
    parser.add_argument(
        "--check-console-scripts",
        action="store_true",
        help="Run discovered console scripts with --help. Use only for safe CLIs.",
    )
    parser.add_argument("--smoke-code", action="append", default=[], help="Python code snippet to run after imports.")
    parser.add_argument("--report", default="repo_env_report.json", help="JSON report output path.")
    parser.add_argument("--timeout", type=int, default=1200, help="Timeout seconds for install commands.")
    parser.add_argument("--smoke-timeout", type=int, default=180, help="Timeout seconds per smoke snippet.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo = Path(args.repo).expanduser().resolve()
    prefix = Path(args.conda_prefix).expanduser().resolve()
    report_path = Path(args.report).expanduser().resolve()

    report: dict[str, Any] = {
        "status": "failed",
        "started_at": utc_now(),
        "inputs": {
            "repo": str(repo),
            "conda_prefix": str(prefix),
            "environment_prefix": str(prefix),
            "requested_env_manager": args.env_manager,
            "python_version": args.python_version,
            "packages": args.package,
            "imports": args.imports,
            "extras": args.extra,
            "requirements": args.requirements,
            "include_scope": args.include_scope,
            "exclude_scope": args.exclude_scope,
            "install_scope_notes": args.install_scope_note,
            "install_mode": args.install_mode,
            "verify_only": args.verify_only,
            "hardware": args.hardware,
            "require_torch_cuda": args.require_torch_cuda,
        },
        "host": {},
        "repo_inspection": {},
        "commands": [],
        "verification": {},
        "warnings": [],
        "failures": [],
        "handoff": {},
    }

    try:
        if not repo.exists() or not repo.is_dir():
            fail(report, "input", f"Repository path does not exist or is not a directory: {repo}")
            return finish(report, report_path)

        conda_path = find_conda(args.conda)
        env_manager = args.env_manager
        if env_manager == "auto":
            env_manager = "conda" if conda_path else "venv"
        if env_manager == "conda" and not conda_path:
            fail(
                report,
                "conda",
                f"Conda executable not found: {args.conda}. Use --env-manager venv or run through bootstrap_python.mjs on machines without conda.",
            )
            return finish(report, report_path)
        report["inputs"]["environment_manager"] = env_manager

        report["host"] = host_probe(conda_path)
        root_prefix = report["host"].get("conda_root_prefix")
        if env_manager == "conda" and root_prefix and Path(str(root_prefix)).expanduser().resolve() == prefix:
            fail(report, "conda-prefix", "Target conda prefix resolves to conda base/root prefix.")
            return finish(report, report_path)

        report["repo_inspection"] = inspect_repo(repo, args.package, args.imports)
        package_names = list(report["repo_inspection"].get("package_names") or [])
        import_modules = list(report["repo_inspection"].get("import_roots") or [])

        if not package_names:
            warn(
                report,
                "No distribution name discovered before install. The script will try direct_url metadata after install; pass --package if this is ambiguous.",
            )
        if not import_modules:
            warn(report, "No import module discovered. Pass --import to make import verification meaningful.")

        if env_manager == "venv":
            host_family = python_major_minor(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
            requested_family = python_major_minor(str(args.python_version))
            if requested_family and requested_family != host_family:
                warn(
                    report,
                    "venv fallback uses the host Python version; requested Python version does not match host Python.",
                    {
                        "requested_python_version": args.python_version,
                        "host_python_version": platform.python_version(),
                        "recommended_action": (
                            "Run through bootstrap_python.mjs with --python-family and --require-family "
                            "matching the requested version, or use conda."
                        ),
                    },
                )

        if not prefix.exists() and not args.verify_only:
            if env_manager == "conda":
                create_cmd = [
                    str(conda_path),
                    "create",
                    "-y",
                    "-p",
                    str(prefix),
                    f"python={args.python_version}",
                    "pip",
                ]
            else:
                create_cmd = [sys.executable, "-m", "venv", "--upgrade-deps", str(prefix)]
            result = run(create_cmd, timeout=args.timeout)
            report["commands"].append(result)
            if not ok(result):
                fail(
                    report,
                    f"{env_manager}-create",
                    f"Failed to create {env_manager} environment prefix.",
                    enrich_env_create_failure(env_manager, result),
                )
                return finish(report, report_path)
        elif not prefix.exists() and args.verify_only:
            fail(report, "verify-only", f"Environment prefix does not exist: {prefix}")
            return finish(report, report_path)
        else:
            warn(report, f"Environment prefix already exists; reusing it without deleting or recreating.")

        python = find_python(prefix)
        if python is None:
            fail(report, "python", f"No runnable Python executable found inside prefix: {prefix}")
            return finish(report, report_path)

        report["handoff"]["python_executable"] = str(python)
        report["handoff"]["conda_prefix"] = str(prefix)
        report["handoff"]["environment_prefix"] = str(prefix)
        report["handoff"]["environment_manager"] = env_manager
        report["handoff"]["repo_path"] = str(repo)

        py_version_result = run([str(python), "--version"], timeout=30)
        report["commands"].append(py_version_result)
        if not ok(py_version_result):
            fail(report, "python", "Target Python executable did not run.", py_version_result)
            return finish(report, report_path)

        if not args.verify_only:
            upgrade = run(
                [str(python), "-m", "pip", "install", "-U", "pip", "setuptools", "wheel"],
                timeout=args.timeout,
            )
            report["commands"].append(upgrade)
            if not ok(upgrade):
                fail(report, "packaging-tools", "Failed to upgrade pip/setuptools/wheel.", upgrade)
                return finish(report, report_path)

            for spec in args.pre_pip_install:
                result = run(pip_install_command(python, spec), timeout=args.timeout)
                report["commands"].append(result)
                if not ok(result):
                    fail(report, "pre-dependency-install", f"Pre-install command failed: {spec}", result)
                    return finish(report, report_path)

            for req in args.requirements:
                req_path = Path(req).expanduser()
                if not req_path.is_absolute():
                    req_path = (repo / req_path).resolve()
                result = run([str(python), "-m", "pip", "install", "-r", str(req_path)], timeout=args.timeout)
                report["commands"].append(result)
                if not ok(result):
                    fail(report, "requirements-install", f"Requirements install failed: {req_path}", result)
                    return finish(report, report_path)

            install_target = make_install_target(repo, args.extra)
            install_cmd = [str(python), "-m", "pip", "install"]
            if args.install_mode == "editable":
                install_cmd.append("-e")
            install_cmd.append(install_target)
            result = run(install_cmd, timeout=args.timeout, cwd=repo)
            report["commands"].append(result)
            if not ok(result):
                fail(report, "repo-install", "Local repository package install failed.", result)
                return finish(report, report_path)

            for spec in args.post_pip_install:
                result = run(pip_install_command(python, spec), timeout=args.timeout)
                report["commands"].append(result)
                if not ok(result):
                    fail(report, "post-dependency-install", f"Post-install command failed: {spec}", result)
                    return finish(report, report_path)

        if not package_names:
            direct = discover_repo_distributions(python, repo)
            report["verification"]["direct_url_distributions"] = direct
            if ok(direct) and isinstance(direct.get("json"), list):
                for item in direct["json"]:
                    name = item.get("name")
                    if isinstance(name, str) and name not in package_names:
                        package_names.append(name)

        if not import_modules and package_names:
            import_modules = [normalize_dist_to_import(name) for name in package_names]
            warn(report, "Import modules were inferred from distribution names.", import_modules)

        pip_check = run([str(python), "-m", "pip", "check"], timeout=180)
        report["commands"].append(pip_check)
        report["verification"]["pip_check"] = pip_check
        if not ok(pip_check):
            fail(report, "pip-check", "pip check reported dependency conflicts.", pip_check)

        if package_names:
            dist_result = verify_distributions(python, package_names)
            report["verification"]["distributions"] = dist_result
            dist_data = dist_result.get("json") if ok(dist_result) else None
            if not isinstance(dist_data, list) or any(not item.get("ok") for item in dist_data):
                fail(report, "distribution-verification", "Expected distribution metadata is missing.", dist_result)
            else:
                for item in dist_data:
                    for top in item.get("top_level", []) or []:
                        if top and top not in import_modules:
                            import_modules.append(top)
        else:
            fail(
                report,
                "distribution-verification",
                "No package distribution name could be verified. Pass --package or fix package metadata.",
            )

        if import_modules:
            import_result = verify_imports(python, import_modules)
            report["verification"]["imports"] = import_result
            import_data = import_result.get("json") if ok(import_result) else None
            if not isinstance(import_data, list) or any(not item.get("ok") for item in import_data):
                fail(report, "import-verification", "One or more expected imports failed.", import_result)
        else:
            fail(report, "import-verification", "No import module was available to verify. Pass --import.")

        console_scripts = list_console_scripts(python, package_names)
        report["verification"]["console_scripts"] = console_scripts
        if args.check_console_scripts and ok(console_scripts) and isinstance(console_scripts.get("json"), list):
            script_results = []
            bin_dir = python.parent
            for item in console_scripts["json"]:
                script = item.get("name")
                if not script:
                    continue
                exe = bin_dir / script
                if not exe.exists():
                    exe = bin_dir / f"{script}.exe"
                if exe.exists():
                    script_results.append(run([str(exe), "--help"], timeout=60))
                else:
                    script_results.append(
                        {
                            "command": f"{script} --help",
                            "returncode": None,
                            "stdout": "",
                            "stderr": "Console script executable not found in prefix bin directory.",
                            "timed_out": False,
                        }
                    )
            report["verification"]["console_script_help"] = script_results
            if any(not ok(item) for item in script_results):
                fail(report, "console-script-verification", "One or more console script help checks failed.", script_results)

        if args.hardware in {"cuda", "mps"} or args.require_torch_cuda:
            torch_result = torch_backend_check(python, args.hardware, args.require_torch_cuda)
            report["verification"]["hardware_backend"] = torch_result
            data = torch_result.get("json") or {}
            if args.require_torch_cuda or args.hardware == "cuda":
                if not ok(torch_result) or not data.get("torch_imported") or not data.get("cuda_available"):
                    fail(report, "backend-verification", "Requested torch CUDA backend is not usable.", torch_result)
            elif args.hardware == "mps":
                if data.get("torch_imported") and not data.get("mps_available"):
                    fail(report, "backend-verification", "Requested torch MPS backend is not usable.", torch_result)

        if args.smoke_code:
            smoke_results = run_smoke_code(python, args.smoke_code, args.smoke_timeout)
            report["verification"]["smoke_code"] = smoke_results
            if any(not ok(item) for item in smoke_results):
                fail(report, "smoke-test", "One or more smoke code snippets failed.", smoke_results)

        freeze = run([str(python), "-m", "pip", "freeze"], timeout=180)
        report["commands"].append(freeze)
        if ok(freeze):
            report["verification"]["pip_freeze"] = freeze["stdout"].splitlines()
        else:
            warn(report, "pip freeze failed; environment may still be usable but reproducibility snapshot is missing.", freeze)

        if not report["failures"]:
            import_data = report.get("verification", {}).get("imports", {}).get("json") or []
            successful_imports = [
                item.get("module") for item in import_data if isinstance(item, dict) and item.get("ok")
            ]
            report["status"] = "ok"
            report["handoff"].update(
                {
                    "package_names": package_names,
                    "successful_imports": successful_imports,
                    "report_path": str(report_path),
                    "ready_for_create_skill_for_a_repo": True,
                }
            )
        else:
            report["handoff"]["ready_for_create_skill_for_a_repo"] = False

        return finish(report, report_path)
    finally:
        # If the function returns before finish due to an unexpected exception, the
        # outer handler below writes the report. Normal paths call finish directly.
        pass


def finish(report: dict[str, Any], report_path: Path) -> int:
    report["finished_at"] = utc_now()
    if report.get("failures"):
        report["status"] = "failed"
        report.setdefault("handoff", {})["ready_for_create_skill_for_a_repo"] = False
    elif report.get("status") != "ok":
        report["status"] = "failed"
        report.setdefault("handoff", {})["ready_for_create_skill_for_a_repo"] = False
    write_report(report_path, report)
    print(f"Wrote report: {report_path}")
    print(f"Status: {report['status']}")
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as exc:
        emergency = {
            "status": "failed",
            "started_at": utc_now(),
            "finished_at": utc_now(),
            "failures": [
                {
                    "phase": "unexpected-error",
                    "message": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(),
                }
            ],
            "handoff": {"ready_for_create_skill_for_a_repo": False},
        }
        report_arg = "repo_env_report.json"
        if "--report" in sys.argv:
            try:
                report_arg = sys.argv[sys.argv.index("--report") + 1]
            except Exception:
                pass
        path = Path(report_arg).expanduser().resolve()
        write_report(path, emergency)
        print(f"Wrote report: {path}")
        print("Status: failed")
        raise SystemExit(1)
