---
name: verify-repo-skill
description: "Verifies a generated or refreshed repo-specific Agent Skill by creating assertion-backed usability test cases, running content-level self-refine, checking native repo examples/tests when available, checking static quality gates, and producing final coverage and handoff artifacts. Use this after create-repo-skill, refresh-repo-skill, or extend-repo-skill finishes an integrated runtime skill draft, and whenever a repo skill needs usability or publication verification."
---

# Verify Repo Skill

## Purpose

Use this skill after a generated, refreshed, or extended repo skill draft exists.
It owns usability test case generation, content-level self-refine, native
repo test/example verification after whole-skill integration, static
verification, final coverage report creation, review-package creation, and
final verification handoff.

This skill does not create the repo skill from source evidence. It verifies and
refines an already-created runtime skill directory using the original creation
context, evidence notes, coverage/depth matrix, planned sub-skill structure, and
review rubrics when available. When this skill is called after
`create-repo-skill`, the runtime skill should already include all
sub-skills, root routing, repo-level references/scripts, repo provenance, and a
main-agent integration pass over parallel subagent outputs.

## Inputs

Resolve these before writing verification artifacts:

- Runtime repo skill directory containing `SKILL.md`.
- Review/test artifact directory. If omitted, use the artifact root selected by
  the calling workflow, normally `<repository-path>/skills/tests/<skill-id>/`.
  Write concrete test cases under `test-cases/` and reports or review
  documents under `reports/`.
- Repository path or evidence summary used to create the skill.
- Python inspection handoff or public package facts used by the skill, when
  available.
- Coverage/depth matrix, target file tree, sub-skill plan, and subagent review
  rubrics from the calling workflow.
- Integration artifacts from the calling workflow, such as integration notes,
  native test/example candidate map, and long-tail gap register, when available.
- Import decision policy from the calling workflow. Default to
  `importAfterVerification: ask`; use `auto-import` only when the original user
  request explicitly delegated the final import decision.
- Any user-provided verification focus, such as required scenarios, specific
  workflows, known failures, or publication gates.

Do not write check-only artifacts into the runtime skill directory. Keep
usability cases under `test-cases/` in the review/test artifact directory, and
keep evals, verification reports, human-review notes, publication checklists,
prompt samples, staleness audits, benchmark notes, and final reports under
`reports/` in that artifact directory.

## Reference Map

Read these references as the workflow reaches each stage:

- [references/usability-test-cases.md](references/usability-test-cases.md): how
  to create realistic, evidence-backed, assertion-backed user-prompt case
  directories and coverage indexes.
- [references/evaluation-verification-and-handoff.md](references/evaluation-verification-and-handoff.md):
  content-level self-refine, native repo test/example verification, static
  verification checklist, final skill coverage report, review package, final
  handoff, import guidance, and quality bar.
- [scripts/run_native_cases.py](scripts/run_native_cases.py): optional
  manifest-driven helper for running preselected safe native repo verification
  commands with timeouts and JSON output. Use it only after an agent has
  classified candidate commands as safe for the current environment.
- [scripts/with_import_lock.mjs](scripts/with_import_lock.mjs): required helper
  for wrapping the approved or auto-authorized import transaction that writes
  `~/.disco/agent/skills/` and the live `repo-skills-router`.
- [scripts/update_repo_skills_router.mjs](scripts/update_repo_skills_router.mjs):
  required managed updater for rebuilding and validating the live
  `repo-skills-router` from structured routing metadata inside the same locked
  import transaction.

## Required Workflow

Use todo tracking or a visible checklist so the user can follow verification
progress.

1. Verification setup:
   Confirm the runtime skill directory, artifact directory, source repo context,
   creation evidence, planned sub-skill structure, coverage/depth matrix, and
   any user-specified verification focus. Inspect the generated root
   `SKILL.md`, sub-skills, references, scripts, repo provenance, integration
   notes, native test/example candidate map, and long-tail gap register before
   writing verification artifacts.
2. Usability test case generation:
   Read [references/usability-test-cases.md](references/usability-test-cases.md).
   Create realistic, difficult, evidence-backed case directories under
   `<artifact-root>/test-cases/`, including `user_request.txt`, `README.md`,
   optional fixtures, per-case `assertions.json`, and an `index.md` that maps
   cases to root or sub-skill capabilities. The generated cases should stress
   routing, workflow depth, support workflows, troubleshooting, and source-repo
   dependency avoidance, not just happy-path prompts. For every generated
   sub-skill, create one or two new difficult synthetic cases in addition to
   cases derived directly from original repo tests/examples. After all
   sub-skills are integrated, also create one or two integrated difficult cases
   under `test-cases/integration/`; prefer adapting original repo tests/examples
   from the native candidate map, and synthesize only when no suitable native
   integrated case exists.
3. Content-level self-refine:
   Read [references/evaluation-verification-and-handoff.md](references/evaluation-verification-and-handoff.md).
   Review the whole skill against the user request, confirmed repository
   include/exclude map, planned sub-skill structure, subagent rubrics, coverage
   matrix, self-containment, privacy, routing, references, scripts, and
   assertion-backed usability cases. Revise the runtime skill when the review
   finds actionable gaps.
4. Native repo test/example verification:
   Using the native test/example candidate map from the calling workflow or one
   built during setup, select a safe representative subset of original repo
   examples, tests, CLI help checks, tiny-fixture checks, or smoke scripts.
   Run only commands that are safe for the current environment: short,
   deterministic, no network, no credentials, no destructive writes, no large
   downloads, and no long training unless the user explicitly approves. Record
   PASS, SKILL_GAP, NATIVE_FAIL, SKIP_UNSAFE, and SKIP_NOT_SELECTED results
   under the artifact directory. Use failures or gaps to revise the runtime
   skill before static verification when the generated skill is wrong or thin.
5. Static verification, final report, and review package:
   Run the static checks from the verification reference. Save verification
   reports, final skill coverage report, human-review notes, publication
   checklist, prompt samples, native verification reports, and any
   eval/self-refine notes under `<artifact-root>/reports/`.
6. Handoff and import readiness:
   Report the runtime skill path, artifact path, usability coverage, native
   verification results, failures fixed, remaining long-tail gaps, and whether
   the skill is ready to import. If `importAfterVerification` is `ask`, use
   `ask_user_question` when available to ask whether to import the verified
   runtime skill into `~/.disco/agent/skills/`; do not only ask in a normal
   assistant message and stop. If `importAfterVerification` is `auto-import`
   and the skill is verified/import-ready with no unresolved high or critical
   failures, import without asking again and state that the original create
   request authorized auto-import. If import is approved or auto-authorized,
   run the whole import as one locked transaction through
   `scripts/with_import_lock.mjs`: copy only the runtime skill directory into
   `~/.disco/agent/skills/`, ensure the imported skill contains
   `references/repo-routing-metadata.json`, then run
   `scripts/update_repo_skills_router.mjs --already-locked` inside that same
   process to rebuild and validate the live DisCo `repo-skills-router`.
   Do not hand-edit router Markdown as the import mechanism. While holding the
   lock, the updater re-reads the current managed skill directory and live router
   before applying this import so concurrent sessions cannot overwrite each
   other's router entries. Do not synchronize into other agent tools during this
   workflow; use `import-repo-skills-to-agent` only when the user explicitly asks to
   export DisCo's managed skill library.

## Non-Negotiables

- Do not put usability cases, evals, verification reports, human-review notes,
  publication checklists, prompt samples, or other check-only artifacts inside
  the runtime skill directory.
- Do not mix concrete test cases and review/report documents directly under the
  artifact root. Test cases belong under `test-cases/`; review and verification
  documents belong under `reports/`.
- Do not mark a repo skill verified if runtime Markdown links point outside the
  skill tree, required bundled references/scripts are missing, local
  environment paths leak into public files, or root/sub-skill routing is too
  thin to use.
- Do not treat the generated usability test cases as runtime documentation.
- Do not treat skipped native repo examples/tests as passing. Record the skip
  reason and decide whether a synthetic assertion-backed case should cover the
  same capability.
- Do not run original repo native examples/tests before the generated skill has
  been fully integrated across all sub-skills; native ground-truth checks are a
  final verification gate, not a sub-skill drafting shortcut.
- Do not import a skill before high or critical verification failures are fixed
  or explicitly accepted by the user.
- Do not import a skill or update the live DisCo `repo-skills-router`
  outside the global import lock. The lock must cover the runtime skill copy,
  router creation from the template when missing, structured metadata read,
  managed router rebuild, stale-file removal, and final existence/link checks.
- Do not update `repo-skills-router` by free-form Markdown editing during
  import. The import transaction must call
  `scripts/update_repo_skills_router.mjs` after copying the runtime skill and
  writing or updating `references/repo-routing-metadata.json`.
- Do not treat `auto-import` as permission to overwrite an unrelated existing
  managed skill. If the target import directory already exists and this workflow
  is not explicitly updating that exact skill, ask before replacing it or choose
  a non-conflicting import name when that is consistent with the generated skill
  id policy.
- Keep the final report clear about what was verified, what was revised, where
  artifacts were written, and what risk remains.

## Output Summary

By the end, the user should have:

- A verified or explicitly-not-verified runtime repo skill directory.
- Usability case directories plus `index.md` under
  `<artifact-root>/test-cases/`.
- One or two difficult synthetic cases for each sub-skill, plus one or two
  integrated difficult cases under `<artifact-root>/test-cases/integration/`.
- Optional self-refine notes and a clean review package under
  `<artifact-root>/reports/`.
- Native repo test/example candidate and verification reports under
  `<artifact-root>/reports/verification/` when original repo examples/tests
  were available.
- A final skill coverage report comparing original repo capabilities,
  generated skill coverage, native verification results, and remaining
  long-tail gaps.
- A concise verification handoff with import readiness and a
  `repo-skills-router` routing update when import is approved or auto-authorized.
