---
name: skills-and-microagents
description: "Create, update, and troubleshoot OpenHands skills and microagents, including public skills, repository instructions, frontmatter, triggers, and V0/V1 loading behavior."
disable-model-invocation: true
---

# Skills and Microagents

Use this sub-skill when changing OpenHands prompt-extension files: public skills in `skills/`, repository-specific instructions in `.openhands/microagents/` or `.openhands/skills/`, V0 microagent terminology, V1 skill terminology, frontmatter, triggers, skill listing, and conversation skill loading behavior.

## Start Here

- Read [Skill Format](references/skill-format.md) for file placement, V0/V1 terminology, frontmatter fields, trigger styles, repository-agent rules, and documentation standards.
- Read [Loading and Routing](references/loading-and-routing.md) for public/user/org/repository loading semantics, app-server proxy behavior, `/skills/search`, conversation skill responses, and slash-command routing.
- Read [Troubleshooting](references/troubleshooting.md) when YAML parsing, missing triggers, repository placement, agent-server loading, optional dependencies, UI listing, slash commands, or factual documentation review fails.

## Route Here

- Add or update a public reusable OpenHands skill under `skills/`.
- Add or update repository-specific instructions under `.openhands/microagents/` for V0 or `.openhands/skills/` for V1-compatible repository guidance.
- Fix malformed skill frontmatter, confusing V0/V1 terminology, trigger activation, slash-command visibility, skill search/listing metadata, or conversation skill-loading behavior.
- Review skill/microagent documentation for factual support and source-grounded claims.

## Route Away

- General Python app-server changes unrelated to skill loading belong in `../backend-development/SKILL.md` when available.
- React UI or TanStack Query changes unrelated to skill display, slash commands, or skill metadata belong in `../frontend-development/SKILL.md` when available.
- Enterprise SaaS-only skill repository behavior, org auth, or enterprise integration changes belong in `../enterprise-extension/SKILL.md` when available.
- DisCo-generated repo skill internals, verification reports, or import mechanics are outside this OpenHands authoring sub-skill.

## Core Rules

- Keep V0/V1 wording precise: V0 calls these prompt extensions `microagents`; V1 calls them `skills`, while V1 still supports legacy `.openhands/microagents/` paths for compatibility.
- Put public reusable knowledge or task workflows in `skills/`; keep private repository-specific guidance in the target repository’s `.openhands/skills/` or `.openhands/microagents/` directory.
- Use YAML frontmatter for public and triggered files. Repository-agent `repo.md` files can omit frontmatter, but explicit `name`, `type`, `agent`, and `triggers` fields make behavior easier to inspect.
- Choose triggers deliberately: keyword triggers activate knowledge context; slash triggers are task-style commands and affect chat autocomplete behavior.
- Documentation skills must stay evidence-grounded: include only claims verified from code, repository docs, official docs, or another reliable source.

## Native Validation Candidates

- Run read-only frontmatter checks over changed Markdown to catch missing delimiters, invalid YAML, non-list `triggers`, duplicate names, and public skills without clear trigger intent.
- Exercise focused tests around skill metadata listing, agent-server skill conversion, conversation skill responses, and slash-command filtering when code behavior changes.
- For content-only prompt edits, review placement, trigger specificity, V0/V1 terminology, factual evidence, and whether the skill is public reusable knowledge or private repository guidance.
