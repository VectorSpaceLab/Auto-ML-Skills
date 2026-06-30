# Troubleshooting Skills and Microagents

## Install and Import Problems

Symptoms:

- `make install-pre-commit-hooks` fails before prompt-file edits.
- Backend skill tests cannot import `openhands` modules.
- V1 skill loader tests fail before reaching skill logic.

Checks:

- Confirm the repository’s Python tooling is available before running backend tests. This repo expects Poetry-managed Python dependencies for many test commands.
- If Poetry is missing, record the blocker and keep content-only skill edits minimal; do not claim backend runtime verification.
- For import-related backend tests, prefer focused test files after dependencies are installed rather than starting the full application.
- Remember that prompt-only Markdown changes usually do not require a live agent-server, Docker runtime, or frontend build unless related code changed.

Relevant focused commands when the environment supports them:

```bash
poetry run pytest tests/unit/server/routes/test_skills_api.py
poetry run pytest tests/unit/app_server/test_skill_loader.py
poetry run pytest tests/unit/app_server/test_app_conversation_skills_endpoint.py
```

## Optional Dependency and Service Problems

Symptoms:

- Conversation skills are empty even though metadata listing works.
- Skill loading logs mention agent-server connection errors or HTTP failures.
- Organization-level skills fail to load for one provider but conversations continue.

Checks:

- Distinguish app-server metadata listing from V1 conversation loading. `/api/v1/skills/search` reads global/user Markdown metadata locally; V1 conversations call the agent-server `/api/skills` endpoint.
- Confirm the sandbox is running and exposes an agent-server URL before expecting conversation skill loading.
- Treat missing organization config repositories as optional. The loader logs failures and degrades to fewer loaded sources.
- Avoid running live provider enumeration or cloning checks in tests; use mocks around provider handlers and authenticated URL resolution.

If only public skill metadata is broken, inspect the user skills router and frontmatter parsing. If runtime activation is broken, inspect agent-server response payloads, `SkillInfo` conversion, and conversation endpoint classification.

## Config and Data Problems

Symptoms:

- A Markdown file does not appear in skill search results.
- A repository instruction loads in one conversation mode but not another.
- A skill appears with the wrong name or type.

Checks:

- Ensure the file is in the expected directory: public `skills/`, V1 repository `.openhands/skills/`, V0-compatible repository `.openhands/microagents/`, or user-level `.openhands/microagents` depending on the feature being tested.
- Public/user metadata listing requires YAML frontmatter at the start of the file. Files without frontmatter are skipped by the metadata route.
- `README.md` is intentionally skipped by the metadata route.
- If `name` is missing in frontmatter, the metadata route falls back to the filename stem.
- If `type` is missing in frontmatter, the metadata route defaults to `knowledge`.
- If `triggers` is missing, metadata may return no triggers and V1 conversion may treat the skill as untriggered repository-style context.

For repository `repo.md` files, frontmatter can be optional according to the repository skills README. Use explicit frontmatter anyway when tests, UI metadata, or reviewer clarity matter.

## Malformed YAML and Frontmatter

Symptoms:

- A skill file is silently absent from `/api/v1/skills/search`.
- Logs mention invalid YAML frontmatter.
- Trigger values appear as one string instead of a list.

Checks:

- Frontmatter must start at byte one with `---` and have a closing `---` delimiter.
- YAML indentation must be valid. Nearby examples use either top-level `- trigger` lines or indented list items under `triggers:`.
- `triggers` should be a list of strings, not a comma-separated string.
- Quote trigger values only when YAML would otherwise interpret them incorrectly.
- Avoid tabs in frontmatter.

A simple read-only lint can scan changed Markdown for delimiters, parse YAML, assert `triggers` is absent or a string list, and report duplicate `name` values without modifying files.

## Trigger and Routing Confusion

Symptoms:

- A knowledge skill activates too often.
- A skill does not appear in the slash-command menu.
- A slash-trigger skill is classified unexpectedly.

Checks:

- Keyword triggers should be distinctive and domain-specific.
- Slash commands must start with `/` to appear as explicit slash commands in the V1 frontend autocomplete for normal skills.
- AgentSkills-format skills can get derived slash commands, but normal OpenHands Markdown skills need explicit slash triggers.
- The V1 converter creates a task trigger when any trigger starts with `/`; do not mix slash and non-slash triggers without a test that proves the desired result.
- Conversation skill response type is `repo` for no trigger and `knowledge` for keyword or task triggers unless the skill is AgentSkills format.

For frontend autocomplete failures, inspect the conversation skills response first. The UI can only render commands from loaded skills and slash-prefixed triggers.

## CLI and API Misuse

Symptoms:

- Tests call the wrong endpoint for the behavior under review.
- A developer expects `/api/v1/skills/search` to show repository or sandbox skills.
- A conversation endpoint returns no skills for a paused sandbox.

Checks:

- Use `/api/v1/skills/search` for global/user metadata listing.
- Use the conversation skills endpoint for loaded V1 conversation skills from public, user, org, project, and sandbox sources.
- Paused or unavailable sandboxes can legitimately return an empty conversation skills list.
- Do not start the full app for a frontmatter-only review unless the task specifically requires end-to-end UI verification.

## Documentation Failures

Symptoms:

- Reviewers ask for sources for skill documentation claims.
- A documentation skill describes behavior that is not supported by current code.
- A generated repository instruction includes temporary or private details.

Checks:

- Follow the repository documentation microagent: include only facts backed by source code, repository docs, official docs, or reliable references.
- In review notes or PR summaries, name the source category used for each new factual claim.
- Do not include private local paths, local virtualenv prefixes, raw credentials, or temporary PR/debugging notes in public or repository instruction files.
- Keep repository memory durable: setup, structure, commands, style, workflows, and CI checks are appropriate; issue-specific fixes are not.

## Workflow-Specific Failures

### Adding a public skill

If a new public skill is not discoverable, check placement under `skills/`, frontmatter delimiters, `name`, `type`, and `triggers`. Then run or propose focused metadata route tests.

### Adding repository guidance

If repository guidance is ignored, verify whether the conversation mode expects `.openhands/microagents/`, `.openhands/skills/`, or both. For V1 compatibility, `.openhands/skills/` is preferred while `.openhands/microagents/` remains supported.

### Adding a slash task

If the command does not autocomplete, ensure the trigger starts with `/`, the conversation skills endpoint returns that trigger, and the skill is not merely keyword-triggered. Add frontend hook coverage when changing autocomplete behavior.

### Updating loader code

If loader changes cause broad failures, narrow the issue to org config construction, agent-server request payload, response conversion, or endpoint classification. Mock provider services and agent-server HTTP calls; do not depend on live Git providers.

## Hard Usability Cases

Use cases that catch subtle mistakes:

- Add a public `/generate-release-notes` task skill with `inputs`, plus a repository `repo.md` instruction without frontmatter. The expected solution keeps public task and private repo guidance separate, makes only the slash task appear in autocomplete, and explains why missing repo frontmatter is acceptable but not useful for metadata listing.
- Diagnose a V1 conversation where `/api/v1/skills/search` lists a `docker` skill but the conversation slash menu does not show it. The expected solution distinguishes metadata listing from conversation loading, identifies that keyword triggers do not create slash commands, and checks agent-server skill response before changing frontend code.
