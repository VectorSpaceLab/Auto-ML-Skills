# Install Planning

## Purpose

Read this reference before creating the conda environment or installing the repo package. The goal is to make the install plan match the repository's real package metadata, Python support, dependencies, and backend expectations instead of guessing from the repo directory name.

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

Install extras only when they are needed for the repo capability being inspected:

```bash
/path/to/prefix/bin/python -m pip install -e "/path/to/repo[cuda,serve]"
```

## Requirements and Extras

Do not blindly install every requirements file. Common meanings differ:

- `requirements.txt`: often runtime dependencies, but verify with docs.
- `requirements-dev.txt`, `dev-requirements.txt`: usually test/lint/dev tools; skip unless needed for import or smoke tests.
- `requirements-cuda.txt`, `requirements-gpu.txt`: backend-specific; use only if hardware supports it.
- `environment.yml`: may be the most reliable path for old conda-heavy projects; inspect before translating to prefix commands.

If metadata dependencies and requirements conflict, prefer the documented install path for the current backend and record the choice.

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
