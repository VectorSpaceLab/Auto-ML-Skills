---
name: prepare-env-for-create-skill-for-a-repo
description: "Create, install, and prove a usable conda Python environment containing a local repository package before running create-skill-for-a-repo. Use when the user gives a repo path plus a conda environment path/prefix, asks to prepare the prerequisite package-inspection environment for create-skill-for-a-repo, install a local repo package into conda, repair a broken repo install, or verify CUDA/driver/torch/backend compatibility before skill generation. Triggers: prerequisite skill, create-skill-for-a-repo environment, repo package conda environment, install local repository, verify environment usability, CUDA driver torch install failure."
---

# Prepare Env for Create Skill for a Repo

## Purpose

Use this skill before `create-skill-for-a-repo` when the user provides:

- A local repository path.
- A desired conda environment prefix/path for the package-inspection Python.

The job is to create or repair an isolated conda environment, install the package from the repository into that environment, and prove that the environment is usable for later live package inspection. Do not hand off an environment just because `pip install` returned successfully. The environment is complete only after import, dependency, metadata, and relevant hardware/backend checks pass.

This skill produces private setup evidence for the current user and downstream agent. The conda prefix, local checkout path, Python executable path, and install report may be handed to `create-skill-for-a-repo`, but they must not be copied into any public repo skill generated later.

## Required Outputs

By the end, deliver either a usable-environment handoff or a detailed failure report.

For success, include:

- Repository path.
- Conda prefix/path.
- Python executable path inside that prefix.
- Installed distribution/package name(s).
- Import module(s) that were verified successfully.
- Hardware/backend verdict when relevant.
- Path to `repo_env_report.json`.
- The exact verification commands or script result that prove usability.

For failure, include:

- The installation phase that failed.
- Hardware, driver, Python, platform, and package-manager facts that matter.
- The exact command(s) that failed, with key stderr lines summarized.
- Whether the blocker is fixable by changing Python/package versions, using CPU fallback, installing a toolkit/compiler, changing torch/CUDA wheels, or whether the current hardware/driver stack cannot support the requested package.
- A clear statement that the environment is not ready for `create-skill-for-a-repo`.

## Reference Map

Read the relevant reference before acting:

- [references/install-planning.md](references/install-planning.md): repo/package discovery, conda prefix handling, install order, editable installs, requirements, extras, and compiled-package policy.
- [references/hardware-and-backends.md](references/hardware-and-backends.md): hardware probing, NVIDIA CUDA/driver/torch wheel decisions, CPU/MPS/ROCm/other accelerator handling, and when to report hardware impossibility.
- [references/verification-and-failure-report.md](references/verification-and-failure-report.md): mandatory verification gates, report interpretation, smoke tests, handoff template, and failure-report template.

Use [scripts/setup_repo_conda_env.py](scripts/setup_repo_conda_env.py) for the common path. It creates or reuses a conda prefix, installs the local repo package, runs verification gates, and writes a JSON report.

## Workflow

### 1. Gather Inputs

Confirm these before installation:

- `repo_path`: the local repository checkout.
- `conda_prefix`: the environment path/prefix the user wants to use.
- Python version preference, if any. If absent, choose from repo metadata; otherwise default to Python 3.11 unless the repo requires another supported version.
- Installed distribution name, if the user knows it.
- Import module names, if they differ from the distribution name.
- Required extras, requirements files, or documented install variants.
- Hardware expectation: `auto`, `cpu`, `cuda`, `rocm`, `mps`, or another documented backend.
- Whether an existing environment at the prefix may be reused. Do not delete/recreate an existing prefix unless the user explicitly requested that.

If `repo_path` or `conda_prefix` is missing, ask for it. Do not invent paths.

### 2. Inspect Repo Packaging Before Installing

Read [references/install-planning.md](references/install-planning.md), then inspect:

- `pyproject.toml`, `setup.cfg`, `setup.py`, `requirements*.txt`, lockfiles, and CI install commands.
- Source roots such as `src/<package>/`, top-level packages with `__init__.py`, and console entry points.
- README/docs install instructions for extras, backend variants, torch/CUDA pins, optional compiled packages, and known setup failures.

Decide:

- Distribution package name(s) to verify with `importlib.metadata` / `pip show`.
- Import module(s) to verify with `import`.
- Whether to use editable install (`pip install -e <repo>`) or normal install (`pip install <repo>`). Prefer editable for local package inspection unless the repo docs warn against it.
- Whether torch, JAX, TensorFlow, CUDA toolkit, compilers, or other backend dependencies must be installed before the repo.

### 3. Probe Hardware and Choose Backend Install Strategy

Read [references/hardware-and-backends.md](references/hardware-and-backends.md), then probe the host before choosing GPU/accelerator packages:

- OS, architecture (`x86_64`, `aarch64`, `arm64`), Python availability.
- Conda availability.
- NVIDIA: `nvidia-smi`, GPU name/count/VRAM, compute capability, driver version, driver-reported max CUDA, and `nvcc` only if source compilation is needed.
- Other backends when present: ROCm, Apple MPS, TPU, Ascend, Cambricon, Hygon DCU, MetaX, or CPU-only.

Use these facts to choose install commands. Examples:

- CUDA wheel packages must match the driver-supported CUDA level and GPU architecture.
- New NVIDIA architectures such as Blackwell need recent CUDA/PyTorch wheels; old wheels can install but fail at runtime.
- `aarch64` often lacks wheels for CUDA extension packages; expect source builds or use fallback backends.
- If the requested backend cannot be supported on the current host, stop, write the failure report, and do not hand off a fake-success environment.

### 4. Create or Reuse the Conda Prefix

Use a prefix path, not `base`, for the inspection environment.

For the common path, run:

```bash
python3 scripts/setup_repo_conda_env.py \
  --repo /path/to/repo \
  --conda-prefix /path/to/conda/env \
  --python-version 3.11 \
  --hardware auto \
  --report repo_env_report.json
```

Add specific names when automatic discovery is ambiguous:

```bash
python3 scripts/setup_repo_conda_env.py \
  --repo /path/to/repo \
  --conda-prefix /path/to/conda/env \
  --python-version 3.10 \
  --package package-dist-name \
  --import package_import_name \
  --extra cuda \
  --hardware cuda \
  --require-torch-cuda \
  --report repo_env_report.json
```

If repo docs require preinstalling a backend package, pass it explicitly:

```bash
python3 scripts/setup_repo_conda_env.py \
  --repo /path/to/repo \
  --conda-prefix /path/to/conda/env \
  --pre-pip-install "torch --index-url https://download.pytorch.org/whl/cu128" \
  --hardware cuda \
  --report repo_env_report.json
```

The script is a helper, not a replacement for judgment. If repo docs require unusual system packages, services, credentials, model downloads, or a custom build command, execute those steps deliberately and record them in the report or final handoff.

### 5. Verify Before Handoff

Read [references/verification-and-failure-report.md](references/verification-and-failure-report.md). A ready environment must pass all applicable gates:

- The conda prefix exists and has a runnable Python executable.
- The repo package is installed in that Python environment.
- `python -m pip check` passes.
- Expected distribution metadata is present.
- Expected import modules import successfully.
- Important console entry points or APIs pass safe `--help`, signature, or smoke checks when relevant.
- Requested hardware/backend checks pass. For CUDA, this includes driver/wheel compatibility and a Python backend check such as torch CUDA when the repo depends on torch.
- Any custom smoke command needed to prove repo-specific usability passes.

If any required gate fails, fix and rerun verification. Do not pass the environment to `create-skill-for-a-repo` until verification succeeds.

### 6. Handoff to `create-skill-for-a-repo`

When verification passes, provide a concise handoff in this form:

```text
Repository path: <repo_path>
Temporary inspection Python: <conda_prefix>/bin/python
Conda prefix: <conda_prefix>
Installed package name: <distribution-name>
Verified import(s): <module-a>, <module-b>
Verification report: <repo_env_report.json>
Hardware/backend verdict: <cpu/cuda/rocm/mps/... ok, warning, or not applicable>
Notes for create-skill-for-a-repo: <extras, optional deps, skipped unsafe tests, known limitations>
```

Only after this handoff is it appropriate to run `create-skill-for-a-repo`.

## Non-Negotiables

- Never hand off an environment that has not been verified.
- Never treat a successful `conda create` or `pip install` as sufficient proof.
- Never install into or mutate conda `base` for this task.
- Never delete/recreate an existing conda prefix unless the user explicitly authorized that exact action.
- Never hide hardware incompatibility. If the current machine cannot support the requested CUDA/backend/package combination, report the concrete facts and stop.
- Keep local environment paths and machine-specific setup details out of any public skill generated later.
