# Loading and Routing

## Source Types

OpenHands skill and microagent content can come from several scopes:

- Public repository skills: Markdown files under `skills/` in the OpenHands repository.
- User-level skills listed by the app-server metadata route: Markdown files under a user `.openhands/microagents` directory.
- Organization or user skill repositories resolved through provider conventions such as `.openhands`, `.agents`, or provider-specific config repositories.
- Project/repository skills in the selected workspace, including `.openhands/microagents/`, `.openhands/skills/`, and `.agents/skills/` according to V1 conversation endpoint documentation.
- Sandbox-provided skills derived from exposed URLs when the sandbox advertises them.

Public skills are appropriate for knowledge that should be available to all OpenHands users. Repository skills are private to a repository and are automatically relevant when that repository is selected or loaded.

## Metadata Listing Route

`GET /api/v1/skills/search` is implemented by the app-server user skills router. It lists metadata for global and user-level Markdown skills so the frontend can render available toggles or settings surfaces.

Key behavior:

- Global files are read from the OpenHands repository `skills/` directory.
- User files are read from a user `.openhands/microagents` directory.
- `README.md` is ignored.
- Files must start with YAML frontmatter to be included.
- Invalid YAML frontmatter is logged and skipped, not returned as a hard error.
- The response item contains `name`, `type`, `source`, and optional `triggers`.
- Results sort by source first, with global skills before user skills, then by name.
- Pagination uses `page_id` as the previous page’s last skill name and `limit` with an upper bound of 100.

Use this route when validating search/listing behavior, not as proof that every V1 conversation source is loaded. Conversation loading is handled separately through the agent-server flow.

## V1 Conversation Skill Loading

For V1 conversations, the app-server acts as a proxy and delegates skill merging to the agent-server:

1. The app-server builds organization/user skill repository configs from the selected repository owner, authenticated user accounts, and organization/group membership.
2. It builds sandbox config from exposed sandbox URLs when present.
3. It calls the agent-server `/api/skills` endpoint with `project_dir`, source enable flags, org configs, and optional sandbox config.
4. It converts the returned skill records into SDK `Skill` objects.
5. Conversation endpoints render the loaded skills back as V1 response objects.

Loading failures intentionally degrade safely in several places. Missing optional org skill repositories, provider enumeration errors, agent-server connection failures, HTTP errors, and per-skill conversion failures are logged and result in fewer returned skills or an empty list rather than crashing the whole conversation flow.

## Organization Skill Repositories

The V1 loader builds org/user configs by provider convention:

- GitHub-style providers can load both `<owner>/.openhands` and `<owner>/.agents`.
- GitLab uses `<owner>/openhands-config`.
- Azure DevOps uses `<org>/openhands-config/openhands-config`.
- Bitbucket Data Center is not globally enumerated because broad project listing can inject unrelated skills; selected-repository org loading still works through its normal path.

The selected repository owner is considered first so legacy single-org behavior is preserved for older agent-server images. Candidate repo verification is deduplicated, bounded, and concurrency-limited to avoid unbounded provider API fan-out.

## Conversation Skills Endpoint

`GET /api/v1/app-conversations/{conversation_id}/skills` returns the skills loaded for a V1 conversation. It returns an empty list when the sandbox is not running or unavailable for loading, and it returns errors for missing conversation/sandbox contexts according to the app-server tests.

Response classification is based on the converted SDK skill:

- `agentskills` when the skill is in AgentSkills format.
- `repo` when no trigger is present.
- `knowledge` when a keyword or task trigger is present.

The response extracts keyword values from `KeywordTrigger` and task command values from `TaskTrigger`. Existing tests cover repository skills with empty triggers, keyword skills with keyword trigger lists, task-trigger skills, paused sandboxes returning an empty list, and error handling during loading.

## Trigger Conversion

The V1 app-server conversion from agent-server skill records follows this rule:

- If `triggers` is empty or absent, the SDK `Skill` has no trigger.
- If any trigger starts with `/`, the skill becomes a `TaskTrigger` with the trigger list.
- Otherwise, the skill becomes a `KeywordTrigger` with the trigger list.

Because the conversion treats slash-prefixed lists as task triggers, avoid mixing slash commands and ordinary keywords in one skill unless tests prove the desired UI and runtime behavior.

## Slash Command UI

The frontend slash command hook builds the chat autocomplete menu from built-in commands plus loaded conversation skills:

- Normal skills appear in slash autocomplete only when they have explicit slash-prefixed triggers.
- AgentSkills-format skills without slash triggers get a derived `/<name>` command.
- Keyword-only skills do not appear in the slash menu.
- The hook waits for conversation skill loading to finish before adding skill-derived commands.

When a slash command does not appear, inspect whether the loaded skill’s `triggers` list contains a value starting with `/`, whether the skill is AgentSkills-format, and whether the conversation skills query has loaded successfully.

## Practical Routing Decisions

Use these decisions when reviewing or changing a skill:

- Public provider/tool guidance used across repositories belongs in `skills/` with keyword triggers.
- Repeatable interactive tasks should use slash triggers and, when needed, `inputs` metadata.
- Repository-specific setup, CI, style, and memory belong under `.openhands/skills/` for V1 or `.openhands/microagents/` for V0 compatibility.
- `repo.md` should describe durable repository knowledge and can load without explicit triggers.
- Skill list UI issues often involve `/api/v1/skills/search`; conversation runtime activation issues often involve agent-server `/api/skills` or trigger conversion.

## Native Verification Candidates

Behavior changes can be validated with focused existing tests:

- Skill metadata listing tests around `tests/unit/server/routes/test_skills_api.py`.
- Loader conversion and org-config tests around `tests/unit/app_server/test_skill_loader.py`.
- Conversation skill endpoint tests around `tests/unit/app_server/test_app_conversation_skills_endpoint.py`.
- Frontend slash-command tests around `frontend/__tests__/hooks/chat/use-slash-command.test.ts` when autocomplete behavior changes.

For prompt-only content changes, prefer read-only Markdown/frontmatter checks plus reviewer inspection over broad application startup.
