# 贡献指南

Auto-ML Skills 把 skills 视为未来 agent 可能加载并执行的操作指导。好的贡献应
基于证据、容易审计，并清楚说明 skill 是如何生成的。

## 贡献路径

可以贡献：

- `repo-skills/<skill-id>/` 下新的 generated repo skills；
- 对已有 repo skills 的优化；
- router、catalog、provenance 和文档更新；
- `meta-skills/` 下的轻量 workflow skills；
- `src/` 下的 DisCo CLI 源码。

## 新增 Repo Skills

最重要的贡献类型是新的 runtime repo skill。

必需文件：

- `repo-skills/<skill-id>/SKILL.md`
- `repo-skills/<skill-id>/references/repo-provenance.md`
- `repo-skills/<skill-id>/references/repo-routing-metadata.json`
- 当上游仓库有多个主要工作流时，包含 sub-skills 和 references
- 当能提升使用安全性时，包含小型 validation 或 preflight scripts

保持 runtime skill 内容与 review artifacts 分离。可发布内容应位于：

```text
repo-skills/<skill-id>/
```

test cases、review notes 和 generation reports 不应混入 runtime skill 目录，
除非它们明确就是运行时指导的一部分。

## Router 与 Catalog 一致性

当添加、删除、重命名、导入 repo skill，或 repo skill 覆盖范围发生实质变化
时，更新 router：

```text
repo-skills/repo-skills-router/SKILL.md
repo-skills/repo-skills-router/references/usage-scenarios.md
repo-skills/repo-skills-router/references/scenarios/*.md
```

router entry 应帮助 agent 在 skills 之间做选择，而不是复制完整 skill 指令。

当 imported skill library 变化时，更新公开 catalog：

```text
docs/imported-repo-skills.md
```

catalog 应与 `repo-routing-metadata.json` 和 `repo-provenance.md` 保持一致。

## 优化已有 Repo Skills

当某个 skill 过期、不清晰、不完整，或 agent 使用起来成本过高时，欢迎优化。

规则：

- 变更应基于源码证据、上游文档、示例或已检查的 package 行为。
- 保留仍然正确的现有指导。
- 当 source commit、package version 或 evidence set 变化时，更新 provenance。
- 当覆盖范围或选择指导变化时，更新 routing metadata。
- scripts 应确定且安全。除非有明确 gate，否则避免下载、训练、启动 server
  或破坏性文件操作。

聚焦检查：

```bash
find repo-skills/<skill-id> -type f -name '*.py' -print0 | xargs -0 -r python -m py_compile
find repo-skills/<skill-id> -type f | sort
```

## Pull Request 要求

任何新增或修改 generated repo skills 的 PR，都应包含：

- 上游 repository URL 和 source commit 或 tag；
- 用于生产 skill 的 model 和 provider；
- 使用的 reasoning 或 thinking level，例如 `low`、`medium`、`high`，或对应
  provider 的等价设置；
- skill 是由 DisCo、复制到其他 agent 的 meta skills，还是人工编辑产生；
- 已运行的 verification commands 或 review steps；
- 已知缺口、跳过的检查、不可用 credentials 或环境限制；
- 当 routing 变化时，确认已经更新 `repo-skills-router`。

如果使用了多个 model 或多轮 pass，请列出每个 model 的角色，例如 generation、
review、refinement 或 verification。

## 文档变更

文档是双语的。修改英文页面时，同步更新对应中文页面；反过来也一样。

规则：

- 使用相对路径，并以 Markdown 文件所在位置为基准。
- 优先写具体命令和路径，少写泛泛描述。
- README 保持简洁，把详细流程放到 `docs/`。
- 避免在每个文档页面重复写语言切换链接。README 文件和 MkDocs 语言切换器是
  主要语言入口。
- 如果 catalog 变化，保持完整 catalog 和 localized index 对齐。

可用检查：

```bash
python - <<'PY'
from pathlib import Path
for p in sorted(Path('docs').glob('*.md')):
    text = p.read_text()
    if '\t' in text:
        print(f'tab: {p}')
PY
```

预览可选 MkDocs 文档站：

```bash
python -m pip install mkdocs-material mkdocs-static-i18n
mkdocs serve
mkdocs build --strict
```

## Meta Skill 变更

顶层 `meta-skills/` 是给 external agents 使用的轻量 mirror。它应在没有
DisCo-only extensions 的情况下也能读懂。

更新 meta skills 时：

- 明确说明期望 inputs 和 outputs。
- 在昂贵或破坏性步骤前请求用户确认，除非用户授权 agent 自行决定。
- 保持环境变更隔离。
- 保持 generated runtime skill 内容与 tests/reports 分离。
- 当名称或 workflow 边界变化时，更新 [`meta-skills/`](meta-skills/) mirror。

## DisCo Source 变更

DisCo CLI 源码位于 `src/`。

常用检查：

```bash
cd src
npm install --ignore-scripts
npm run build
npm run check
```

发布准备时，先 dry-run package contents：

```bash
npm pack --workspace packages/ai --dry-run
npm pack --workspace packages/tui --dry-run
npm pack --workspace packages/agent --dry-run
npm pack --workspace packages/coding-agent --dry-run
```

不要把生成的 `dist/` 文件或 standalone binary runtime assets 当作 source
changes 手工编辑。

## 最终 Checklist

交付变更前：

- README 和 docs 链接指向存在的文件。
- 适用时，英文和中文文档都已更新。
- runtime skill 变更包含 provenance 和 source evidence。
- router 和 catalog 与 skill 变更一致。
- PR text 列出 model、provider、reasoning 或 thinking level，以及验证步骤。
- 变更过的 scripts 已做 syntax check 或其他验证。
- 最终说明写清楚验证了什么、没有验证什么。
