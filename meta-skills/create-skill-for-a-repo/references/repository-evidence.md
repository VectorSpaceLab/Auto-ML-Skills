# Repository Evidence Discovery

## Purpose

Read this reference before extracting repo knowledge into a generated skill. The goal is to automatically discover which repository directories and files should inform the skill, instead of asking the user to list them manually.

## Build an Evidence Map First

Read the repo structure before extracting skills. First build a short evidence map that identifies which directories and files will be used for extraction. Do not ask the user to preselect these directories unless the repo is so large or ambiguous that automatic discovery cannot distinguish project code from vendored or generated material.

Record the evidence map in working notes before planning sub-skills:

```text
Evidence source | Why it matters | Planned use
src/package_name/ | canonical source root from pyproject package_dir | verify APIs, signatures, config objects, CLI modules
docs/ | public guides and install docs | workflow references and troubleshooting
examples/ | runnable user workflows | adapt smoke tests and recipes into skill scripts/references
scripts/ | repo-maintained automation | wrap safe reusable scripts inside generated skill
tests/ | behavior and edge-case evidence | confirm defaults, errors, and expected outputs
skills/*/SKILL.md | existing repo-local agent guidance | follow compatible structure and reuse validated guidance in the new self-contained skill
```

## Start from Metadata and Top-Level Structure

Inspect:

- Package metadata: `pyproject.toml`, `setup.py`, `setup.cfg`, `MANIFEST.in`, `requirements*.txt`, lockfiles, `tox.ini`, `noxfile.py`, CI workflows such as `.github/workflows/*`, and documented dependency files.
- Root docs: `README*`, `CHANGELOG*`, `CONTRIBUTING*`, `LICENSE*`, release notes, and public install guides.
- Public CLI or service metadata: console entry points, `__main__.py`, `cli.py`, `commands/`, `bin/`, shell completions, config schemas, and service launch scripts.
- Existing repo skills: `skills/` and nested skill directories with `SKILL.md`, when present. Exclude `skills/tests/` because it is a usability-test-case area, not an existing generated skill.

## Locate Source Roots

Treat source roots as essential evidence. The source code is the most reliable reference for public APIs, signatures, options, object relationships, runtime constraints, and confusing edge behavior. Use documentation, examples, and tests to learn intent and workflows, but use source code plus installed-package inspection to confirm API facts.

Common Python source root patterns:

- `src/<package_name>/`, `src/<normalized_repo_name>/`, and other `src/*` package directories.
- `<package_name>/`, `<normalized_repo_name>/`, and other top-level import packages containing `__init__.py` or namespace package files.
- `lib/`, `libs/`, `python/`, `packages/*/src/`, `packages/*/<package_name>/`, `projects/*/src/`, and monorepo package directories.
- Module directories that match package metadata, entry points, or public imports even if their names differ from the repository name.
- Important implementation-adjacent directories such as `configs/`, `conf/`, `config/`, `schemas/`, `templates/`, or `assets/` when the source imports or validates them.

## Discover Workflow and Documentation Sources

Common useful names:

- Documentation and guides: `docs/`, `doc/`, `documentation/`, `guide/`, `guides/`, `site/`, `website/`, `website/docs/`, `mkdocs.yml`, `readthedocs.yml`, `sphinx/`, `tutorials/`, `cookbook/`, and `recipes/`.
- Examples and runnable workflows: `examples/`, `example/`, `samples/`, `sample/`, `demos/`, `demo/`, `notebooks/`, `notebook/`, `colab/`, `scripts/`, `tools/`, `bin/`, `recipes/`, `experiments/`, and files whose names include workflow terms such as `train`, `infer`, `inference`, `predict`, `evaluate`, `eval`, `serve`, `deploy`, `finetune`, `preprocess`, or `convert`.
- Tests and behavior evidence: `tests/`, `test/`, `testing/`, `integration/`, `e2e/`, `benchmarks/`, `benchmark/`, `examples/tests/`, fixtures, golden files, and snapshot data.
- Configuration and data-format evidence: `configs/`, `conf/`, `config/`, `examples/configs/`, `templates/`, `schemas/`, `data/`, `datasets/`, fixture directories, and documented sample input/output files.
- Existing skills: `skills/*/SKILL.md`, `skills/*/references/`, and `skills/*/scripts/`, excluding `skills/tests/`.

If the user supplied specific reference directories, merge them into the evidence map rather than limiting extraction to only those directories.

If automatic discovery finds no docs, examples, tests, scripts, or obvious source roots, explicitly report the missing category and continue with the installed package, package metadata, and any source files that can be identified.

## De-Prioritize Noise

Ignore or de-prioritize generated, vendored, build, and environment directories unless package metadata explicitly points to them:

- `.git/`, `.venv/`, `venv/`, `env/`, `site-packages/`, `node_modules/`
- `dist/`, `build/`, `.tox/`, `.mypy_cache/`, `.pytest_cache/`, `__pycache__/`
- Generated docs output, downloaded model/data caches, and large binary artifacts

For each candidate evidence directory, sample representative files before reading deeply. Prioritize files that expose public workflows, APIs, CLIs, data formats, configuration, and errors.

## Use Evidence Correctly

Prefer existing documentation and tests for intended behavior. Use source code to resolve gaps or confirm details. Use the installed package to verify live import behavior, signatures, and runtime facts before writing generated skill claims.

Treat repo docs, examples, notebooks, and scripts as source material for the generated skill. Do not merely summarize them into `SKILL.md`; decide which parts should become bundled reference files, which examples should become bundled reusable scripts, and which details are unnecessary.
