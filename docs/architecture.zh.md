# 架构说明

Auto-ML Skills 把已发布技能库与创建、维护技能的工具链分开。

## 当前仓库快照

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

当前 checkout 同时包含已发布的 skill library 和 DisCo TypeScript 源码树。
runtime repo skills 位于 `repo-skills/`，公开的 optional-install workflow
mirror 位于 `meta-skills/`，完整的 bundled DisCo workflow source 位于
`src/packages/coding-agent/src/disco/skills/`。

## 源码布局

DisCo 源码树位于 `src/`：

```text
src/
  package.json
  packages/
    ai/
    tui/
    agent/
    coding-agent/
```

预期 package 职责：

| Package | 职责 |
| --- | --- |
| `packages/ai` | Provider integrations、model registries、streaming utilities、environment API-key handling，以及 image/model helpers。 |
| `packages/tui` | Terminal UI components 和 rendering infrastructure。 |
| `packages/agent` | Agent core、loop、harness、prompts、skill loading 和共享 agent abstractions。 |
| `packages/coding-agent` | 暴露 `disco` 的 CLI package，包含 interactive/print modes、project trust、session management、built-in tools、DisCo workflow skills 和 dynamic workflow orchestration。 |

workspace root 是 private。可发布 npm packages 位于 `src/packages/`。CLI
package 是 `@auto-ml-skills/disco`，暴露 `disco` 命令。

## Skill 生成 Pipeline

DisCo 有两类 source workflows：package/repo 和 paper。两者都集成在 `disco`
CLI 中。bundled workflow skill source 位于
`src/packages/coding-agent/src/disco/skills/`。

### Package/Repo Flow

从高层看，DisCo 的 repo-skill pipeline 是：

1. 分类 source type：package/repo 或 paper。
2. 分析 source structure 并确认 scope。
3. 准备最小 inspection environment。
4. 从 source、docs、examples、tests、metadata 和 live package inspection 收集证据。
5. 规划顶层 skill 和 sub-skill 结构。
6. 生成并集成自包含 runtime guidance。
7. 运行内置 verification workflow。
8. 把批准的 runtime skills 导入 managed library。
9. 在锁内重建 routing metadata 和 router scenario pages。

create flow 不把 verification 当作可选收尾步骤。`create-repo-skill` 会在
skill 准备导入或发布前，把集成后的 draft 交给 `verify-repo-skill`。

### Verification Gate

`verify-repo-skill` 负责 created、refreshed 或 extended repo skills 的最终质
量门禁。它把 check-only artifacts 写在 runtime skill directory 之外，通常位
于：

```text
<repository>/skills/tests/<skill-id>/
  test-cases/
  reports/
```

verification stage 覆盖：

- 生成 assertion-backed usability cases；
- 基于选定 source scope 和 generated skill tree 运行 content-level self-refine；
- 在安全且可用时检查代表性的原仓库 native examples/tests；
- 对 links、self-containment、provenance、routing metadata、本地路径泄漏和
  frontmatter shape 运行 static quality gates；
- 写出 final coverage、review、publication 和 handoff reports；
- 检查 import readiness，并在批准或 auto-authorized 时锁定导入 DisCo
  managed skill library。

runtime skill directories 不应包含 usability cases、eval notes、verification
reports、human-review notes、publication checklists 或 prompt samples。这些
内容属于 review/test artifact directory。

### Paper Flow

paper-to-skill flow 通过 `--source paper` 集成在 DisCo CLI 中。当前源码树包
含：

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

该流程会解析 paper source，可选地把 implementation repository 作为
pre-recovery evidence，随后对论文做 modularization，创建并验证 module-level
skills，准备有边界的 runtime evidence，在不读取原始 implementation repo 的
情况下运行 recovery experiment，分析差距，在配置的 `iteration_budget` 内必
要时 refine，并写出 attempt artifacts 和 final reports。重复运行时默认使
用基于 bundled `distiller-run-config-template.toml` 的 TOML run config。batch
configs 会在 workspace-level `paper2skills_runs/` 区域 normalize 成 JSON，
然后为每个选中的 paper/run 创建独立的 run root、source acquisition record、
generated-skills root 和 attempt directory。

run config normalization 会记录 `paper_slug`、`paper_source`、
`original_repo_source`、`repo_discovery_mode`、`recovery_target`、
`recovery_mode`、`runtime_constraints`、`iteration_budget` 和
`generated_skills_root` 等字段。新运行默认使用 `recovery_mode: hard` 和
`iteration_budget: 10`；`hard` mode 不会把 reduced、proxy、toy、
smaller-model 或 fallback recovery 接受为成功结果，而 `soft` mode 只有在明
确声明 proxy、具备 executable evidence 并通过 mechanism checks 时才可接受。

run root 也会在需要时记录 source acquisition，通常位于
`source/source_resolution.json`。每个 paper attempt 遵循类似下面的 artifact
contract：

```text
run_manifest.json
run_config.normalized.json   # 使用 config 时推荐存在
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

paper recovery 的 source boundary 比 modularization 更严格：optional
implementation repository 可以用于 module planning 和 module-skill creation，
但 recovery 只能使用 paper、module docs、generated skills、runtime handoff、
data 和 general package documentation。recovery result 必须由 executable
command logs 支撑，并且 attempt 需要证明 generated module skills 被调用、
导入或 cross-check，而不是被一次性的 handwritten recovery script 绕过。

### Bundled Workflow Skills

package/repo workflow skills 包括：

| Workflow Skill | 作用 |
| --- | --- |
| `prepare-repo-skill-env` | 在 extraction scope 已知后创建或验证 scoped Python inspection environment。 |
| `create-repo-skill` | 分析 source evidence，规划并生成 runtime skill，然后交给 verification。 |
| `verify-repo-skill` | 负责 assertion-backed usability cases、content self-refine、native checks、static gates、reports 和 import readiness。 |
| `refresh-repo-skill` | 根据 upstream source 变化更新已有 repo skill，然后验证。 |
| `extend-repo-skill` | 为已有 skill 增加更深覆盖，然后验证。 |
| `repo-skills-router` | 为导入后的 skill library 提供 progressive routing index。 |
| `import-repo-skills-to-agent` | 把 DisCo-managed skills 和 scoped router 导出到 Codex、Claude Code 或其他 agent target。 |

paper workflow skills 包括：

| Workflow Skill | 作用 |
| --- | --- |
| `create-paper-skills` | `disco --source paper` 的入口。 |
| `paper-skills-distiller` | 编排 source resolution、modularization、module-skill creation、recovery、analysis、refinement 和 final reports。 |
| `plan-paper-skill-modules` | 创建 paper profile、module plan 和 module docs。 |
| `create-paper-module-skill` | 把 module docs 转换成 generated module skills 和 validation checks。 |
| `prepare-paper-recovery-env` | 记录有边界的 package、model、GPU、dataset、command-log 和 runtime handoff evidence。 |
| `recover-paper-result` | 使用 generated skills 运行有边界的 recovery experiment，并保存 executable command 与 generated-skill invocation evidence。 |
| `analyze-paper-recovery` | 对比 recovery evidence、paper target、experiment gate、source boundary 和 mechanism checks，返回 accept/refine feedback。 |

## Runtime Skill 形态

runtime skill 使用 progressive disclosure：

```text
SKILL.md                         # agent 首先读取的文件
references/                      # 支撑证据和较长说明
sub-skills/<area>/SKILL.md       # 更深入的任务级指导
scripts/                         # 用于 checks/preflight 的小工具
```

`SKILL.md` 应该单独可用，并且只在任务需要更多细节时路由到更深页面。references
和 scripts 如果需要被使用，应在 skill 文本中链接出来。

generated repo skills 预期包含：

- `references/repo-provenance.md`，记录 source commit、package version、
  dirty state 和 evidence paths；
- `references/repo-routing-metadata.json`，用于 managed router placement；
- repo-skill root 和 sub-skill frontmatter 中的
  `disable-model-invocation: true`，让兼容的 agent 保持
  `repo-skills-router` 作为 model-visible entry point；
- 当未来使用依赖相关细节时，使用 bundled references 或 scripts，而不是链接
  到原始 checkout。

## Router

repo-skills router 是 skill library 的生成/维护索引：

```text
repo-skills/repo-skills-router/
  SKILL.md
  references/
    usage-scenarios.md
    maintenance.md
    scenarios/
```

它不是单个 skill 的替代品。它提供第一轮选择地图，并把 agent 指向合适的
scenario 页面和候选 skill。

## Managed Library

在 DisCo 中，用户级 managed library 位于：

```text
~/.disco/agent/skills/
```

managed library 是 import/export source，不一定是所有下游 agent 的 runtime
skill source。使用 `import-repo-skills-to-agent` 可以把 managed skills 和
router 导出到 `~/.agents`、`~/.codex` 或 `~/.claude` 等目标。

导出到 Codex 时，import workflow 还会在目标侧为非 router repo skills 写入
`agents/openai.yaml`，设置 `policy.allow_implicit_invocation: false`，因为
Codex 不使用 `disable-model-invocation` frontmatter 字段表达这个 policy。

批准或 auto-authorized 的导入会通过 verification workflow 的 import lock
串行化。同一个 locked transaction 会复制 runtime skill directory，验证
`references/repo-routing-metadata.json`，并重建 managed `repo-skills-router`
scenario map。import 阶段的 router update 应从 structured metadata 生成，而
不是手工自由编辑 Markdown。

## Source Of Truth

source-of-truth 规则：

- 本仓库 runtime repo skills 位于 `repo-skills/`。
- 轻量 external-agent workflow skills 位于 `meta-skills/`，包括 package/repo
  和 paper-to-skill workflows。
- Bundled DisCo workflow skills 位于
  `src/packages/coding-agent/src/disco/skills/`。
- 应在 `src/` 中编辑 bundled workflow skill source，然后按需 rebuild/resync
  `meta-skills/` mirrors。
- Verification 和 review artifacts 位于 runtime skill directories 之外，通常
  在被检查仓库的 `skills/tests/<skill-id>/` 下。
- 不要把生成的 `dist/` resources 当作 source of truth 手工编辑。
- 文档需要明确某个功能属于 runtime skill library、轻量 external-agent
  mirror，还是 DisCo CLI source。
