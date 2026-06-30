<h1 align="center">Auto-ML-Skills</h1>

<p align="center">
  <strong>把 ML 仓库和研究论文蒸馏成可复用的 Agent Skills</strong>
</p>

<p align="center">
  <a href="docs/imported-repo-skills.md"><img src="https://img.shields.io/badge/Skill_Library-170_repo_skills-0E9B9B?style=for-the-badge" alt="Skill Library: 170 repo skills"></a>
  <a href="https://www.npmjs.com/package/@auto-ml-skills/disco"><img src="https://img.shields.io/badge/CLI-disco%20v0.0.4-5865F2?style=for-the-badge&logo=npm&logoColor=white" alt="DisCo CLI v0.0.4"></a>
  <a href="meta-skills/README.md"><img src="https://img.shields.io/badge/Meta_Skills-Workflows-7A5AF8?style=for-the-badge" alt="Meta Skills"></a>
  <a href="CONTRIBUTING_CN.md"><img src="https://img.shields.io/badge/Contributing-Guide-0E9B9B?style=for-the-badge" alt="贡献指南"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-D22128?style=for-the-badge&logo=apache&logoColor=white" alt="License: Apache 2.0"></a>
</p>

<p align="center">
  <a href="README.md">English</a> | <b>简体中文</b>
</p>

**Auto-ML-Skills 让 coding agents 不再把 ML 仓库和论文当成匿名上下文。** 它
把软件仓库和研究论文中的 source-grounded operating knowledge 蒸馏成紧凑的
Agent Skills，并提供 TypeScript CLI DisCo，用于创建、验证、刷新、扩展、导
入和维护这些 skills。最终得到的是一个 runtime skill library：它能用更少的
API 猜测、更少的 token 浪费和更强的证据约束，指导 agent 使用真实 ML 软件
和 paper-derived methods。

在当前 checkout 中，公开 library 包含 **170 个 repository-specific runtime
skills**，以及一个用于 progressive selection 的 router skill。同一仓库还包
含 DisCo 源码、可复制的 meta skills、架构说明，以及把 research papers 转
换成 modular skills 的 Paper2Skills Distiller workflow。

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

- **2026-06-28**：Auto-ML-Skills 初次发布，包含公开的 runtime skill
  library、用于 repo-skill 和 paper-to-skill workflows 的 DisCo CLI，以及
  可把 DisCo workflows 带入 Codex、Claude Code 等 agent 的配套 meta
  skills。

## 💡 Why Auto-ML-Skills <a id="why-auto-ml-skills"></a>

现代 coding agents 已经能写出有用的机器学习代码，但在真实 ML 仓库中仍然经
常遇到的问题，不只是 generic package memory 能解决的。

- **Repo-specific APIs 很容易被误用。** ML libraries 经常把关键行为藏在
  configs、launchers、examples、registry systems、data formats 和特定版本
  约定中。
- **Package choice 本身就是任务。** LLM serving、RAG、生物/化学、视觉、
  MLOps、evaluation、RL 和 scientific Python stacks 经常能力重叠；agent 在
  选工具前需要 routing map。
- **新鲜源码证据很重要。** 安全的操作指导通常来自当前 checkout、package
  metadata、tests、examples 和 upstream commit，而不是过期的公开记忆总结。
- **论文需要 operational distillation。** 论文中的可复用知识往往分布在方
  法章节、公式、ablations、数据假设和可选 implementation repos 中；在做
  recovery work 前，agent 需要先把这些知识转成可测试的 module-level
  skills。
- **Trial and error 成本很高。** 缺少结构化 repo operating map 时，agent
  可能在找到仓库已经说明过的 workflow 前浪费 turns、下载、GPU jobs 和调试
  时间。

Auto-ML-Skills 通过把仓库知识变成 installable、verifiable、routable 的
skills 来解决这个问题。一个 skill 不是泛泛教程，而是紧凑的 operating map：
它告诉 agent 如何使用具体项目、什么时候加载更深的 references、以及哪些错
误需要避免。Paper-derived skills 把同一思路用于研究方法：把论文转成可在有
边界的 recovery runs 中验证、调用和 refine 的可复用模块。

## 🧰 What Is Included <a id="what-is-included"></a>

| Layer | Location | What it provides |
| --- | --- | --- |
| Runtime skill library | [`repo-skills/`](repo-skills/) | 170 个 repository-specific ML、LLM、agent、RAG、生物/化学、视觉、MLOps、RL、evaluation 和 scientific Python skills，并包含用于选择的 `repo-skills-router`。 |
| DisCo CLI source | [`src/`](src/) | `@auto-ml-skills/disco` TypeScript workspace，提供 `disco` 命令，以及 repo-skill 创建、验证、导入、刷新、扩展和 Paper2Skills distillation workflows。 |
| Workflow meta skills | [`meta-skills/`](meta-skills/) | 可复制到 Codex 或 Claude Code 的轻量 package/repo 与 paper-to-skill workflows，适合不直接使用完整 CLI 源码时使用。 |
| Documentation | [`docs/`](docs/) | 架构说明和公开 imported-skill catalog，记录 upstream repositories、package versions、commits 和 coverage summaries。 |

### 应该使用哪一部分？

- **使用 skill library**：当你希望 agent 直接使用现成的 ML repo knowledge。
  - 把 [`repo-skills/`](repo-skills/) 复制到 DisCo managed library：
    `~/.disco/agent/skills/`。
  - 然后把选定或全部 repo skills 导入 Codex、Claude Code 或其他目标 agent。
- **使用 DisCo CLI**：当你希望创建或维护 skills。
  - 创建、验证、刷新、扩展和导入 repo skills。
  - 使用 `disco --source paper` 把论文蒸馏成可复用的 module-level skills。
  - 为导入的 skills 维护 routing metadata 和 `repo-skills-router`。
- **使用 workflow meta skills**：当另一个 agent 需要在没有完整 CLI 源码时
  运行这些 workflows。
  - 把 [`meta-skills/`](meta-skills/) 复制到目标 agent 的 `skills/` 目录。
  - 这一路径适合在 Codex、Claude Code 或类似 agent 中运行可移植的
    repo-skill 和 paper-to-skill workflows。

## 🗂️ Library Coverage <a id="library-coverage"></a>

已包含 skill 的目录维护在
[`docs/imported-repo-skills.md`](docs/imported-repo-skills.md)。它记录每个
skill 的 upstream repository、update date、package version information、
source commit 和 intended workflow coverage。

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

最小安装只需要两步：

1. 安装 `disco` CLI。
2. 把 skill library 安装到 DisCo managed skill directory。

安装 workflow meta skills 是可选项。只有当你希望另一个 agent 在不使用完整
CLI 的情况下运行 DisCo 风格的创建、维护或 paper-to-skill workflows 时，才
需要安装这一部分。

### 安装 DisCo

从 npm 安装 DisCo CLI：

```bash
npm install -g @auto-ml-skills/disco
disco
```

DisCo 需要 Node.js `>=22.19.0`。pi 原生支持 35 个模型 providers，DisCo 继
承了这层 provider 支持。你需要在启动流程中通过 `/login` 配置至少一个
provider，或使用环境变量，例如 `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、
`GEMINI_API_KEY`、`OPENROUTER_API_KEY` 或 `MISTRAL_API_KEY`。

<details>
<summary>从源码构建用于本地开发</summary>

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
bash scripts/build-from-source-link.sh
```

该脚本会安装 workspace dependencies、构建 TypeScript packages，并把
`disco` 命令 link 到全局，便于本地使用。

</details>

### 安装 Runtime Skill Library

Clone 当前仓库，并把 runtime repo skills 复制到 DisCo managed skills 目录：

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
mkdir -p ~/.disco/agent/skills
cp -R repo-skills/* ~/.disco/agent/skills/
```

复制后重启 DisCo，让 managed skill index 重新加载。

### 安装 Workflow Meta Skills（Optional）

顶层 [`meta-skills/`](meta-skills/) 目录包含可复制到其他 agent 的 workflow
skills。它们用于让 Codex、Claude Code 或其他 agent 在不依赖完整 DisCo CLI
的情况下运行 DisCo 风格的 repo-skill 或 paper-to-skill workflow。

如果本地还没有 checkout，先 clone 这个仓库：

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
```

安装全部 workflow meta skills 到 Codex：

```bash
mkdir -p ~/.codex/skills
cp -R meta-skills/* ~/.codex/skills/
```

安装全部 workflow meta skills 到 Claude Code：

```bash
mkdir -p ~/.claude/skills
cp -R meta-skills/* ~/.claude/skills/
```

<details>
<summary>只把 paper-to-skill workflow 安装到 Codex</summary>

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

workflow 列表、Claude Code paper-only 安装命令、可直接复制给 agent 执行的
自动 clone 安装指令，以及默认 workflow artifact layout 见
[`meta-skills/README.md`](meta-skills/README.md)。

## 🚀 Quick Start <a id="quick-start"></a>

### 在 Codex 或 Claude Code 中使用 Repo Skills

把 skill library 安装到 DisCo managed skills 目录后，使用 DisCo 的 import
workflow，把选定或全部 repo skills 导出到目标 agent。例如，把 router 以及
`vllm`、`sglang` 两个模型服务 skills 导入 Claude Code：

```bash
disco -p "/skill:import-repo-skills-to-agent import vllm and sglang to ~/.claude"
```

导入 Codex 时使用：

```bash
disco -p "/skill:import-repo-skills-to-agent import vllm and sglang to ~/.codex"
```

重启目标 agent 后，发起一个具体部署任务：

```text
Use the repo skills to compare vLLM and SGLang for deploying Qwen3-32B on this
machine, then prepare a minimal OpenAI-compatible serving plan with launch
commands, environment checks, and a smoke-test request.
```

<details>
<summary>Hint：让 agent 更容易主动使用 router</summary>

导入 repo skills 之后，可以在项目的 `CLAUDE.md` 或 `AGENTS.md` 里告诉
agent：当用户需求可能受益于已安装的 repository skills 时，主动查阅
`repo-skills-router`。例如：

```text
When a task involves ML libraries, LLM serving, RAG, agents, bio/chem, vision,
MLOps, RL, evaluation, or scientific Python, proactively check
repo-skills-router before choosing a library-specific approach.
```

也可以在请求中直接调用 router：

```text
/repo-skills-router compare vLLM and SGLang for this deployment task
$repo-skills-router compare vLLM and SGLang for this deployment task
```

Claude Code 使用 `/repo-skills-router`，Codex 使用 `$repo-skills-router`。

</details>

### 为一个仓库创建 Skill

使用 DisCo 从源码证据创建并验证 repo-specific skill：

```bash
disco -p "Create a repo skill for /path/to/repo."
```

该 workflow 会分析仓库结构，在需要时准备或检查 Python inspection
environment，编写 runtime guidance，记录 provenance，然后把 draft 交给
`verify-repo-skill`。verification 会创建 assertion-backed usability cases，
运行 content-level self-refine，在安全可行时检查原仓库 native examples 或
tests，运行 static quality gates，并写出 coverage 和 review artifacts，之后
skill 才会被视为可用。

如果希望 agent 自动决定 extraction scope，并在验证通过后自动导入 DisCo
managed library，可以在请求中同时授权这两项决策：

```bash
disco -p "Create a repo skill for /path/to/repo with auto decide and auto import."
```

### 从论文创建 Skills

当输入来源是 research paper 而不是软件仓库时，使用集成在 DisCo CLI 中的
paper-to-skill workflow。对于可重复运行的任务，先复制并填写内置 run-config
template，再交给 DisCo：

```bash
cp meta-skills/create-paper-skills/assets/distiller-run-config-template.toml \
  /path/to/distiller_run_config.toml
disco --source paper -p "Use Distiller to process the runs in this config. config_path: /path/to/distiller_run_config.toml"
```

paper source 可以是本地 PDF/text 文件、直接 PDF URL、arXiv URL/id 或论文
标题。implementation repository 是可选项，可以是本地路径、Git URL、`none`
或 `unknown`。Distiller 会对论文做模块化，创建并验证 module-level skills，
准备有边界的 runtime evidence，在不读取原始 implementation repo 的情况下运
行当前可行的最强 recovery experiment，分析差距，在 `iteration_budget` 内
必要时 refine，并把 attempt artifacts 和 final reports 写到
`<attempt_dir>/reports/final/`。默认 `recovery_mode` 是 `hard`，因此 reduced、
proxy、toy 或 fallback runs 只会作为诊断记录；除非显式选择 `soft` mode，否
则不会被接受为成功 recovery。

### 扩展已有 Skill

当某个已有 skill 是正确的，但需要覆盖新的工作流领域时，直接向 DisCo 说明
要扩展的能力：

```bash
disco -p "Add streaming inference coverage to the existing skill at /path/to/repo/skills/example-skill using /path/to/repo as evidence."
```

### 上游代码更新后刷新 Skill

当上游仓库的 API、配置、示例、依赖或 runtime behavior 发生变化时，直接请
DisCo 对当前代码刷新 skill：

```bash
disco -p "Refresh the skill at /path/to/repo/skills/example-skill against the current /path/to/repo code."
```

refresh 应保留仍然正确的现有指导，同时基于当前 source baseline 更新过期内
容。

## 🛠️ DisCo Workflow Skills <a id="disco-workflow-skills"></a>

DisCo 内置了一组 workflow skills，用于编排 skill 创建、验证、维护、导入和
paper distillation。这些 workflows 已随 CLI 打包，同时也镜像在
[`meta-skills/`](meta-skills/) 中，便于按需安装到其他 agent。

- **Package 和 repository workflows**
  - `create-repo-skill`：基于 source code、docs、examples、tests、package
    metadata 和可选 installed-package inspection 创建 repo-specific skill。
  - `prepare-repo-skill-env`：在深入分析仓库前，准备或验证隔离的 Python
    inspection environment。
  - `verify-repo-skill`：用 usability cases、content self-refine、安全
    native checks、static gates、reports 和 import-readiness checks 验证生
    成或刷新后的 repo skills。
  - `refresh-repo-skill`：当 upstream APIs、configs、examples、
    dependencies 或 runtime behavior 变化时，更新已有 skill。
  - `extend-repo-skill`：为已有 skill 补充新的 workflow area 或更深覆盖。
  - `repo-skills-router`：根据 scenario 和 package coverage，在已安装的 repo
    skills 中路由用户请求。
  - `import-repo-skills-to-agent`：把选定或全部 managed repo skills 以及
    router 复制到 Codex、Claude Code 或其他 agent skill directory。
- **Paper-to-skill workflows**
  - `create-paper-skills`：`disco --source paper` 请求的入口。
  - `paper-skills-distiller`：编排 source resolution、paper modularization、
    module-skill creation、recovery、analysis、refinement 和 final reporting。
  - `plan-paper-skill-modules`：读取论文并生成 paper profile、module plan 和
    module docs。
  - `create-paper-module-skill`：把每个 module doc 转换成可复用的 generated
    Agent Skill，并附带 validation checks。
  - `prepare-paper-recovery-env`：准备有边界的 runtime evidence、package
    setup、model/data state 和 recovery handoff artifacts。
  - `recover-paper-result`：在不读取原始 implementation repo 的前提下，使用
    generated skills 运行有边界的 recovery experiment。
  - `analyze-paper-recovery`：把 recovery evidence 和 paper target 对比，并
    产出 accept、refine 或 blocker feedback。

## 🤝 Contributing <a id="contributing"></a>

我们欢迎三类主要贡献：

1. **贡献生成好的 repo skills。** 在 `repo-skills/<skill-id>/` 下添加可发布
   runtime skill，包含 provenance 和 routing metadata，并更新
   `repo-skills-router`，确保 agent 能发现它。
2. **扩展或刷新已有 repo skills。** 用基于源码证据的变更优化过期、不完整或
   不清晰的 skills。当 upstream baseline 或覆盖范围变化时，同步更新
   provenance 或 routing metadata。
3. **改进 DisCo CLI 源码。** 欢迎贡献 [`src/`](src/) 下的 TypeScript CLI，
   包括 package/repo 和 paper-to-skill workflows。请运行聚焦检查，并说明行
   为变化。repo-skill workflow 相关变更应保持 create/verify 分工、
   review/test artifact layout、import-readiness gates 和 locked router-update
   transaction。对集成的 Paper2Skills workflow 的改动应保持
   source-resolution、modularization、generated-skill validation、recovery、
   analysis 和 final-report contracts。

repo-skill PR 需要列出用于生成或修订 skill 的 model、provider、
reasoning/thinking level、source repository commit 和 verification steps。
涉及 paper-to-skill 行为的 DisCo CLI 变更还应在适用时说明 paper source、
run config、recovery mode、validation artifacts 和 final report path。完整
checklist 见 [CONTRIBUTING_CN.md](CONTRIBUTING_CN.md)。

## 📚 Documentation <a id="documentation"></a>

| 页面 | 说明 |
| --- | --- |
| [Imported Repo Skills Catalog](docs/imported-repo-skills.md) | 已包含 runtime repo skills 的公开目录，按工作流领域组织，并记录上游 baseline。 |
| [Architecture](docs/architecture.md) | 仓库分层、DisCo 源码布局、skill authoring pipeline、runtime skill 形态和 managed library model。 |
| [Workflow Meta Skills](meta-skills/README.md) | 可复制到外部 agent 的 package/repo 和 paper-to-skill workflow skills。 |
| [DisCo CLI README](src/packages/coding-agent/README.md) | DisCo CLI 的 repo-skill 创建、导入、验证和 paper-to-skill workflow 使用说明。 |
| [贡献指南](CONTRIBUTING_CN.md) | generated repo skills、router/catalog、文档、meta skills 和 CLI 源码贡献规范。 |

## 🙏 Acknowledgement <a id="acknowledgement"></a>

DisCo 的 CLI 和 agent runtime 构建在
[earendil-works/pi](https://github.com/earendil-works/pi) 的基础之上。Pi 是
一个开源 AI agent toolkit，提供 unified LLM API、agent loop、terminal UI
和 coding-agent CLI。

Auto-ML-Skills 也离不开 GitHub 开源社区。这个 skill library 能够存在，是因
为许多研究者和工程师开放了高质量的 ML、agent、data、生物/化学、视觉和基
础设施项目。

## 📄 License <a id="license"></a>

Auto-ML-Skills 使用 Apache License 2.0 发布。除非文件中另有明确说明，该
license 适用于 [`src/`](src/) 下的 DisCo CLI 源码，也适用于
[`repo-skills/`](repo-skills/) 下开源出来的 runtime repo skills。

完整 license 文本见 [LICENSE](LICENSE)。

## 📝 Citation <a id="citation"></a>

TBA
