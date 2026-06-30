# Skill Format

## Terminology

OpenHands uses two names for the same broad prompt-extension concept depending on conversation version:

- V0 uses `microagents`; V0 is described as the stable terminology in the repository skills README.
- V1 uses `skills`; the app-server and frontend have V1-oriented skill endpoints and UI types.
- Public files under `skills/` can serve as V1 skills and V0 microagents from the same underlying Markdown files.
- V1 repository loading also keeps backward compatibility with `.openhands/microagents/`.

When editing user-facing copy, prefer the term that matches the surface being changed. Use `microagent` for V0 documentation and existing `.openhands/microagents/` flows; use `skill` for V1 app-server, V1 UI, and `skills/` authoring copy. If both are relevant, state both explicitly instead of implying that one path replaced the other everywhere.

## Placement

Use the smallest scope that matches the content:

- Public reusable knowledge or workflows: `skills/<name>.md`.
- V1 repository-specific guidance: `.openhands/skills/<name>.md` in the target repository.
- V0 or compatibility repository-specific guidance: `.openhands/microagents/<name>.md` in the target repository.
- Repository memory/instructions that should always load for a repo are commonly stored as `.openhands/microagents/repo.md`; V1 can also read repository skills from `.openhands/skills/`.

Do not put project-private team policy into public `skills/`. Do not put broadly reusable provider/tool guidance into a single repository’s `.openhands/` directory unless the user explicitly wants local-only behavior.

## Public Skill Frontmatter

Most public skills use Markdown with YAML frontmatter. Representative fields in `skills/*.md` include:

```yaml
---
name: github
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
- github
- git
---
```

Field guidance:

- `name`: stable skill identifier. Prefer lowercase words separated by underscores or hyphens, matching nearby examples and UI expectations.
- `type`: usually `knowledge` for keyword/slash-triggered expertise; `repo` is used for repository agents.
- `version`: examples commonly use `1.0.0` for public skills.
- `agent`: examples commonly use `CodeActAgent`.
- `triggers`: list of keywords or slash commands that activate the skill.
- `inputs`: optional list used by slash-command task skills to describe templated parameters.

The `/api/v1/skills/search` metadata endpoint parses only Markdown files with frontmatter. It skips files without frontmatter, skips `README.md`, falls back from missing `name` to the filename stem, defaults missing `type` to `knowledge`, and returns `triggers` as `null` when absent.

## Repository Agent Frontmatter

Repository-specific instructions can be explicit or minimal:

```yaml
---
name: repo
type: repo
agent: CodeActAgent
---
```

The repository skills README states that frontmatter is optional for repository agents such as `repo.md`; if omitted, the loader can treat the file with default repository-agent settings. Even when optional, frontmatter is helpful when the file must appear clearly in listings, tests, or code review.

Repository-agent content should capture durable repository facts: purpose, setup, structure, required commands, CI checks, style rules, and team conventions. Avoid issue-specific debugging notes, temporary PR context, secrets, private machine paths, and claims that cannot be re-verified.

## Trigger Styles

Trigger values control how a skill is activated and presented:

- Keyword triggers such as `github`, `docker`, or `documentation` become `KeywordTrigger` entries in V1 loader conversion.
- Slash triggers such as `/remember`, `/add_repo_inst`, or `/codereview` are task-style triggers and become `TaskTrigger` entries when the converted trigger list starts with slash commands.
- Empty or missing triggers mean the converted V1 `Skill` has no trigger and is classified as repository-style context in conversation skill responses unless it is an AgentSkills-format skill.

Keep trigger lists distinctive. Generic words can activate context too often; overly narrow triggers can make a useful skill invisible. For task workflows, prefer a stable slash trigger and document any `inputs` placeholders in frontmatter and body text.

Avoid mixing keyword and slash triggers in one file unless the intended conversion and UI behavior are tested. The V1 conversion code treats a trigger list containing slash-prefixed entries as task-style, and the frontend slash menu only shows explicit slash triggers for normal skills.

## Content Rules

A good OpenHands skill or microagent is focused, factual, and operational:

- Focus on one domain or workflow.
- State required environment variables, credentials, and tools without exposing secret values.
- Prefer APIs over browser flows when an existing provider skill requires that pattern.
- Include safety boundaries, such as not pushing branches unless the user asks.
- Use concise examples only when they make the workflow less ambiguous.
- For documentation-oriented skills, every factual statement should be traceable to source code, repo docs, official docs, or another reliable reference.

When updating existing skills, preserve the established voice and frontmatter style unless the task is specifically to modernize the format.

## Review Checklist

Before handoff, check:

- Correct placement: public reusable skill vs repository-private instruction.
- Valid YAML delimiters and parseable frontmatter.
- Stable `name`, appropriate `type`, and trigger list with expected keyword or slash behavior.
- Clear V0 `microagent` vs V1 `skill` terminology.
- No secrets, local machine paths, or unsupported claims.
- Evidence cited or summarized for documentation facts.
- Tests or read-only lint checks identified when behavior changes.
