# Auto-ML-Skills

<p align="center">
  <a href="https://github.com/VectorSpaceLab/Auto-ML-Skills/discussions">Discussions</a> |
  <a href="docs/imported-repo-skills.md">Skill Library</a> |
  <a href="LICENSE">License</a>
</p>

<p align="center">
  <a href="README.md">English</a> | <b>简体中文</b>
</p>

## 🧭 Table of Contents <a id="table-of-contents"></a>

- [Introduction](#introduction)
- [News](#news)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [Acknowledgement](#acknowledgement)
- [License](#license)
- [Citation](#citation)

## 💡 Introduction <a id="introduction"></a>

现代 coding agents 已经能写出有用的机器学习代码，但在真实 ML 仓库中仍然经
常遇到几类问题：

- **Package selection：** 当多个 ML、LLM、RAG、生物/化学、视觉或 MLOps
  项目能力重叠时，agent 不一定知道哪个 library 最适合当前任务。
- **Repo-specific usage：** agent 经常误用本地 API、配置文件、启动命令或数
  据格式，随后花费额外 turns 和 tokens 调试本可避免的错误。
- **Current-code awareness：** 当正确做法依赖当前源码树、examples、tests
  和 package metadata 时，agent 需要基于仓库证据的操作指导。
- **Costly trial and error：** 如果缺少可靠的 repo operating map，agent 在
  探索陌生仓库时可能浪费时间、tokens、下载成本或 GPU 运行成本。

Auto-ML-Skills 是一个面向 automated machine learning 的 skill library。它
为 agent 提供 repo-specific 和 paper-derived operating knowledge，让 agent
能更准确、更少浪费 tokens 地处理 ML software。

本仓库提供：

- **Runtime skill library：** [`repo-skills/`](repo-skills/) 包含覆盖常见
  ML、LLM、agent、RAG、生物/化学、视觉、MLOps 和科学计算 Python 项目的
  skills。
- **DisCo CLI：** [`src/`](src/) 包含基于
  [earendil-works/pi](https://github.com/earendil-works/pi) 构建的 CLI，用
  于创建、验证、刷新、扩展、导入和维护 repo skills。repo-skill 创建流程内
  置 assertion-backed usability cases、content-level self-refine、安全 native
  examples/tests 检查、static verification、coverage reports 和 import-readiness
  gates。DisCo CLI 也通过集成的 Paper2Skills Distiller workflow 把 AI
  research papers 转换成 modular Agent Skills。
- **Meta skills：** [`meta-skills/`](meta-skills/) 包含可复制到其他 agent
  的轻量 repo-skill 和 paper-to-skill workflows，适合在不运行完整 DisCo CLI
  的情况下使用。

使用 Auto-ML-Skills，你可以：

1. **Use ready-made skills：** 把 DisCo 生成的高质量 ML repo skills 安装到
   自己的 agent 中，提高 agent 完成 ML tasks 的效率。
2. **Build new skills：** 使用 DisCo 为自己的仓库创建 repo skills，并可选
   择通过内置 verification workflow 验证后贡献回这个 skill library。
3. **Distill research papers：** 使用 `--source paper` 让 DisCo 把 PDF、
   arXiv id/URL、paper title 或 paper/repo pair 转换成可复用的 module-level
   skills。
4. **Bring workflows into agents：** 把本仓库提供的 meta skills 导入 Codex
   或 Claude Code 等 agent，使它们具备 DisCo 风格的 repo-skill 和
   paper-to-skill workflows。

## 📣 News <a id="news"></a>

- **2026-06-28**：Auto-ML-Skills 初次发布，包含公开的 runtime skill
  library、用于 repo-skill 和 paper-to-skill workflows 的 DisCo CLI，以及
  可把 DisCo workflows 带入 Codex、Claude Code 等 agent 的配套 meta
  skills。

## ⚙️ Installation <a id="installation"></a>

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

也可以从源码构建：

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
bash scripts/build-from-source-link.sh
```

该脚本会安装 workspace dependencies、构建 TypeScript packages，并把
`disco` 命令 link 到全局，便于本地使用。

### 安装 Skill Library

Clone 当前仓库，并把 runtime repo skills 复制到 DisCo managed skills 目录：

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
mkdir -p ~/.disco/agent/skills
cp -R repo-skills/* ~/.disco/agent/skills/
```

复制后重启 DisCo，让 managed skill index 重新加载。

### 安装 Workflow Meta Skills

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

如果只需要把 paper workflow 安装到 Codex，复制这七个目录：

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

workflow 列表、Claude Code paper-only 安装命令、可直接复制给 agent 执行的
自动 clone 安装指令，以及默认 workflow artifact layout 见
[`meta-skills/README.md`](meta-skills/README.md)。

## 🚀 Quick Start <a id="quick-start"></a>

### 在 Codex 或 Claude Code 中使用 Repo Skills

把 skill library 安装到 DisCo managed skills 目录后，使用 DisCo 的 import
workflow，把选定的 repo skills 导出到目标 agent。例如，把 router 以及
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
