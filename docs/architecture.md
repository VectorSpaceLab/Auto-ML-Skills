# Architecture

Auto-ML Skills separates the published skill library from the tooling that
creates and maintains it.

## Current Repository Snapshot

```text
Auto-ML-Skills/
  README.md
  README.zh-CN.md
  CONTRIBUTING.md
  CONTRIBUTING_CN.md
  docs/
  meta-skills/
  repo-skills/
  scripts/
  src/
```

The current checkout contains both the published skill library and the DisCo
TypeScript source tree. Runtime repo skills live under `repo-skills/`, the
public optional-install workflow mirror lives under `meta-skills/`, and the
full bundled DisCo workflow source lives under
`src/packages/coding-agent/src/disco/skills/`.

## Source Layout

The DisCo source tree lives at `src/`:

```text
src/
  package.json
  packages/
    ai/
    tui/
    agent/
    coding-agent/
```

Expected package roles:

| Package | Role |
| --- | --- |
| `packages/ai` | Provider integrations, model registries, streaming utilities, environment API-key handling, and image/model helpers. |
| `packages/tui` | Terminal UI components and rendering infrastructure. |
| `packages/agent` | Agent core, loop, harness, prompts, skill loading, and shared agent abstractions. |
| `packages/coding-agent` | CLI package exposing `disco`, interactive/print modes, project trust, session management, built-in tools, DisCo workflow skills, and dynamic workflow orchestration. |

The workspace is private at the root. Publishable npm packages are under
`src/packages/`. The CLI package is `@auto-ml-skills/disco` and exposes the
`disco` command.

## Skill Authoring Pipeline

DisCo has two source workflows: package/repo and paper. Both are integrated in
the `disco` CLI. The bundled workflow skill source is under
`src/packages/coding-agent/src/disco/skills/`.

### Package/Repo Flow

At a high level, DisCo's repo-skill pipeline is:

1. Classify source type: package/repo or paper.
2. Analyze source structure and confirm scope.
3. Prepare a minimal inspection environment.
4. Gather evidence from source, docs, examples, tests, metadata, and live
   package inspection.
5. Plan a top-level skill and sub-skill structure.
6. Generate and integrate self-contained runtime guidance.
7. Run the built-in verification workflow.
8. Import approved runtime skills into a managed library.
9. Rebuild routing metadata and router scenario pages under a lock.

The create flow does not treat verification as optional cleanup.
`create-repo-skill` hands the integrated draft to `verify-repo-skill` before a
skill is ready to import or publish.

### Verification Gate

`verify-repo-skill` owns the final quality gate for created, refreshed, or
extended repo skills. It writes check-only artifacts outside the runtime skill
directory, normally under:

```text
<repository>/skills/tests/<skill-id>/
  test-cases/
  reports/
```

The verification stage covers:

- assertion-backed usability case generation;
- content-level self-refine against the selected source scope and generated
  skill tree;
- representative native repo example/test checks when they are safe and
  available;
- static quality gates for links, self-containment, provenance, routing
  metadata, local-path leaks, and frontmatter shape;
- final coverage, review, publication, and handoff reports;
- import readiness and, when approved or auto-authorized, locked import into
  DisCo's managed skill library.

Runtime skill directories should not contain usability cases, eval notes,
verification reports, human-review notes, publication checklists, or prompt
samples. Those belong under the review/test artifact directory.

### Paper Flow

The paper-to-skill flow is integrated in the DisCo CLI via `--source paper`.
The current source tree includes:

```text
src/packages/coding-agent/src/disco/skills/
  create-paper-skills/
  paper-skills-distiller/
  plan-paper-skill-modules/
  create-paper-module-skill/
  prepare-paper-recovery-env/
  recover-paper-result/
  analyze-paper-recovery/
```

The flow resolves a paper source, optionally uses an implementation repository
as pre-recovery evidence, modularizes the paper, creates and validates
module-level skills, prepares bounded runtime evidence, runs a recovery
experiment without reading the original implementation repo, analyzes gaps,
refines within the configured `iteration_budget` when needed, and writes
attempt artifacts plus final reports. The default repeated-run input is a TOML
run config based on the bundled `distiller-run-config-template.toml`. Batch
configs are normalized to JSON under a workspace-level `paper2skills_runs/`
area, then each selected paper/run gets its own run root, source acquisition
record, generated-skills root, and attempt directory.

Run config normalization records fields such as `paper_slug`, `paper_source`,
`original_repo_source`, `repo_discovery_mode`, `recovery_target`,
`recovery_mode`, `runtime_constraints`, `iteration_budget`, and
`generated_skills_root`. New runs default to `recovery_mode: hard` and
`iteration_budget: 10`; `hard` mode does not accept reduced, proxy, toy,
smaller-model, or fallback recovery as success, while `soft` mode may accept a
declared proxy only when executable evidence and mechanism checks pass.

The run root also records source acquisition when needed, normally at
`source/source_resolution.json`. Each paper attempt follows a contract shaped
like:

```text
run_manifest.json
run_config.normalized.json   # preferred when a config was used
paper_profile.md
module_plan.json
modules/
generated_skills_validation/
reports/
  generated-skills/
  verification/
  final/
    final_report.md
    final_report.json
environment/
  runtime_handoff.json
  logs/command_log.json
recovery/
  experiment_plan.md
  experiment_validation.json
  source_manifest.json
  recovery_result.json
  logs/
    experiment_command_log.json
    generated_skill_invocations.json
analysis/
  analysis_report.json
  feedback.md
final_validation.json
```

Paper recovery has a stricter source boundary than modularization: the optional
implementation repository may inform module planning and module-skill creation,
but recovery must use only the paper, module docs, generated skills, runtime
handoff, data, and general package documentation. The recovery result must be
backed by executable command logs, and the attempt must prove that generated
module skills were called, imported, or cross-checked rather than bypassed by a
one-off handwritten recovery script.

### Bundled Workflow Skills

The package/repo workflow skills include:

| Workflow Skill | Role |
| --- | --- |
| `prepare-repo-skill-env` | Create or verify a scoped Python inspection environment after extraction scope is known. |
| `create-repo-skill` | Analyze source evidence, plan and generate the runtime skill, then hand off to verification. |
| `verify-repo-skill` | Own assertion-backed usability cases, content self-refine, native checks, static gates, reports, and import readiness. |
| `refresh-repo-skill` | Update an existing repo skill against changed upstream source, then verify. |
| `extend-repo-skill` | Add deeper coverage to an existing skill, then verify. |
| `repo-skills-router` | Provide the progressive routing index for an imported skill library. |
| `import-repo-skills-to-agent` | Export DisCo-managed skills and a scoped router into Codex, Claude Code, or another agent target. |

The paper workflow skills include:

| Workflow Skill | Role |
| --- | --- |
| `create-paper-skills` | Entry point for `disco --source paper`. |
| `paper-skills-distiller` | Orchestrate source resolution, modularization, module-skill creation, recovery, analysis, refinement, and final reports. |
| `plan-paper-skill-modules` | Create paper profile, module plan, and module docs. |
| `create-paper-module-skill` | Convert module docs into generated module skills and validation checks. |
| `prepare-paper-recovery-env` | Record bounded package, model, GPU, dataset, command-log, and runtime handoff evidence. |
| `recover-paper-result` | Run a bounded recovery experiment using generated skills and save executable command plus generated-skill invocation evidence. |
| `analyze-paper-recovery` | Compare recovery evidence against the paper target, experiment gate, source boundary, and mechanism checks, then return accept/refine feedback. |

## Runtime Skill Shape

The runtime skill shape follows progressive disclosure:

```text
SKILL.md                         # first file an agent reads
references/                      # supporting evidence and longer notes
sub-skills/<area>/SKILL.md       # deeper task-specific guidance
scripts/                         # small helpers for checks/preflight
```

`SKILL.md` should be useful on its own and route deeper only when the task needs
more detail. References and scripts should be linked from the skill text when
they are expected to be used.

Generated repo skills are expected to include:

- `references/repo-provenance.md` with source commit, package version, dirty
  state, and evidence paths;
- `references/repo-routing-metadata.json` for managed router placement;
- `disable-model-invocation: true` in repo-skill root and sub-skill frontmatter
  so compatible agents keep `repo-skills-router` as the model-visible entry
  point;
- bundled references or scripts instead of links to the original checkout when
  future use depends on those details.

## Router

The repo-skills router is a generated or maintained index for a skill library:

```text
repo-skills/repo-skills-router/
  SKILL.md
  references/
    usage-scenarios.md
    maintenance.md
    scenarios/
```

It is not a replacement for individual skills. It gives the first-pass
selection map and points agents to the right scenario page and candidate skill.

## Managed Library

In DisCo, the user-level managed library lives under:

```text
~/.disco/agent/skills/
```

The managed library is an import/export source, not necessarily the runtime
skill source for every downstream agent. Use `import-repo-skills-to-agent` to
export managed skills and the router into targets such as `~/.agents`,
`~/.codex`, or `~/.claude`.

When exporting to Codex, the import workflow also adds target-side
`agents/openai.yaml` files with `policy.allow_implicit_invocation: false` to
non-router repo skills, because Codex does not use the
`disable-model-invocation` frontmatter field for that policy.

Approved or auto-authorized imports are serialized with the verification
workflow's import lock. The same locked transaction copies the runtime skill
directory, validates `references/repo-routing-metadata.json`, and rebuilds the
managed `repo-skills-router` scenario map. Router updates should be generated
from structured metadata, not hand-edited as free-form Markdown during import.

## Source Of Truth

Use these source-of-truth rules:

- Runtime repo skills in this repository live under `repo-skills/`.
- Lightweight external-agent workflow skills live under `meta-skills/`,
  including package/repo and paper-to-skill workflows.
- Bundled DisCo workflow skills live under
  `src/packages/coding-agent/src/disco/skills/`.
- Edit bundled workflow skill source in `src/`, then rebuild/resync
  `meta-skills/` mirrors as needed.
- Verification and review artifacts live outside runtime skill directories,
  normally under `skills/tests/<skill-id>/` in the inspected repository.
- Do not hand-edit generated `dist/` resources as the source of truth.
- Keep docs explicit about whether a feature belongs to the runtime skill
  library, the lightweight external-agent mirror, or the DisCo CLI source.
