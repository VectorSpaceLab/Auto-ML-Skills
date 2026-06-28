# Contributing

Auto-ML Skills treats skills as operating guidance that future agents may load
and follow. Good contributions are evidence-grounded, easy to audit, and clear
about how the skill was produced.

## Contribution Paths

You can contribute:

- new generated repo skills under `repo-skills/<skill-id>/`;
- improvements to existing repo skills;
- router, catalog, provenance, and documentation updates;
- lightweight workflow skills under `meta-skills/`;
- DisCo CLI source changes under `src/`.

## New Repo Skills

The most important contribution type is a new runtime repo skill.

Required files:

- `repo-skills/<skill-id>/SKILL.md`
- `repo-skills/<skill-id>/references/repo-provenance.md`
- `repo-skills/<skill-id>/references/repo-routing-metadata.json`
- sub-skills and references when the upstream repository has multiple major
  workflow areas
- small validation or preflight scripts when they make the skill safer to use

Keep runtime skill content separate from review artifacts. Publication-ready
content belongs in:

```text
repo-skills/<skill-id>/
```

Test cases, review notes, and generation reports should stay outside the
runtime skill directory unless they are intentionally part of the runtime
guidance.

## Router And Catalog Consistency

When adding, deleting, renaming, importing, or materially changing a repo skill,
update the router:

```text
repo-skills/repo-skills-router/SKILL.md
repo-skills/repo-skills-router/references/usage-scenarios.md
repo-skills/repo-skills-router/references/scenarios/*.md
```

Router entries should help an agent choose among skills. They should not copy
the full skill instructions.

Update the public catalog when the imported skill library changes:

```text
docs/imported-repo-skills.md
```

The catalog should stay aligned with `repo-routing-metadata.json` and
`repo-provenance.md`.

## Improving Existing Repo Skills

Improvements are welcome when a skill is stale, unclear, incomplete, or too
hard for an agent to use.

Rules:

- Ground changes in source evidence, upstream docs, examples, or inspected
  package behavior.
- Preserve correct existing guidance.
- Update provenance when the source commit, package version, or evidence set
  changes.
- Update routing metadata when coverage or selection guidance changes.
- Keep scripts deterministic and safe. Avoid downloads, training, server
  startup, or destructive filesystem operations unless clearly gated.

Focused checks:

```bash
find repo-skills/<skill-id> -type f -name '*.py' -print0 | xargs -0 -r python -m py_compile
find repo-skills/<skill-id> -type f | sort
```

## Pull Request Requirements

For every PR that adds or modifies generated repo skills, include:

- the upstream repository URL and source commit or tag;
- the model and provider used to produce the skill;
- the reasoning or thinking level used, such as `low`, `medium`, `high`, or the
  provider-specific equivalent;
- whether the skill was produced by DisCo, by copied meta skills, or by manual
  editing;
- the verification commands or review steps that were run;
- any known gaps, skipped checks, unavailable credentials, or environment
  limits;
- confirmation that `repo-skills-router` was updated when routing changed.

If multiple models or passes were used, list each model and its role, for
example generation, review, refinement, or verification.

## Documentation Changes

Documentation is bilingual. When changing an English page, update the
corresponding Chinese page, and vice versa.

Rules:

- Keep paths relative to the Markdown file location.
- Prefer concrete commands and locations over general descriptions.
- Keep README pages concise and move detailed workflows into `docs/`.
- Avoid duplicating language-switch links in every document page. The README
  files and MkDocs language switcher are the main language entry points.
- If the catalog changes, keep the catalog and localized index aligned.

Useful checks:

```bash
python - <<'PY'
from pathlib import Path
for p in sorted(Path('docs').glob('*.md')):
    text = p.read_text()
    if '\t' in text:
        print(f'tab: {p}')
PY
```

To preview the optional MkDocs site:

```bash
python -m pip install mkdocs-material mkdocs-static-i18n
mkdocs serve
mkdocs build --strict
```

## Meta Skill Changes

The top-level `meta-skills/` directory is a lightweight mirror for external
agents. Keep it understandable without DisCo-only extensions.

When updating meta skills:

- State expected inputs and outputs explicitly.
- Ask for user confirmation at expensive or destructive points unless the user
  authorized agent-decided behavior.
- Keep environment changes isolated.
- Keep generated runtime skill content separate from tests and reports.
- Update the [`meta-skills/`](meta-skills/) mirror when names or workflow boundaries
  change.

## DisCo Source Changes

The DisCo CLI source lives under `src/`.

Common checks:

```bash
cd src
npm install --ignore-scripts
npm run build
npm run check
```

For publish preparation, dry-run package contents before publishing:

```bash
npm pack --workspace packages/ai --dry-run
npm pack --workspace packages/tui --dry-run
npm pack --workspace packages/agent --dry-run
npm pack --workspace packages/coding-agent --dry-run
```

Do not hand-edit generated `dist/` files or standalone binary runtime assets as
source changes.

## Final Checklist

Before handing off a change:

- README and docs links point to existing files.
- English and Chinese docs are both updated when applicable.
- Runtime skill changes include provenance and source evidence.
- Router and catalog changes are consistent with skill changes.
- PR text lists the model, provider, reasoning or thinking level, and
  verification steps.
- Scripts touched by the change have been syntax-checked or otherwise
  verified.
- The final summary states what was verified and what was not.
