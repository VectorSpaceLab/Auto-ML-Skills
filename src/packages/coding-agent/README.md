# DisCo CLI

DisCo is the command line interface for Auto-ML-Skills. It helps coding agents
create, verify, maintain, and import reusable Agent Skills for machine-learning
software and AI research papers.

Use DisCo when an agent needs repository-grounded guidance instead of generic
API guesses, or when you want to distill a paper into smaller skills that can be
used and tested in later recovery runs.

## Install

```bash
npm install -g @auto-ml-skills/disco
disco --help
```

DisCo requires Node.js `>=22.19.0`.

Configure a model provider in interactive mode with `/login`, or set provider
environment variables such as `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`,
`GEMINI_API_KEY`, `OPENROUTER_API_KEY`, or `MISTRAL_API_KEY`.

## What DisCo Provides

- Repo-skill creation from source code, docs, examples, tests, package metadata,
  and optional installed-package inspection.
- Built-in repo-skill verification with usability cases, content self-refine,
  safe native example/test checks, static quality gates, coverage reports, and
  import-readiness checks.
- Paper2Skills Distiller for turning PDFs, arXiv ids, paper URLs, paper titles,
  or paper/repo pairs into modular Agent Skills.
- Skill refresh and extension workflows when upstream repositories change or a
  skill needs deeper coverage.
- Import/export workflows for moving selected or all repo skills into Codex,
  Claude Code, or another agent skill directory.
- A managed local skill library under `~/.disco/agent/skills/`.

## Quick Start

Create and verify a repo skill:

```bash
disco --source package -p "Create a repo skill for /path/to/repo."
```

Let DisCo decide the extraction scope and import the verified result into its
managed skill library:

```bash
disco --source package -p "Create a repo skill for /path/to/repo with auto decide and auto import."
```

Import selected or all skills into Codex:

```bash
disco -p "/skill:import-repo-skills-to-agent import vllm and sglang to ~/.codex"
```

Then ask Codex to use those skills for a concrete task, for example:

```text
Use the vLLM and SGLang repo skills to prepare a Qwen3-32B deployment plan with
launch commands, environment checks, and an OpenAI-compatible smoke test.
```

## Paper To Skill

Paper-to-skill is integrated into the same `disco` CLI. Use `--source paper`
when the input is a paper PDF, text file, direct PDF URL, arXiv URL/id, paper
title, or paper plus an optional implementation repository.

For repeatable runs, create a TOML config:

```toml
schema_version = 1

[defaults]
workspace_root = "/path/to/paper2skills-workspace"
original_repo_source = "unknown"
repo_discovery_mode = "ask"
recovery_target = "Choose the fastest faithful target and ask me before expensive recovery."
recovery_mode = "hard"
runtime_constraints = "Use isolated environments only; do not mutate shared envs."
iteration_budget = 10

[[runs]]
paper_slug = "example_paper"
paper_source = "/path/to/paper.pdf"
original_repo_source = "unknown"
```

Run Distiller through DisCo:

```bash
disco --source paper -p "Use Distiller to process the runs in this config. config_path: /path/to/distiller_run_config.toml"
```

The paper workflow resolves sources when permitted, modularizes the paper,
creates generated module skills, validates each generated skill, prepares a
bounded runtime handoff, runs a recovery experiment without reading the
original implementation repository, analyzes gaps, and refines within the
configured `iteration_budget`.

By default, recovery uses `hard` mode: reduced, proxy, toy, fallback, or
smaller-model runs are useful diagnostics, but they are not accepted as a
successful recovery unless the user explicitly chooses `soft` mode and the
proxy is executable, mechanism-checked, validator-approved, and logged.

Default outputs use this layout:

```text
<workspace_root>/<paper_slug>/
  distillation/
    run_manifest.json
    paper_profile.md
    module_plan.json
    modules/
    generated_skills_validation/
    environment/runtime_handoff.json
    recovery/
    analysis/
    reports/final/final_report.md
    reports/final/final_report.json
  skills/
    <generated-module-skill>/
```

## Repo Skill Verification

Repo-skill creation is not complete after drafting `SKILL.md`. DisCo hands the
draft to `verify-repo-skill` before the result is treated as import-ready.

Verification checks include:

- assertion-backed usability case generation;
- content-level self-refine against repository evidence;
- safe native example or test execution when available;
- static checks for links, provenance, routing metadata, frontmatter,
  self-containment, and local-path leaks;
- coverage, publication, review, and handoff artifacts.

Runtime skill content and review artifacts are kept separate. Publishable skill
content lives under `skills/<skill-id>/` or `skills/disco/<skill-id>/`; test
cases, review notes, reports, and other check-only artifacts live under
`skills/tests/<skill-id>/`.

## Common Commands

```bash
# Start interactive DisCo
disco

# Print-mode task
disco -p "Create a repo skill for /path/to/repo."

# Force package/repo workflow
disco --source package -p "Refresh the skill at /path/to/skill against /path/to/repo."

# Force paper workflow
disco --source paper -p "Use Distiller to process this paper. paper_source: https://arxiv.org/abs/0000.00000"

# Continue or resume sessions
disco --continue
disco --resume
```

## Local Development

From the repository source tree:

```bash
cd src
npm install --ignore-scripts
npm run build
npm --prefix packages/coding-agent run build:binary
```

The TypeScript build writes `packages/coding-agent/dist/`. The binary build
writes `packages/coding-agent/dist/disco` and copies bundled DisCo workflow
skills next to it.

## Related Packages

This package publishes the user-facing `disco` executable. The workspace also
publishes internal packages used by the CLI:

- `@auto-ml-skills/disco-ai`
- `@auto-ml-skills/disco-agent-core`
- `@auto-ml-skills/disco-tui`

Most users should install and run `@auto-ml-skills/disco` directly.

## Acknowledgement

DisCo builds on [pi](https://github.com/earendil-works/pi). We thank the pi
authors and contributors for their work.

## License

Apache-2.0
