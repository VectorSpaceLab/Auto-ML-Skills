# Auto-ML-Skills Meta Skills

`meta-skills/` contains workflow skills that can be copied into another coding
agent when you want DisCo-style skill creation without running the full DisCo
CLI. These are orchestration skills, not runtime repo skills.

## Package / Repo Workflows

Use these for software repositories and Python packages:

- `create-repo-skill`: create a new repo-specific skill from source evidence.
- `prepare-repo-skill-env`: prepare or verify an isolated inspection
  environment for repo analysis.
- `verify-repo-skill`: verify generated repo skills with usability cases,
  self-refine, native checks when safe, and import-readiness gates.
- `refresh-repo-skill`: update an existing skill after upstream changes.
- `extend-repo-skill`: add coverage to an existing skill.
- `import-repo-skills-to-agent`: copy selected repo skills into Codex, Claude
  Code, or another agent skill directory.
- `repo-skills-router`: route user requests across installed repo skills.

Package workflow defaults:

- If the user does not provide a repository path, use the current working
  directory.
- Default decision policy is `extractionScope: ask` and
  `importAfterVerification: ask`; `auto decide` / `agent decide` delegates
  scope confirmation, and `auto import` / `default import` delegates final
  import after successful verification.
- Default generated skill output is under `<repository-path>/skills/`; if that
  directory already exists, use `<repository-path>/skills/disco/` as the active
  DisCo-generated skills root.
- Default review/test artifact directory is
  `<repository-path>/skills/tests/<chosen-skill-id>/`, with concrete cases in
  `test-cases/` and reports in `reports/`.
- If no Python inspection environment is supplied, analyze repository structure
  first, confirm or agent-confirm the extraction scope, then prepare a private
  inspection environment.
- Default private inspection environment prefix is
  `$DISCO_CODING_AGENT_DIR/envs/<chosen-skill-id>-inspection` when set,
  otherwise `~/.disco/agent/envs/<chosen-skill-id>-inspection`.
- Environment setup uses `prepare-repo-skill-env`, prefers conda when
  available, falls back to venv, defaults to Python 3.11 unless repo metadata
  requires another version, and installs the smallest dependency set needed for
  the confirmed extraction scope.
- Verification is required before a generated repo skill is treated as ready;
  successful auto-import writes to `~/.disco/agent/skills/` and updates the
  live `repo-skills-router` through the locked import protocol.

## Paper Workflows

Use these for AI research papers:

- `create-paper-skills`: entry point for paper sources and `source=paper`
  requests.
- `paper-skills-distiller`: top-level Paper2Skills Distiller controller.
- `plan-paper-skill-modules`: read a paper and produce a paper profile, module
  plan, and module docs.
- `create-paper-module-skill`: convert each module doc into a reusable
  generated Agent Skill.
- `prepare-paper-recovery-env`: prepare bounded recovery runtime evidence in an
  isolated environment.
- `recover-paper-result`: run a fast recovery experiment without reading the
  original implementation repo.
- `analyze-paper-recovery`: compare recovery evidence against the paper target
  and produce refine feedback.

Paper workflow defaults:

- Input can be a local PDF/text file, direct PDF URL, arXiv URL/id, paper title,
  or paper/repo pair.
- Default output layout is `<workspace_root>/<paper_slug>/distillation/` for
  process artifacts and `<workspace_root>/<paper_slug>/skills/` for generated
  skills.
- Default `iteration_budget` is `10` refine cycles after the first recovery.
- Default `recovery_mode` is `hard`, so reduced, proxy, toy, fallback, or
  smaller-model runs are not accepted as successful recovery.
- Missing packages, model caches, datasets, benchmark files, or credentials are
  setup work first. The workflow should create or reuse an isolated recovery
  environment under `$DISCO_CODING_AGENT_DIR/envs/` or `~/.disco/agent/envs/`,
  attempt targeted installs/downloads when allowed, and record command evidence
  before marking a blocker.

## Install Into Agents

### Shell Commands

If you do not already have a local checkout, clone this repository first:

```bash
git clone https://github.com/VectorSpaceLab/Auto-ML-Skills.git
cd Auto-ML-Skills
```

Run the install commands below from the repository root.

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

Install only the paper workflow into Codex:

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

Install only the paper workflow into Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R \
  meta-skills/create-paper-skills \
  meta-skills/paper-skills-distiller \
  meta-skills/plan-paper-skill-modules \
  meta-skills/create-paper-module-skill \
  meta-skills/prepare-paper-recovery-env \
  meta-skills/recover-paper-result \
  meta-skills/analyze-paper-recovery \
  ~/.claude/skills/
```

Restart the target agent after copying skills.

### Agent Instructions

Instead of running shell commands yourself, give one of these prompts to an
agent that can download this repository and write to the target agent's skills
directory. If you already have a local checkout, replace `local_checkout` with
that path.

For Codex:

```text
Install the DisCo workflow meta skills into Codex.

source_repo_url: https://github.com/VectorSpaceLab/Auto-ML-Skills.git
local_checkout: /tmp/Auto-ML-Skills
target_agent: codex
target_skills_root: ~/.codex/skills
workflow_set: all

Requirements:
- If local_checkout does not exist, clone source_repo_url into local_checkout.
- If local_checkout already exists, use it when it contains meta-skills/;
  otherwise stop and report the conflict.
- Verify local_checkout/meta-skills exists before copying.
- Create target_skills_root if it does not exist.
- For workflow_set: all, copy every direct child directory under
  local_checkout/meta-skills/ into target_skills_root/.
- For workflow_set: paper-only, copy only the listed directories from
  local_checkout/meta-skills/ into target_skills_root/.
- Preserve each skill directory exactly.
- Overwrite matching DisCo workflow meta-skill directories only; do not delete
  unrelated target skills.
- Do not modify repository source files except cloning the repository when
  needed.
- Report the copied skill names and remind me to restart Codex.

If I set workflow_set to paper-only, copy only:
- create-paper-skills
- paper-skills-distiller
- plan-paper-skill-modules
- create-paper-module-skill
- prepare-paper-recovery-env
- recover-paper-result
- analyze-paper-recovery
```

For Claude Code:

```text
Install the DisCo workflow meta skills into Claude Code.

source_repo_url: https://github.com/VectorSpaceLab/Auto-ML-Skills.git
local_checkout: /tmp/Auto-ML-Skills
target_agent: claude-code
target_skills_root: ~/.claude/skills
workflow_set: all

Requirements:
- If local_checkout does not exist, clone source_repo_url into local_checkout.
- If local_checkout already exists, use it when it contains meta-skills/;
  otherwise stop and report the conflict.
- Verify local_checkout/meta-skills exists before copying.
- Create target_skills_root if it does not exist.
- For workflow_set: all, copy every direct child directory under
  local_checkout/meta-skills/ into target_skills_root/.
- For workflow_set: paper-only, copy only the listed directories from
  local_checkout/meta-skills/ into target_skills_root/.
- Preserve each skill directory exactly.
- Overwrite matching DisCo workflow meta-skill directories only; do not delete
  unrelated target skills.
- Do not modify repository source files except cloning the repository when
  needed.
- Report the copied skill names and remind me to restart Claude Code.

If I set workflow_set to paper-only, copy only:
- create-paper-skills
- paper-skills-distiller
- plan-paper-skill-modules
- create-paper-module-skill
- prepare-paper-recovery-env
- recover-paper-result
- analyze-paper-recovery
```
