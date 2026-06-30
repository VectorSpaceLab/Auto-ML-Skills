<h1 align="center">Auto-ML-Skills</h1>

<p align="center">
  <strong>Distilling ML repositories and research papers into reusable Agent Skills</strong>
</p>

<p align="center">
  <a href="docs/imported-repo-skills.md"><img src="https://img.shields.io/badge/Skill_Library-170_repo_skills-0E9B9B?style=for-the-badge" alt="Skill Library: 170 repo skills"></a>
  <a href="https://www.npmjs.com/package/@auto-ml-skills/disco"><img src="https://img.shields.io/badge/CLI-disco%20v0.0.4-5865F2?style=for-the-badge&logo=npm&logoColor=white" alt="DisCo CLI v0.0.4"></a>
  <a href="meta-skills/README.md"><img src="https://img.shields.io/badge/Meta_Skills-Workflows-7A5AF8?style=for-the-badge" alt="Meta Skills"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/Contributing-Guide-0E9B9B?style=for-the-badge" alt="Contributing Guide"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-D22128?style=for-the-badge&logo=apache&logoColor=white" alt="License: Apache 2.0"></a>
</p>

<p align="center">
  <b>English</b> | <a href="README.zh-CN.md">简体中文</a>
</p>

**Auto-ML-Skills helps coding agents stop treating ML repositories and papers as
anonymous context.** It distills source-grounded operating knowledge from
software repositories and research papers into compact Agent Skills, then gives
DisCo, a TypeScript CLI, the workflows needed to create, verify, refresh,
extend, import, and maintain those skills. The result is a runtime skill
library that can guide agents through real ML software and paper-derived
methods with less API guessing, fewer wasted tokens, and stronger evidence
discipline.

At the current checkout, the public library contains **170 repository-specific
runtime skills** plus a router skill for progressive selection. The same repo
also includes DisCo source code, copyable meta skills, architecture notes, and
the Paper2Skills Distiller workflow for turning research papers into modular
skills.

## 🧭 Table Of Contents <a id="table-of-contents"></a>

- [📣 News](#news)
- [💡 Why Auto-ML-Skills](#why-auto-ml-skills)
- [🧰 What Is Included](#what-is-included)
- [🗂️ Library Coverage](#library-coverage)
- [⚙️ Installation](#installation)
- [🚀 Quick Start](#quick-start)
- [🛠️ DisCo Workflow Skills](#disco-workflow-skills)
- [🤝 Contributing](#contributing)
- [📚 Documentation](#documentation)
- [🙏 Acknowledgement](#acknowledgement)
- [📄 License](#license)
- [📝 Citation](#citation)

## 📣 News <a id="news"></a>

- **2026-06-28**: Initial release of Auto-ML-Skills, including the public
  runtime skill library, the DisCo CLI for repo-skill and paper-to-skill
  workflows, and the companion meta skills for bringing DisCo workflows into
  agents such as Codex and Claude Code.

## 💡 Why Auto-ML-Skills <a id="why-auto-ml-skills"></a>

Modern coding agents can already write useful machine-learning code, but they
often struggle when the correct action depends on a living repository rather
than a generic package memory.

- **Repo-specific APIs are easy to misuse.** ML libraries hide important
  behavior in configs, launchers, examples, registry systems, data formats, and
  version-specific conventions.
- **Package choice is itself a task.** LLM serving, RAG, bio/chem, vision,
  MLOps, evaluation, RL, and scientific Python stacks overlap heavily; agents
  need a routing map before they can pick the right tool.
- **Fresh source evidence matters.** The safest instruction often comes from
  today's checkout, package metadata, tests, examples, and upstream commit
  rather than a stale public-memory summary.
- **Papers need operational distillation.** A paper's reusable knowledge is
  often split across method sections, equations, ablations, data assumptions,
  and optional implementation repos; agents need that knowledge converted into
  testable module-level skills before recovery work is credible.
- **Trial and error is expensive.** Unstructured exploration can burn turns,
  downloads, GPU jobs, and debugging time before the agent reaches the workflow
  the repository already documents.

Auto-ML-Skills addresses this by making repository knowledge installable,
verifiable, and routable. A skill is not a broad tutorial; it is a compact
operating map that tells an agent how to work with a specific project, when to
load deeper references, and which mistakes to avoid. Paper-derived skills apply
the same idea to research methods: they turn a paper into reusable modules that
can be validated, invoked, and refined during bounded recovery runs.

## 🧰 What Is Included <a id="what-is-included"></a>

| Layer | Location | What it provides |
| --- | --- | --- |
| Runtime skill library | [`repo-skills/`](repo-skills/) | 170 repository-specific ML, LLM, agent, RAG, bio/chem, vision, MLOps, RL, evaluation, and scientific Python skills, plus `repo-skills-router` for selection. |
| DisCo CLI source | [`src/`](src/) | The `@auto-ml-skills/disco` TypeScript workspace, exposing the `disco` command and bundled workflows for repo-skill creation, verification, import, refresh, extension, and Paper2Skills distillation. |
| Workflow meta skills | [`meta-skills/`](meta-skills/) | Lightweight package/repo and paper-to-skill workflows that can be copied into Codex or Claude Code when you do not need the full CLI source. |
| Documentation | [`docs/`](docs/) | Architecture notes and the public imported-skill catalog with upstream repositories, package versions, commits, and coverage summaries. |

### Which Part Should You Use?

- **Use the skill library** when you want an agent to use existing ML repo
  knowledge.
  - Copy [`repo-skills/`](repo-skills/) into DisCo's managed library at
    `~/.disco/agent/skills/`.
  - Then import selected or all repo skills into Codex, Claude Code, or another
    target agent.
- **Use the DisCo CLI** when you want to create or maintain skills.
  - Create, verify, refresh, extend, and import repo skills.
  - Distill papers into reusable module-level skills with `disco --source
    paper`.
  - Keep routing metadata and `repo-skills-router` updated for imported skills.
- **Use workflow meta skills** when another agent should run the workflows
  without the full CLI source.
  - Copy [`meta-skills/`](meta-skills/) into the target agent's `skills/`
    directory.
  - Use this path for portable repo-skill and paper-to-skill workflows in
    Codex, Claude Code, or similar agents.

## 🗂️ Library Coverage <a id="library-coverage"></a>

The included skill catalog is maintained in
[`docs/imported-repo-skills.md`](docs/imported-repo-skills.md). It records each
skill's upstream repository, update date, package version information, source
commit, and intended workflow coverage.

| Area | Examples from the included library |
| --- | --- |
| ML infrastructure and training | Dask, DGL, PyTorch Lightning, Optuna, PyTorch Geometric |
| Data preparation and evaluation | MTEB, LM Evaluation Harness, Datasets, Evaluate, OpenCompass, Pillow, TorchVision |
| LLM training, fine-tuning, and serving | Axolotl, DeepSpeed, Transformers, PEFT, NeMo, vLLM, SGLang, Unsloth, TRL |
| Agents and agentic workflows | Browser Use, CAMEL, CrewAI, OpenHands, MetaGPT, LangFlow, LangChain, LangGraph, AutoGen, OpenAI Agents SDK |
| RAG and document AI | Haystack, Docling, LightRAG, RAGFlow, Khoj, Kotaemon, GraphRAG, LlamaIndex, Qdrant Client, Unstructured |
| RL and distributed AI systems | Gymnasium, Ray, Acme, AgileRL, Stable-Baselines3, CleanRL, PettingZoo, Tianshou |
| Bio, chemistry, vision, and scientific Python | AlphaFold, AlphaFold3, OmegaFold, OpenFE, DeepMD-kit, Scanpy, MONAI, MMCV, MMDetection, ComfyUI |
| MLOps and orchestration | Airflow, BentoML, Dagster, Feast, Great Expectations, MLflow, ZenML, ClearML, Kedro, Snakemake, W&B |

## ⚙️ Installation <a id="installation"></a>

The minimal setup has two steps:

1. Install the `disco` CLI.
2. Install the skill library into DisCo's managed skill directory.

Installing workflow meta skills is optional. Use that path only when you want
another agent to run DisCo-style creation or paper-to-skill workflows without
using the full CLI.

### Install DisCo

Install the DisCo CLI from npm:

```bash
npm install -g @auto-ml-skills/disco
disco
```

DisCo requires Node.js `>=22.19.0`. pi natively supports 35 model providers,
and DisCo inherits that provider layer. Configure at least one provider in the
startup flow with `/login`, or use environment variables such as
`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`,
or `MISTRAL_API_KEY`.

<details>
<summary>Build from source for local development</summary>

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
bash scripts/build-from-source-link.sh
```

The script installs workspace dependencies, builds the TypeScript packages, and
links the `disco` command globally for local use.

</details>

### Install The Runtime Skill Library

Clone this repository and copy the runtime repo skills into DisCo's managed
skills directory:

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
mkdir -p ~/.disco/agent/skills
cp -R repo-skills/* ~/.disco/agent/skills/
```

Restart DisCo after copying so the managed skill index is reloaded.

### Install Workflow Meta Skills (Optional)

The top-level [`meta-skills/`](meta-skills/) directory contains workflow skills
for agents that should run DisCo-style repo-skill or paper-to-skill workflows
without relying on the full DisCo CLI.

If you do not already have a local checkout, clone this repository first:

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
```

Install all workflow meta skills into Codex:

```bash
mkdir -p ~/.codex/skills
cp -R meta-skills/* ~/.codex/skills/
```

Install all workflow meta skills into Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R meta-skills/* ~/.claude/skills/
```

<details>
<summary>Install only the paper-to-skill workflow into Codex</summary>

```bash
mkdir -p ~/.codex/skills
cp -R \
  meta-skills/create-paper-skills \
  meta-skills/paper-skills-distiller \
  meta-skills/plan-paper-skill-modules \
  meta-skills/create-paper-module-skill \
  meta-skills/prepare-paper-recovery-env \
  meta-skills/recover-paper-result \
  meta-skills/analyze-paper-recovery \
  ~/.codex/skills/
```

</details>

See [`meta-skills/README.md`](meta-skills/README.md) for the workflow list,
Claude Code paper-only install command, copy-and-run agent installation prompts
that clone the repository automatically, and default workflow artifact layout.

## 🚀 Quick Start <a id="quick-start"></a>

### Use Repo Skills In Codex Or Claude Code

After the skill library is installed in DisCo's managed skills directory, use
DisCo's import workflow to export selected or all repo skills into your target
agent.
For example, import the router plus the `vllm` and `sglang` skills into Claude
Code:

```bash
disco -p "/skill:import-repo-skills-to-agent import vllm and sglang to ~/.claude"
```

To import the same skills into Codex:

```bash
disco -p "/skill:import-repo-skills-to-agent import vllm and sglang to ~/.codex"
```

Restart the agent, then ask for a concrete deployment task:

```text
Use the repo skills to compare vLLM and SGLang for deploying Qwen3-32B on this
machine, then prepare a minimal OpenAI-compatible serving plan with launch
commands, environment checks, and a smoke-test request.
```

<details>
<summary>Hint: make the router easy for your agent to use</summary>

After importing repo skills, tell your agent to consult `repo-skills-router`
when a user request could benefit from installed repository skills. A project
`CLAUDE.md` or `AGENTS.md` can include a short instruction such as:

```text
When a task involves ML libraries, LLM serving, RAG, agents, bio/chem, vision,
MLOps, RL, evaluation, or scientific Python, proactively check
repo-skills-router before choosing a library-specific approach.
```

You can also invoke the router directly in a request:

```text
/repo-skills-router compare vLLM and SGLang for this deployment task
$repo-skills-router compare vLLM and SGLang for this deployment task
```

Use `/repo-skills-router` in Claude Code and `$repo-skills-router` in Codex.

</details>

### Create A Skill For A Repository

Use DisCo to create and verify a repo-specific skill from source evidence:

```bash
disco -p "Create a repo skill for /path/to/repo."
```

The workflow analyzes repository structure, prepares or checks a Python
inspection environment when needed, writes runtime guidance, records
provenance, and then hands the draft to `verify-repo-skill`. Verification
creates assertion-backed usability cases, runs content-level self-refine,
checks safe native examples or tests when available, runs static quality gates,
and writes coverage and review artifacts before the skill is treated as ready.

To let the agent choose the extraction scope and import the verified skill into
DisCo's managed library without another confirmation round, delegate both
decisions in the request:

```bash
disco -p "Create a repo skill for /path/to/repo with auto decide and auto import."
```

### Create Skills From A Paper

Use the paper-to-skill workflow integrated in the DisCo CLI when the source is
a research paper rather than a software repository. For repeatable runs, copy
and fill the bundled run-config template, then pass it to DisCo:

```bash
cp meta-skills/create-paper-skills/assets/distiller-run-config-template.toml \
  /path/to/distiller_run_config.toml
disco --source paper -p "Use Distiller to process the runs in this config. config_path: /path/to/distiller_run_config.toml"
```

The paper source can be a local PDF or text file, direct PDF URL, arXiv URL or
id, or paper title. An implementation repository is optional and can be a local
path, Git URL, `none`, or `unknown`. Distiller modularizes the paper, creates
and validates module-level skills, prepares bounded runtime evidence, runs the
strongest feasible recovery experiment without reading the original
implementation repo, analyzes gaps, refines within `iteration_budget` when
needed, and writes attempt artifacts plus final reports under
`<attempt_dir>/reports/final/`. The default `recovery_mode` is `hard`, so
reduced, proxy, toy, or fallback runs are recorded as diagnostics rather than
accepted as successful recovery unless you explicitly choose `soft` mode.

### Extend An Existing Skill

Ask DisCo to extend an existing skill when it is correct but needs deeper
coverage for a new workflow area:

```bash
disco -p "Add streaming inference coverage to the existing skill at /path/to/repo/skills/example-skill using /path/to/repo as evidence."
```

### Refresh A Skill After Upstream Changes

Ask DisCo to refresh a skill when the upstream repository changes APIs,
configs, examples, dependencies, or runtime behavior:

```bash
disco -p "Refresh the skill at /path/to/repo/skills/example-skill against the current /path/to/repo code."
```

Refresh should preserve correct existing guidance while updating stale
instructions against the current source baseline.

## 🛠️ DisCo Workflow Skills <a id="disco-workflow-skills"></a>

DisCo bundles workflow skills that orchestrate skill creation, verification,
maintenance, import, and paper distillation. They are available inside the CLI
and mirrored under [`meta-skills/`](meta-skills/) for optional installation into
other agents.

- **Package and repository workflows**
  - `create-repo-skill`: create a repo-specific skill from source code, docs,
    examples, tests, package metadata, and optional installed-package
    inspection.
  - `prepare-repo-skill-env`: prepare or verify an isolated Python inspection
    environment before deeper repository analysis.
  - `verify-repo-skill`: verify generated or refreshed repo skills with
    usability cases, content self-refine, safe native checks, static gates,
    reports, and import-readiness checks.
  - `refresh-repo-skill`: update an existing skill when upstream APIs, configs,
    examples, dependencies, or runtime behavior change.
  - `extend-repo-skill`: add deeper coverage to an existing skill for a new
    workflow area.
  - `repo-skills-router`: route user requests across installed repo skills by
    scenario and package coverage.
  - `import-repo-skills-to-agent`: copy selected or all managed repo skills,
    plus the router, into Codex, Claude Code, or another agent skill directory.
- **Paper-to-skill workflows**
  - `create-paper-skills`: entry point for `disco --source paper` requests.
  - `paper-skills-distiller`: orchestrate source resolution, paper
    modularization, module-skill creation, recovery, analysis, refinement, and
    final reporting.
  - `plan-paper-skill-modules`: read the paper and produce the paper profile,
    module plan, and module docs.
  - `create-paper-module-skill`: convert each module doc into a reusable
    generated Agent Skill with validation checks.
  - `prepare-paper-recovery-env`: prepare bounded runtime evidence, package
    setup, model/data state, and recovery handoff artifacts.
  - `recover-paper-result`: run a bounded recovery experiment using generated
    skills without reading the original implementation repo.
  - `analyze-paper-recovery`: compare recovery evidence against the paper
    target and produce accept, refine, or blocker feedback.

## 🤝 Contributing <a id="contributing"></a>

We welcome contributions in three main areas:

1. **Contribute generated repo skills.** Add a publishable runtime skill under
   `repo-skills/<skill-id>/`, include provenance and routing metadata, and
   update `repo-skills-router` so agents can discover it.
2. **Extend or refresh existing repo skills.** Improve stale, incomplete, or
   unclear skills with source-grounded changes. Update provenance or routing
   metadata when the upstream baseline or coverage changes.
3. **Improve the DisCo CLI source.** Changes to the TypeScript CLI under
   `src/` are welcome, including package/repo and paper-to-skill workflows.
   Run focused checks and document behavior changes. Repo-skill workflow
   changes should preserve the create/verify split, review/test artifact
   layout, import-readiness gates, and locked router-update transaction.
   Updates to the integrated Paper2Skills workflow should preserve its
   source-resolution, modularization, generated-skill validation, recovery,
   analysis, and final-report contracts.

For repo-skill PRs, list the model, provider, reasoning or thinking level,
source repository commit, and verification steps used to produce or revise the
skill. For DisCo CLI changes that touch paper-to-skill behavior, include the
paper source, run config, recovery mode, validation artifacts, and final report
path when applicable. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full
checklist.

## 📚 Documentation <a id="documentation"></a>

| Page | Description |
| --- | --- |
| [Imported Repo Skills Catalog](docs/imported-repo-skills.md) | Public catalog of included runtime repo skills, grouped by workflow area with upstream baselines. |
| [Architecture](docs/architecture.md) | Repository layers, DisCo source layout, skill authoring pipeline, runtime skill shape, and managed library model. |
| [Workflow Meta Skills](meta-skills/README.md) | Copyable package/repo and paper-to-skill workflow skills for external agents. |
| [DisCo CLI README](src/packages/coding-agent/README.md) | DisCo CLI usage for repo-skill creation, import, verification, and paper-to-skill workflows. |
| [Contributing](CONTRIBUTING.md) | Contribution rules for generated repo skills, router/catalog updates, documentation, meta skills, and CLI source. |

## 🙏 Acknowledgement <a id="acknowledgement"></a>

DisCo's CLI and agent runtime are built on the foundation of
[earendil-works/pi](https://github.com/earendil-works/pi), an open-source AI
agent toolkit with a unified LLM API, agent loop, terminal UI, and coding-agent
CLI.

Auto-ML-Skills is also made possible by the GitHub open-source community. The
repo skills in this library exist because many researchers and engineers have
released high-quality ML, agent, data, bio/chem, vision, and infrastructure
projects for the community to build on.

## 📄 License <a id="license"></a>

Auto-ML-Skills is released under the Apache License 2.0. Unless a file
explicitly states otherwise, the license applies to both the DisCo CLI source
code in [`src/`](src/) and the open-sourced runtime repo skills under
[`repo-skills/`](repo-skills/).

See [LICENSE](LICENSE) for the full license text.

## 📝 Citation <a id="citation"></a>

TBA
