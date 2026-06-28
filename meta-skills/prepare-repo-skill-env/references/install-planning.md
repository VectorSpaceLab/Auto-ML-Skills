# Install Planning

## Purpose

Read this reference before creating the conda environment or installing the repo package. The goal is to make the install plan match the repository's real package metadata, Python support, dependencies, backend expectations, and the confirmed extraction scope from `create-repo-skill` instead of guessing from the repo directory name or installing broad dependency sets.

When this skill is called from `create-repo-skill`, repository structure
analysis should already have identified the directories and workflows that will
be used for skill extraction. Treat that include/exclude map as part of the
install input. The environment should support live inspection of the selected
repo areas, not every optional capability in the repository.

## Repo Evidence to Inspect

Start with package metadata:

- `pyproject.toml`: `project.name`, `requires-python`, dependencies, optional dependencies, console scripts, build backend.
- `setup.cfg`: metadata name, `python_requires`, `install_requires`, entry points.
- `setup.py`: fallback source for package name and custom build behavior.
- `requirements*.txt`, lockfiles, `environment.yml`, `tox.ini`, `noxfile.py`, and CI workflow install steps.
- README/docs install sections, especially extras such as `[dev]`, `[cuda]`, `[torch]`, `[all]`, `[serve]`, or backend-specific instructions.

Then identify the Python import roots:

- `src/<module>/`
- top-level `<module>/` directories with `__init__.py`
- namespace packages documented by the repo
- top-level modules such as `<module>.py`
- console entry points and `__main__.py`

Do not assume the distribution name and import name are identical. Examples: distribution `scikit-learn` imports as `sklearn`; distribution names often use hyphens while imports use underscores.

## Extraction-Scope Install Planning

When the caller provides confirmed included and excluded directories, map
dependencies to that scope before installing:

- Start from the package metadata needed for the main distribution and import
  roots that correspond to included source directories.
- Add extras only when an included workflow, included directory, or explicit
  user requirement needs that extra. Examples: use `[serve]` only when serving
  APIs are in scope; use `[cuda]` only when GPU behavior is in scope and the
  hardware plan supports it.
- Add requirements files only when they are documented as runtime requirements
  for included workflows. Skip dev, lint, docs, benchmark, and test
  requirements unless those workflows are explicitly in scope or needed for a
  safe smoke check.
- Add backend foundations such as torch, JAX, TensorFlow, CUDA, ROCm, or
  compiler toolchains only when selected repo areas import or exercise them.
- Skip packages used only by excluded directories, notebooks, examples,
  research experiments, integrations, or optional services that are not part of
  the skill extraction request.

Prefer the narrowest install that still lets import checks, signature
inspection, CLI help, and safe smoke tests pass for the selected areas. If two
install variants both satisfy the confirmed scope, choose the lower-risk one
with fewer heavyweight or hardware-specific packages.

Record the scope decision in the private setup report or handoff notes:

```text
Included scope: src/package, docs/inference.md, examples/predict.py
Excluded scope: training/, benchmarks/, docs/serving.md
Install choices: base package + [inference], skipped [train], [serve], requirements-dev.txt
Reason: only inference APIs and CLI are selected for skill extraction
```

## Python Version Selection

Use repo metadata first:

- Honor `requires-python` when present.
- Prefer the version used in CI or documented install examples.
- If unconstrained, use Python 3.11 as the default stable choice for modern ML/Python packages.
- Avoid Python 3.13 unless the repo and all compiled dependencies explicitly support it.
- Use Python 3.10 or 3.11 for older ML repos with `torch`, `tensorflow`, `tokenizers`, `deepspeed`, `flash-attn`, `xformers`, or similar compiled packages.

If the repo's declared Python range conflicts with the available package/backend wheels, report the conflict and choose the safest compatible version only when evidence supports it.

## Conda Prefix Policy

Use an isolated prefix:

```bash
conda create -y -p /path/to/prefix python=3.11 pip
```

Rules:

- Do not use conda `base`.
- Do not install the repo package into the agent's current Python unless the user explicitly asks for that.
- If the prefix already exists, inspect it before reuse: Python version, `pip check`, existing conflicting packages, and whether the target repo package is already installed.
- Do not delete an existing prefix unless the user explicitly authorized recreation. If cleanup is needed but not authorized, report what blocks reuse and ask or choose a different prefix only if the user allowed that.
- If the prefix is a user-provided existing environment, distinguish
  read-only verification from mutation. Running imports, `pip check`, metadata
  inspection, or CLI `--help` checks is verification. Reinstalling the repo,
  upgrading dependencies, adding extras, removing packages, or repairing
  conflicts is mutation and can break the user's environment. Ask before
  mutating unless the user already authorized it. If they decline, use a new
  private prefix when available.
- Prefer running `/path/to/prefix/bin/python -m pip ...` instead of relying on shell activation. Direct Python paths are less fragile for agents.

## Install Order

Use this order unless repo docs clearly require otherwise:

1. Create or reuse the conda prefix.
2. Upgrade packaging basics inside that prefix:

   ```bash
   /path/to/prefix/bin/python -m pip install -U pip setuptools wheel
   ```

3. Install heavy backend foundations first when required: torch/JAX/TensorFlow, CUDA/ROCm-specific wheels, or conda-provided toolkit/compiler packages.
4. Install normal Python dependencies from package metadata, requirements files, or documented extras.
5. Install the local repo package.
6. Install or build CUDA extension packages last, with build isolation disabled when they must compile against the already-installed torch.
7. Run verification gates.

For local package inspection, prefer editable install:

```bash
/path/to/prefix/bin/python -m pip install -e /path/to/repo
```

Use normal install when editable mode is unsupported or changes import behavior:

```bash
/path/to/prefix/bin/python -m pip install /path/to/repo
```

Install extras only when they are needed for the repo capability being inspected
and the confirmed extraction scope:

```bash
/path/to/prefix/bin/python -m pip install -e "/path/to/repo[cuda,serve]"
```

## Slow Install and Network Acceleration

Do not wait passively while installs crawl. Treat any of these as a signal to
pause and choose a faster route:

- Conda solving, package metadata fetching, or pip downloads show no meaningful
  progress for several minutes.
- Pip repeatedly logs retry, timeout, connection reset, TLS, proxy, or
  read-timeout messages.
- A small package or metadata step is moving at only a few KB/s.
- Large backend wheels are downloading from a distant index and the estimated
  time is unreasonable for the task.

When this happens:

1. Stop or interrupt the current install attempt cleanly. Keep the command,
   elapsed time, and relevant output for the private report.
2. Check whether the slowness is network/index related rather than compilation:
   metadata fetches, wheel downloads, and retry logs point to network; active
   compiler output points to build time.
3. Ask the user whether they have a VPN/proxy command for this machine if
   network access appears slow, blocked, or region-limited. Do not invent,
   install, or start VPN software yourself.
4. If the user provides a VPN/proxy command, confirm it is safe to run for this
   task, run it, and retry the package install.
5. If no VPN/proxy is available or it does not help, try a faster temporary
   mirror or index that matches the package source and backend requirements.
6. If a mirror breaks dependency resolution, serves stale packages, lacks
   backend wheels, or changes CUDA/torch wheel availability, revert to the
   upstream index or a package-specific official wheel index.
7. Record the selected route in the private setup report and final environment
   handoff. Keep private proxy commands, tokens, and local network details out
   of generated public skill content.

Prefer temporary command-level mirror settings over mutating global user config:

```bash
PIP_INDEX_URL=https://pypi.org/simple \
PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cu128 \
/path/to/prefix/bin/python -m pip install <package>
```

For a regional PyPI mirror, use a temporary `-i` only when it is appropriate for
the package:

```bash
/path/to/prefix/bin/python -m pip install -i <trusted-pypi-mirror-simple-url> <package>
```

For conda, prefer command-level channels or repo-documented channels before
editing `.condarc`:

```bash
conda create -y -p /path/to/prefix -c conda-forge python=3.11 pip
```

Torch, JAX, TensorFlow, CUDA, ROCm, and vendor accelerator packages often need
official or backend-specific indexes. Do not replace those indexes with a
generic mirror unless the mirror is known to host the exact required wheels.

## Requirements and Extras

Do not blindly install every requirements file. Common meanings differ:

- `requirements.txt`: often runtime dependencies, but verify with docs.
- `requirements-dev.txt`, `dev-requirements.txt`: usually test/lint/dev tools; skip unless needed for import or smoke tests.
- `requirements-cuda.txt`, `requirements-gpu.txt`: backend-specific; use only if hardware supports it.
- `environment.yml`: may be the most reliable path for old conda-heavy projects; inspect before translating to prefix commands.

If metadata dependencies and requirements conflict, prefer the documented install path for the current backend and record the choice.

When multiple optional dependency groups are available, build a small mapping
before running pip:

```text
Group or file | Needed? | Evidence | Decision
[train] | no | training/ excluded | skip
[serve] | yes | docs/serving.md included by user | install --extra serve
requirements-dev.txt | no | lint/test tools only | skip
requirements-cuda.txt | no | CPU requested | skip
```

If the mapping is ambiguous and the choice would add large, slow, or
environment-breaking dependencies, ask for confirmation before installing the
broader option.

## Compiled Packages

Packages such as `flash-attn`, `xformers`, `apex`, `bitsandbytes`, `deepspeed`, custom CUDA extensions, `tokenizers`, `sentencepiece`, `llama-cpp-python`, and `faiss` are sensitive to Python, platform, compiler, CUDA/ROCm, and torch versions.

For torch CUDA extension packages:

- Install and verify torch first.
- Match the torch CUDA wheel tag to the driver and GPU architecture.
- Use `--no-build-isolation` for packages that compile against torch:

  ```bash
  MAX_JOBS=4 /path/to/prefix/bin/python -m pip install flash-attn --no-build-isolation -v
  ```

- Set `MAX_JOBS` conservatively on memory-limited hosts. CUDA compilation can consume several GB of RAM per job.
- If `nvcc` is unavailable and source compilation is required, either install a matching toolkit/compiler in conda or choose a fallback package path.

## Reproducibility Snapshot

After verification succeeds, capture a package snapshot for the private setup report:

```bash
/path/to/prefix/bin/python -m pip freeze
/path/to/prefix/bin/python -m pip check
```

The snapshot helps debug future failures. Do not copy local prefix paths into the public generated repo skill.
