# Evaluation, Verification, and Handoff

## Purpose

Read this reference after generating the skill and usability test cases. It defines the lightweight self-refine loop, verification checklist, final creation report, publication notes, and quality bar.

## Evaluate and Self-Refine

After writing a draft, do not stop at first pass. Run a lightweight evaluation loop to catch thin, overpacked, or hard-to-use skills before delivery.

Use the generated usability test case directories as the primary source of realistic user prompts. Read each selected case's `user_request.txt` as the prompt and its `README.md` as the expected-behavior notes. Pick a focused subset when the test set is large, making sure the subset includes:

- At least one novice or broad-purpose prompt.
- At least one expert or specific prompt.
- At least one ordinary workflow.
- At least one troubleshooting or edge-case prompt.

When practical, also save a small machine-readable eval subset in the generated skill directory as `evals/evals.json`:

```json
{
  "skill_name": "repo-name",
  "evals": [
    {
      "id": 1,
      "prompt": "Use this repo skill to set up the package and run a minimal inference smoke test.",
      "expected_output": "A correct setup path, verified import command, and smoke-test result.",
      "files": [],
      "assertions": [
        "The output uses the install command documented in the root SKILL.md",
        "The output runs or references the generated smoke-test script",
        "The output reports a concrete import or runtime verification result",
        "The output does not depend on scripts or docs from the original repo checkout",
        "The output does not mention the user's temporary Python environment",
        "All generated skill directory names, frontmatter name fields, and evals skill_name values are lowercase-hyphen identifiers",
        "YAML frontmatter strings containing colons are wrapped in double quotes",
        "Generated SKILL.md frontmatter does not contain disable-model-invocation: true unless the user explicitly requested manual-only invocation",
        "The generated skill tree covers every public capability identified in the coverage matrix",
        "The relevant sub-skill has enough references, scripts, examples, parameters, and troubleshooting to complete the task without reopening the original repo"
      ]
    }
  ]
}
```

For each test prompt, write concrete assertions before judging the result. Good assertions check observable outcomes: a file exists, a command is present, an API signature is correct, a workflow references the right sub-skill, or troubleshooting advice names the expected failure mode.

When subagents or isolated runs are available, run at least one fresh agent against the draft skill with no access to your research notes. Ask it to complete a test prompt using the generated skill and save or summarize the result. If isolated runs are not available, review from the perspective of a future agent that can only read the generated skill files.

Grade assertions with `PASS` or `FAIL` and cite evidence. Then perform a qualitative review:

- Triggering: would the root and sub-skill `description` fields plausibly trigger for natural prompts from the usability test case `user_request.txt` files, including novice prompts that do not know exact API names?
- Breadth: compare the generated skill tree against the coverage/depth matrix.
- Depth: can a future agent complete common workflows using only the nearest `SKILL.md` plus linked bundled references/scripts?
- Routing: can the agent identify the correct sub-skill from the root router?
- Concrete requirements: are commands, imports, config files, data assumptions, and optional dependencies concrete and verified?
- Self-containment: does any workflow force the agent back into the original repo or depend on original repo paths?
- Privacy: does any generated file leak local Python environment details?
- Structure: are identifiers normalized, frontmatter parseable, and bulky material moved into references/scripts?

Save a short evaluation note when practical, for example `evals/iteration-1.md`, with prompts, assertions, grades, failures, and revisions made.

Treat `evals/` as a development artifact, not part of the public runtime skill. Do not link `evals/` from generated root or sub-skill `SKILL.md` files as user-facing documentation.

Treat usability test case directories under the configured test case output path as review artifacts. They may be kept and shared as a test suite when useful, but they are not required for the generated skill to work at runtime.

If any assertion fails or the qualitative review reveals a gap, revise the generated skill before finishing and repeat the focused check.

## Verification Checklist

Before finishing, confirm:

- The directory layout matches the intended output structure.
- Each generated `SKILL.md` has valid frontmatter.
- Every frontmatter `description` is double-quoted, and YAML-sensitive strings are escaped.
- No generated `SKILL.md` contains `disable-model-invocation: true` unless the user explicitly requested a manual-only skill.
- The generated root directory basename is a canonical lowercase-hyphen skill id, not a raw mixed-case repo name.
- Every `name` field uses only lowercase letters, numbers, and hyphens, is no longer than 64 characters, and matches the corresponding generated skill directory basename.
- `evals/evals.json` uses the canonical root skill id in `skill_name` when that file exists.
- Root `SKILL.md` routes to sub-skills instead of duplicating all details when sub-skills exist.
- Every sub-skill `SKILL.md` routes to nearby references and scripts instead of becoming a manual.
- Root `SKILL.md` includes package installation instructions and a minimal verification command.
- Package installation instructions are public and reproducible, not copied from the user's temporary Python environment.
- The generated skill covers every user-facing capability found in the repo, docs, examples, tests, package metadata, and installed package inspection.
- The coverage/depth matrix has no unmapped public capabilities.
- Every non-trivial public capability maps to a root or sub-skill entry plus enough bundled references/scripts for practical use.
- Each sub-skill passes a depth check: workflows, APIs, commands, configs, inputs/outputs, examples, troubleshooting, and safe scripts are sufficient for future agents to avoid reopening original source code or docs for ordinary use.
- Sub-skill boundaries are explained, functionally independent, and not just copied from folder names.
- References and scripts are linked from a nearby `SKILL.md` with clear read/run guidance.
- Every linked reference or script path resolves inside the generated skill directory.
- Generated `SKILL.md` files do not instruct future agents to run, read, or open scripts, docs, examples, notebooks, or configs from the original repo checkout.
- Generated skill files do not mention the user's local Python executable, virtualenv or conda name, activation command, machine-specific path, local checkout path, or `pip show` installation directory.
- `references/` is non-empty wherever repo docs, examples, notebooks, tests, or CLIs provided reusable material.
- `scripts/` exists wherever the repo has reusable scripts, example pipelines, repeatable diagnostics, or smoke-test opportunities that can be safely adapted.
- `troubleshooting.md` exists in relevant `references/` directories when troubleshooting information is available, or the user was asked when the repo alone was insufficient.
- No `SKILL.md` exceeds its intended size without a clear reason.
- No detailed content is duplicated between `SKILL.md` and reference files.
- Common workflows can be completed from the generated skill tree and a freshly installed public package environment without rereading the original repo.
- Usability test case directories were generated in the configured test case output path.
- Usability test cases include diverse user familiarity levels, diverse scenario difficulty, and broad coverage of major sub-skills and public capabilities.
- Every usability test case is a directory named with the target root or sub-skill id plus a descriptive scenario slug.
- Every usability test case directory contains `user_request.txt` with only the directly copyable future-user prompt.
- Every usability test case directory contains `README.md` with user persona, scenario coverage, expected successful behavior, and failure signals.
- Multiple scenario directories exist for the same sub-skill when that sub-skill has multiple important scenarios.
- The generated root and sub-skill `description` values are broad enough to trigger on the natural prompts represented by the usability test cases.
- `tests/<chosen-skill-id>/index.md` or the equivalent user-specified index summarizes case coverage and flags untested major capabilities.
- Usability test cases are not linked from generated `SKILL.md` files as runtime documentation unless the user explicitly requested that.
- The eval/self-refine pass was performed, assertions were graded with evidence, and gaps were fixed or explicitly reported.
- `evals/` is treated as a development artifact.
- The final handoff includes a short creation report covering repo evidence used, generated sub-skills, usability test case coverage, and self-refine results.
- Safe import/signature checks were run in the provided Python environment for APIs mentioned in the skill, then translated into public package facts.
- Stale placeholders, speculative claims, and unnecessary empty directories were removed.

## Final Handoff

When presenting the generated skill to the user, include a short creation report. Keep it concise, but do not omit these items:

- Repo evidence used: summarize the repository directories and evidence categories consulted, such as source roots, docs, examples, scripts, tests, configs, existing skills, and installed-package inspection.
- Generated skill content: give the generated skill path and summarize the root skill plus each generated sub-skill, including its purpose and main covered capabilities.
- Usability test cases: give the test case output path, the approximate count, the per-sub-skill or per-capability distribution, and representative scenario names.
- Self-refine result: summarize the lightweight checks performed, important revisions made, and any explicit remaining gaps.

Also include a short publication note:

- The generated `SKILL.md`, `sub-skills/`, `references/`, and `scripts/` are the public skill content.
- The generated usability test case directories under the configured test case output path are review cases for checking how future users may use the skill.
- The `evals/` directory, if present, is for self-refine/development review and may include prompts, grades, failures, or feedback that should not be published by default.
- Before sharing the skill with the community, the user should delete `evals/`, add it to ignore rules, or exclude it from packaging unless they intentionally want to publish the eval suite.

## Quality Bar

The generated skill must be:

- Consistent: aligned with the original repo's implementation, public APIs, terminology, and documented behavior.
- Correct: free of false API claims, invalid commands, broken imports, inaccurate signatures, or fabricated capabilities.
- Comprehensive: makes all user-facing capabilities reachable through routers, sub-skills, references, and scripts.
- Deep enough: each non-trivial sub-skill contains or links to enough bundled guidance for future agents to perform common tasks without returning to the original repo.
- Self-contained: does not depend on source repo docs, examples, notebooks, configs, or scripts remaining available after skill generation.
- Public-ready: omits user-specific inspection environment details and describes only reproducible public installation and runtime requirements.
- Well-structured: keeps `SKILL.md` files readable and moves depth into the nearest `references/` or `scripts/` directory.
- Tested: includes usability test case directories plus a lightweight eval/self-refine pass.
- Reasonable: free of vague, contradictory, misleading, or unjustified guidance that could confuse future agents.
