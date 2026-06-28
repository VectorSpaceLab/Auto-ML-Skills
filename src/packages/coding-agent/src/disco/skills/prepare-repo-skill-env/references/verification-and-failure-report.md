# Verification and Failure Report

## Purpose

Read this reference after installation commands run. The central rule is simple: an environment is not ready for `create-repo-skill` until verification proves it can be used for live package inspection.

## Mandatory Verification Gates

A successful handoff requires all applicable gates to pass:

1. Environment prefix exists. For conda, it is not `base`.
2. Python executable inside the prefix runs.
3. `python -m pip check` passes.
4. Expected distribution metadata exists via `importlib.metadata` or `pip show`.
5. Expected import modules import successfully.
6. Console scripts or CLIs needed by the repo can at least run safe help commands.
7. Backend checks pass when the user or repo requires a backend such as CUDA, ROCm, MPS, TPU, or a vendor accelerator.
8. Repo-specific smoke checks pass when a simple import is too weak to prove usability.

Gate 4 and 5 are both needed. Metadata without import success can mean a broken install. Import success without the expected distribution metadata can mean the wrong package is being imported from the repo checkout or another environment path.

## Using the Setup Script Report

The helper script writes `repo_env_report.json`. Treat `status: "ok"` as usable only after checking that the report covers the repo's actual requirements.

Important fields:

- `handoff.python_executable`: pass this to `create-repo-skill` as the temporary inspection Python.
- `handoff.environment_manager`: `conda` or `venv`.
- `handoff.environment_prefix`: prefix/path for the verified inspection environment.
- `handoff.package_names`: distribution names that were installed and verified.
- `handoff.successful_imports`: modules that imported successfully.
- `verification.pip_check`: dependency resolver consistency.
- `verification.imports`: per-module import results.
- `verification.distributions`: installed package metadata checks.
- `verification.hardware_backend`: Python-level backend facts when available.
- `failures` and `warnings`: unresolved blockers or caveats.

If `status` is not `ok`, do not hand the environment to the next skill.

## Extra Smoke Checks

Use additional smoke checks when import is not enough:

- A repo exposes a CLI: run `<command> --help` with a short timeout.
- A package has a documented minimal object construction path: run that code without downloads or credentials.
- A torch CUDA package must prove GPU usability: allocate a tiny tensor on CUDA or run the package's backend self-test.
- A service package needs optional dependencies: import the service module and inspect CLI help, but do not start long-running servers unless needed.

With the setup script, pass repeatable Python checks as:

```bash
--smoke-code "import package; print(package.__version__)"
--smoke-code "from package import important_api; print(important_api)"
```

For checks that need files, credentials, downloads, network, training runs, or destructive writes, do not run them silently. Report that they were skipped and explain what would be needed to verify them.

## Handoff Template

Use this exact shape when the environment is ready:

```text
Environment ready for create-repo-skill: yes
Repository path: <repo_path>
Environment manager: <conda|venv>
Environment prefix: <environment_prefix>
Temporary inspection Python: <python_executable>
Installed package name(s): <distribution names>
Verified import(s): <modules>
Verification report: <repo_env_report.json>
Hardware/backend verdict: <backend ok/not required/warnings>
Additional notes: <extras installed, skipped unsafe tests, limitations>
```

## Failure Report Template

Use this shape when the environment is not ready:

```text
Environment ready for create-repo-skill: no
Failed phase: <metadata discovery | conda create | dependency install | repo install | pip check | import verification | backend verification | smoke test>
Repository path: <repo_path>
Environment manager: <conda|venv>
Environment prefix: <environment_prefix>
Requested backend: <cpu/cuda/rocm/mps/auto/...>

Facts:
- OS/arch: <...>
- Python target: <...>
- Conda/venv: <...>
- Hardware: <GPU/backend facts or CPU-only>
- Driver/toolkit: <driver CUDA, nvcc, ROCm, vendor toolkit, or not present>

Blocker:
<specific reason the install cannot be considered usable>

Evidence:
- Command: <failed command>
- Key error: <short stderr excerpt>
- Report: <repo_env_report.json if available>

Next viable actions:
1. <change Python/package/backend/wheel/toolkit/driver/hardware>
2. <fallback route if one exists, such as venv when conda is missing>
3. <what the user must provide if external action is needed>
```

## Quality Bar

The final claim must be evidence-backed:

- "Ready" means the report and commands prove the package can be inspected from the target Python.
- "Installed" is not the same as "ready".
- "CUDA available" is not the same as "repo CUDA backend works"; run a repo-specific smoke check when needed.
- "Cannot install on this hardware" must be supported by exact hardware/platform/version evidence.
- Any warnings that weaken later `create-repo-skill` inspection must be surfaced in the handoff.
