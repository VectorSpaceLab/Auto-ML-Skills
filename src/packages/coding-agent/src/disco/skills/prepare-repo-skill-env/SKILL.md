---
name: prepare-repo-skill-env
description: "Create, install, and prove a usable Python inspection environment containing a local repository package before running create-repo-skill. Use when create-repo-skill needs an inspection environment and the user did not provide one, when the user gives a repo path plus an environment path/prefix, asks to prepare the prerequisite package-inspection environment, install a local repo package into conda or venv, repair a broken repo install, bootstrap Python on an npm-installed machine, or verify CUDA/driver/torch/backend compatibility before skill generation."
---

# Prepare Repo Skill Env

## Purpose

Use this skill before `create-repo-skill` when the user provides or the
calling skill can infer:

- A local repository path.
- A desired or inferred environment prefix/path for the package-inspection Python.

When this skill is invoked by `create-repo-skill` because the user gave a
repo path but did not provide an installed Python environment, it is acceptable
to use the caller's private default environment prefix instead of asking the user for
a prefix. In that path, expect the caller to have already completed repository
structure analysis and to pass the confirmed extraction scope. Use that scope to
choose the smallest install plan that covers the selected directories and user
requirements. The default prefix should be under
`$DISCO_CODING_AGENT_DIR/envs/` when that variable is set, otherwise under
`~/.disco/agent/envs/`.

The job is to create or repair an isolated Python inspection environment,
install the package from the repository into that environment, and prove that
the environment is usable for later live package inspection. Prefer conda when
it is already available because it handles package Python versions and compiled
dependencies well; when conda is unavailable, use a venv fallback rather than
blocking. If no usable host Python exists to run DisCo's helper, use the
bundled Node bootstrap helper to download a private host Python under the
DisCo agent directory, then continue. Do not hand off an environment just
because `pip install` returned successfully. The environment is complete only
after import, dependency, metadata, and relevant hardware/backend checks pass.

This skill produces private setup evidence for the current user and downstream
agent. The environment prefix, local checkout path, Python executable path,
bootstrap Python path, and install report may be handed to `create-repo-skill`,
but they must not be copied into any public repo skill generated later.

## Required Outputs

By the end, deliver either a usable-environment handoff or a detailed failure report.

For success, include:

- Repository path.
- Environment manager and prefix/path.
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
- A clear statement that the environment is not ready for `create-repo-skill`.

## Reference Map

Read the relevant reference before acting:

- [references/install-planning.md](references/install-planning.md): repo/package discovery, environment prefix handling, install order, editable installs, requirements, extras, and compiled-package policy.
- [references/hardware-and-backends.md](references/hardware-and-backends.md): hardware probing, NVIDIA CUDA/driver/torch wheel decisions, CPU/MPS/ROCm/other accelerator handling, and when to report hardware impossibility.
- [references/verification-and-failure-report.md](references/verification-and-failure-report.md): mandatory verification gates, report interpretation, smoke tests, handoff template, and failure-report template.

Use [scripts/bootstrap_python.mjs](scripts/bootstrap_python.mjs) before running
the Python helper whenever `python3`/`python` is absent, too old, or the wrong
major/minor family for the requested target. It first uses `DISCO_PYTHON` or
PATH, otherwise downloads a private host Python under
`$DISCO_CODING_AGENT_DIR/runtimes/python-host/` or
`~/.disco/agent/runtimes/python-host/`, then runs the requested command. If
the install plan requires a specific Python family such as 3.10 or 3.12, pass
both `--python-family <major.minor>` and `--require-family <major.minor>` to
the bootstrap helper so it does not silently reuse a different PATH Python. If
the target inspection environment may use venv fallback, also pass
`--require-venv` so Linux hosts with Python but missing `venv`/`ensurepip`
packages do not get selected accidentally. In restricted networks, use
`--archive /path/to/python-build-standalone.tar.gz` for a local archive or
`--asset-url <mirror-url>` with optional `--asset-digest sha256:<hex>` for an
approved mirror; keep `--download-timeout` finite so failed downloads do not
stall the workflow indefinitely.

Use [scripts/setup_repo_conda_env.py](scripts/setup_repo_conda_env.py) for the
common path after a host Python is available. It creates or reuses an isolated
inspection environment, installs the local repo package, runs verification
gates, and writes a JSON report. With `--env-manager auto`, it prefers conda
when available and falls back to venv when conda is missing.

Do not let package installation crawl indefinitely. If conda or pip is making
little progress, timing out, repeatedly retrying downloads, or spending several
minutes on a small metadata/download step, pause the current attempt and use the
network acceleration guidance in
[references/install-planning.md](references/install-planning.md). Prefer
proactively trying a faster route over waiting for a slow install to finish.

## Workflow

### 1. Gather Inputs

Confirm these before installation:

- `repo_path`: the local repository checkout.
- `environment_prefix`: the environment path/prefix the user wants to use.
- Confirmed extraction scope from `create-repo-skill` when available:
  included directories, excluded directories, selected workflows, and user
  requirements that affect install choices.
- Python version preference, if any. If absent, choose from repo metadata; otherwise default to Python 3.11 unless the repo requires another supported version.
- Installed distribution name, if the user knows it.
- Import module names, if they differ from the distribution name.
- Required extras, requirements files, or documented install variants.
- Hardware expectation: `auto`, `cpu`, `cuda`, `rocm`, `mps`, or another documented backend.
- Environment manager preference: `auto`, `conda`, or `venv`. Use `auto` unless
  the user explicitly requested conda or venv. `auto` prefers conda and falls
  back to venv.
- Whether an existing environment at the prefix may be reused. Do not delete/recreate an existing prefix unless the user explicitly requested that.
- Whether a user-provided existing environment may be modified if verification
  requires reinstalling, upgrading, or repairing packages. If the user has not
  allowed potentially breaking changes, ask before mutating it or fall back to a
  new private prefix when the caller permits that fallback.

If `repo_path` is missing, ask for it. If `environment_prefix` is missing
during a direct invocation, ask for it or propose a private default prefix
before proceeding. If `environment_prefix` is missing because
`create-repo-skill` invoked this skill as an automatic prerequisite, use the
caller-provided private default prefix and continue. Do not invent paths
outside these explicit default-prefix rules.

### 2. Inspect Repo Packaging Before Installing

Read [references/install-planning.md](references/install-planning.md), then inspect:

- `pyproject.toml`, `setup.cfg`, `setup.py`, `requirements*.txt`, lockfiles, and CI install commands.
- Source roots such as `src/<package>/`, top-level packages with `__init__.py`, and console entry points.
- README/docs install instructions for extras, backend variants, torch/CUDA pins, optional compiled packages, and known setup failures.

Decide:

- Distribution package name(s) to verify with `importlib.metadata` / `pip show`.
- Import module(s) to verify with `import`.
- Whether to use editable install (`pip install -e <repo>`) or normal install (`pip install <repo>`). Prefer editable for local package inspection unless the repo docs warn against it.
- Which extras, requirements files, backend packages, and optional dependencies
  are actually needed for the confirmed extraction scope. Install only the
  smallest set that covers included directories, selected workflows, and
  explicit user requirements. Do not install packages used only by excluded
  directories, unselected workflows, dev-only tasks, or broad `[all]` extras
  unless the user explicitly asked for that coverage.
- Whether torch, JAX, TensorFlow, CUDA toolkit, compilers, or other backend dependencies must be installed before the repo.

### 3. Probe Hardware and Choose Backend Install Strategy

Read [references/hardware-and-backends.md](references/hardware-and-backends.md), then probe the host before choosing GPU/accelerator packages:

- OS, architecture (`x86_64`, `aarch64`, `arm64`), Python availability, and
  whether `scripts/bootstrap_python.mjs` is needed.
- Conda availability and whether venv fallback will be used.
- NVIDIA: `nvidia-smi`, GPU name/count/VRAM, compute capability, driver version, driver-reported max CUDA, and `nvcc` only if source compilation is needed.
- Other backends when present: ROCm, Apple MPS, TPU, Ascend, Cambricon, Hygon DCU, MetaX, or CPU-only.

Use these facts to choose install commands. Examples:

- CUDA wheel packages must match the driver-supported CUDA level and GPU architecture.
- New NVIDIA architectures such as Blackwell need recent CUDA/PyTorch wheels; old wheels can install but fail at runtime.
- `aarch64` often lacks wheels for CUDA extension packages; expect source builds or use fallback backends.
- If the requested backend cannot be supported on the current host, stop, write the failure report, and do not hand off a fake-success environment.

### 4. Create or Reuse the Inspection Environment

Use a prefix path, not conda `base`, for the inspection environment. When
Python is missing on an npm-installed machine, do not stop after reporting
`python: command not found`; run the Node bootstrap helper and continue unless
the download fails or the user forbade downloads.

Before long installs, establish the fastest safe network route available:

- If downloads or metadata resolution are slow, ask the user whether they have a
  VPN/proxy command that should be enabled for package installation.
- If the user provides a VPN/proxy command, run it only after confirming it is
  intended for this task, then retry the install commands.
- If no VPN/proxy is available or it does not help, try a suitable temporary
  pip or conda mirror/index for the current package ecosystem.
- Record any VPN/proxy, mirror, timeout, and retry choices in the private setup
  report or handoff notes. Do not copy local proxy commands or private network
  details into generated public repo skills.

For the common path, run through the bootstrap helper. It is safe to use even
when Python is already installed:

```bash
node scripts/bootstrap_python.mjs --python-family 3.11 --require-family 3.11 --require-venv -- \
  {python} scripts/setup_repo_conda_env.py \
  --repo /path/to/repo \
  --conda-prefix /path/to/inspection/env \
  --env-manager auto \
  --python-version 3.11 \
  --hardware auto \
  --report repo_env_report.json
```

Add specific names when automatic discovery is ambiguous:

```bash
node scripts/bootstrap_python.mjs --python-family 3.10 --require-family 3.10 --require-venv -- \
  {python} scripts/setup_repo_conda_env.py \
  --repo /path/to/repo \
  --conda-prefix /path/to/inspection/env \
  --env-manager auto \
  --python-version 3.10 \
  --include-scope src/package \
  --include-scope docs/inference.md \
  --exclude-scope training/ \
  --install-scope-note "Install only inference dependencies because training is outside the confirmed extraction scope." \
  --package package-dist-name \
  --import package_import_name \
  --extra cuda \
  --hardware cuda \
  --require-torch-cuda \
  --report repo_env_report.json
```

If repo docs require preinstalling a backend package, pass it explicitly:

```bash
node scripts/bootstrap_python.mjs --python-family 3.11 --require-family 3.11 --require-venv -- \
  {python} scripts/setup_repo_conda_env.py \
  --repo /path/to/repo \
  --conda-prefix /path/to/inspection/env \
  --env-manager auto \
  --pre-pip-install "torch --index-url https://download.pytorch.org/whl/cu128" \
  --hardware cuda \
  --report repo_env_report.json
```

The script is a helper, not a replacement for judgment. If repo docs require unusual system packages, services, credentials, model downloads, or a custom build command, execute those steps deliberately and record them in the report or final handoff.

If the caller provided a confirmed extraction scope, translate it into helper
arguments deliberately. Record the scope with `--include-scope`,
`--exclude-scope`, and `--install-scope-note`. Use `--extra`,
`--requirements`, `--pre-pip-install`, and `--post-pip-install` only for
dependencies needed by the selected directories and workflows. Keep
excluded-directory dependencies out of the command unless they are also needed
by an included workflow.

If the helper appears stuck on network I/O, interrupt it rather than waiting
blindly. Then rerun it with the chosen faster route, such as a configured
VPN/proxy environment, a temporary `PIP_INDEX_URL`, `PIP_EXTRA_INDEX_URL`, or
conda channel override when that is appropriate for the packages being
installed. If the blocker is GitHub release access for the bootstrap Python
itself, rerun `scripts/bootstrap_python.mjs` with `--archive` pointing at a
local python-build-standalone archive, or with `--asset-url` pointing at an
approved mirror and `--asset-digest sha256:<hex>` when available.

### 5. Verify Before Handoff

Read [references/verification-and-failure-report.md](references/verification-and-failure-report.md). A ready environment must pass all applicable gates:

- The conda prefix exists and has a runnable Python executable.
- If venv fallback was used, the venv prefix exists and has a runnable Python executable.
- The repo package is installed in that Python environment.
- `python -m pip check` passes.
- Expected distribution metadata is present.
- Expected import modules import successfully.
- Important console entry points or APIs pass safe `--help`, signature, or smoke checks when relevant.
- Requested hardware/backend checks pass. For CUDA, this includes driver/wheel compatibility and a Python backend check such as torch CUDA when the repo depends on torch.
- Any custom smoke command needed to prove repo-specific usability passes.

If any required gate fails, fix and rerun verification. Do not pass the environment to `create-repo-skill` until verification succeeds.

### 6. Handoff to `create-repo-skill`

When verification passes, provide a concise handoff in this form:

```text
Repository path: <repo_path>
Temporary inspection Python: <conda_prefix>/bin/python
Environment manager: <conda|venv>
Environment prefix: <environment_prefix>
Installed package name: <distribution-name>
Verified import(s): <module-a>, <module-b>
Verification report: <repo_env_report.json>
Hardware/backend verdict: <cpu/cuda/rocm/mps/... ok, warning, or not applicable>
Notes for create-repo-skill: <extras, optional deps, skipped unsafe tests, known limitations>
```

Only after this handoff is it appropriate to run `create-repo-skill`.

## Non-Negotiables

- Never hand off an environment that has not been verified.
- Never treat a successful `conda create`, `python -m venv`, or `pip install` as sufficient proof.
- Never wait indefinitely on a very slow package install. If progress stalls,
  interrupt, diagnose network/index speed, ask about VPN/proxy commands when
  useful, try faster mirrors or indexes when safe, and rerun verification.
- Never install into or mutate conda `base` for this task.
- Never delete/recreate an existing environment prefix unless the user explicitly authorized that exact action.
- Never block solely because the npm-installed machine has no Python on PATH.
  Use `scripts/bootstrap_python.mjs` to install a private host Python and then
  continue with `scripts/setup_repo_conda_env.py`.
- Never mutate a user-provided existing environment with reinstall, upgrade, or
  repair commands when those changes may break it unless the user authorizes the
  modification. If permission is denied, create or request a separate private
  inspection environment instead.
- Never install broad optional dependency sets when the confirmed extraction
  scope only needs a smaller set.
- Never hide hardware incompatibility. If the current machine cannot support the requested CUDA/backend/package combination, report the concrete facts and stop.
- Keep local environment paths and machine-specific setup details out of any public skill generated later.
