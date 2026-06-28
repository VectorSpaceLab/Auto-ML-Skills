# DisCo Skills

This directory contains the DisCo skill-authoring workflow skills and the
`repo-skills-router` progressive routing-index template. They are used to build,
maintain, and export Agent Skills from local machine-learning repositories,
Python packages, and AI research papers.

Package/repo workflow skills:

- `prepare-repo-skill-env`: prepares and verifies an isolated Python
  inspection environment with the target repository package installed. It can
  bootstrap a private host Python for npm-installed machines with no Python,
  prefers conda when available, and falls back to venv.
- `create-repo-skill`: inspects repository evidence and the verified
  Python environment, then creates a self-contained repo-specific runtime skill.
- `verify-repo-skill`: creates assertion-backed usability test cases,
  runs content-level self-refine, checks safe native examples/tests when
  available, performs static verification, and writes final coverage and review
  handoff artifacts under `skills/tests/<skill-id>/`, with concrete cases in
  `test-cases/` and reports in `reports/`.
- `refresh-repo-skill`: refreshes an existing repo-specific skill after
  repository code, APIs, docs, examples, configs, or dependencies changed.
- `extend-repo-skill`: expands an already implemented skill with new or
  deeper coverage without discarding useful current guidance.
- `repo-skills-router`: template for a progressive routing index with a compact
  usage-scenario map and scenario pages that describe repo skill roles,
  differences, and selection guidelines.
- `import-repo-skills-to-agent`: exports DisCo's managed skills and
  `repo-skills-router` into another agent tool, asks before overwriting
  duplicate skills, and merges an existing target router. When exporting only
  selected skills, it builds a filtered router view for those selected skills
  instead of copying the full DisCo-managed router.

Paper workflow skills:

- `create-paper-skills`: entry skill for `disco --source paper`.
- `paper-skills-distiller`: orchestrates paper source resolution,
  modularization, module skill creation, recovery runtime preparation,
  recovery, analysis, and refinement.
- `plan-paper-skill-modules`: creates a paper profile, module plan, and module docs.
- `create-paper-module-skill`: converts module docs into generated module skills.
- `prepare-paper-recovery-env`: records bounded package, model, GPU, dataset,
  and runtime evidence for recovery.
- `recover-paper-result`: runs a fast recovery experiment without reading the original
  implementation repo.
- `analyze-paper-recovery`: compares recovery against the paper target and returns
  accept/refine/blocker feedback.

DisCo loads the bundled workflow skills automatically from its npm package
or binary assets. It does not use the bundled `repo-skills-router` copy as the
live writable index. During approved or auto-authorized imports, create or
update the user-level copy at
`~/.disco/agent/skills/repo-skills-router/SKILL.md`.
Those managed-library imports run under a global lock in the DisCo agent
directory, so concurrent auto-import sessions serialize the runtime skill copy
and the managed `update_repo_skills_router.mjs` rebuild.
DisCo's own `~/.disco/agent/skills/` directory is a managed skill
library and export source, not the runtime skill source for ordinary downstream
tasks.
Users do not need to install these skills separately to use the `disco`
command.

DisCo also manages `npm:@juicesharp/rpiv-ask-user-question`,
`npm:@juicesharp/rpiv-todo`, and `npm:pi-subagents` as default packages.
Dynamic workflow orchestration is built into DisCo as the `workflow` tool,
with state stored under `~/.disco/workflows`. The create workflow uses
todo tracking for progress visibility, structured questions for user
intervention points, subagents for parallel extraction, and the built-in
workflow tool for coordinated sub-skill generation and main-agent review.
Main-agent planning owns the sub-skill structure and canonical ids, while each
subagent receives a complete brief with evidence, target files, required
references/scripts, boundaries, and quality rubrics for its assigned sub-skill.

When these meta skills are copied into another agent such as Claude Code or
Codex, do not assume those DisCo-managed extensions exist. Follow the same
natural-language workflow with that agent's own task list, user-question,
subagent, or manual sequencing features.

## Use With DisCo

Run DisCo from the repository you want to inspect, or pass explicit paths:

```bash
./bin/disco
```

Select the source workflow explicitly when needed:

```bash
disco --source package -p "Create a skill for /path/to/repo using Python /path/to/env/bin/python"
disco --source paper -p "Use Distiller to process the runs in this config. config_path: /path/to/distiller_run_config.toml"
```

When `--source` is omitted, DisCo classifies the request as package/repo
or paper from the prompt and visible evidence, then asks for confirmation when
the source choice is ambiguous or expensive. Use `--source package` or
`--source paper` to force the route in scripts.

Typical create flow:

1. Ask DisCo to create a repo-specific skill for the target repository. If
   no Python inspection environment is provided, DisCo first analyzes the
   repository structure, asks for confirmation of the extraction scope by
   default, then uses `prepare-repo-skill-env` to create and
   verify the smallest inspection environment needed for that scope. If the
   create request says `auto decide`, DisCo agent-confirms the extraction
   scope from repo evidence and continues without routine manual scope approval.
2. When a verified Python executable is already available, include it in the
   create request to skip automatic environment preparation.
3. DisCo uses `verify-repo-skill` to create assertion-backed
   usability cases, run content-level self-refine, check safe native
   examples/tests when available, and produce review/test artifacts. By
   default, DisCo writes the publishable skill to
   `skills/<skill-id>/` when `skills/` does not exist yet, or
   `skills/disco/<skill-id>/` when the repo already has a `skills/`
   directory. Check-only artifacts go to `skills/tests/<skill-id>/`: concrete
   usability and native-backed cases live under `test-cases/`, while
   assertion/eval notes, native verification reports, final skill reports,
   human-review notes, publication checklists, and prompt samples live under
   `reports/`.
4. Approve import when DisCo asks through the structured user-question
   tool whether to copy the verified skill into `~/.disco/agent/skills/`,
   or include `auto import` in the original create request to authorize import
   after successful verification. Import only the runtime skill directory, not
   the review/test artifacts. The copied runtime skill must include
   `references/repo-routing-metadata.json`; while still holding the same import
   lock, DisCo runs `update_repo_skills_router.mjs` to rebuild and validate
   the user-managed `repo-skills-router` usage-scenario map and scenario pages.
   The runtime skill copy and router rebuild are one locked transaction,
   preventing parallel auto-import sessions from dropping each other's router
   entries.

Example prompt:

```text
Use create-repo-skill for /path/to/repo and put the generated skill under
/path/to/repo/skills/.
```

To delegate routine scope approval and final import approval for one create run:

```text
/skill:create-repo-skill auto decide, auto import for /path/to/repo and
put the generated skill under /path/to/repo/skills/.
```

To skip automatic environment preparation:

```text
Use create-repo-skill for /path/to/repo with /path/to/env/bin/python and
put the generated skill under /path/to/repo/skills/.
```

To refresh an existing skill after the repository changed:

```text
Use refresh-repo-skill to update /path/to/repo/skills/example-skill from
the current /path/to/repo code. Use /path/to/env/bin/python as evidence.
```

To extend an existing skill with new coverage:

```text
Use extend-repo-skill to add streaming inference coverage to
/path/to/repo/skills/example-skill. Use /path/to/repo and
/path/to/env/bin/python as evidence.
```

Paper create flow:

```text
Use Distiller to process the runs in this config.

config_path: /path/to/distiller_run_config.toml
```

For repeated paper runs, copy and fill
`create-paper-skills/assets/distiller-run-config-template.toml`. The
paper source may be a local PDF/text file, direct PDF URL, arXiv URL/id, or
paper title. The optional implementation repo may be a local repo, Git URL,
`none`, or `unknown`. Recovery must not read the original implementation repo.

## Optional Installation In Other Agents

Use this directory when you want the DisCo workflow in another agent that
supports Agent Skills.

Use `import-repo-skills-to-agent` when you want another agent tool to receive the
skills already imported into DisCo's managed library. It resolves a target
such as `~/.codex`, `~/.agents`, or `~/.claude`, asks before overwriting
duplicate non-router skills, and merges an existing target `repo-skills-router`
with a DisCo router view scoped to the selected skills. For subset exports,
unselected DisCo repo skills are not added to the target router.

For agents that read `~/.agents/skills/`:

```bash
mkdir -p ~/.agents/skills
cp -R meta-skills/prepare-repo-skill-env ~/.agents/skills/
cp -R meta-skills/create-repo-skill ~/.agents/skills/
cp -R meta-skills/create-paper-skills ~/.agents/skills/
cp -R meta-skills/paper-skills-distiller ~/.agents/skills/
cp -R meta-skills/plan-paper-skill-modules ~/.agents/skills/
cp -R meta-skills/create-paper-module-skill ~/.agents/skills/
cp -R meta-skills/prepare-paper-recovery-env ~/.agents/skills/
cp -R meta-skills/recover-paper-result ~/.agents/skills/
cp -R meta-skills/analyze-paper-recovery ~/.agents/skills/
cp -R meta-skills/verify-repo-skill ~/.agents/skills/
cp -R meta-skills/refresh-repo-skill ~/.agents/skills/
cp -R meta-skills/extend-repo-skill ~/.agents/skills/
cp -R meta-skills/repo-skills-router ~/.agents/skills/
cp -R meta-skills/import-repo-skills-to-agent ~/.agents/skills/
```

For project-local use:

```bash
mkdir -p .agents/skills
cp -R meta-skills/prepare-repo-skill-env .agents/skills/
cp -R meta-skills/create-repo-skill .agents/skills/
cp -R meta-skills/create-paper-skills .agents/skills/
cp -R meta-skills/paper-skills-distiller .agents/skills/
cp -R meta-skills/plan-paper-skill-modules .agents/skills/
cp -R meta-skills/create-paper-module-skill .agents/skills/
cp -R meta-skills/prepare-paper-recovery-env .agents/skills/
cp -R meta-skills/recover-paper-result .agents/skills/
cp -R meta-skills/analyze-paper-recovery .agents/skills/
cp -R meta-skills/verify-repo-skill .agents/skills/
cp -R meta-skills/refresh-repo-skill .agents/skills/
cp -R meta-skills/extend-repo-skill .agents/skills/
cp -R meta-skills/repo-skills-router .agents/skills/
cp -R meta-skills/import-repo-skills-to-agent .agents/skills/
```

After installing optional copies into another agent, restart that agent session
so it reloads available skills.

## Maintenance

The source copy is
`src/packages/coding-agent/src/disco/skills/`. Keep it synchronized with
the top-level optional-install mirror:

- `meta-skills/`

Build output is regenerated from the source copy:

- npm/dist resources: `src/packages/coding-agent/dist/disco-resources/skills/`
- binary resources: `src/packages/coding-agent/dist/disco-skills/`

Do not edit generated resource directories directly for source changes. Edit
the source copy, rebuild DisCo, and resync the `meta-skills/` mirror.
