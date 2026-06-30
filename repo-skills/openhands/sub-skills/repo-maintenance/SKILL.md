---
name: repo-maintenance
description: "Maintain OpenHands repository setup, validation, GitHub automation, lockfiles, PR artifacts, issue triage automation, and safe git practices."
disable-model-invocation: true
---

# Repo Maintenance

Use this sub-skill for OpenHands repo-wide maintenance that is not owned by a single implementation area: setup prerequisites, pre-commit hooks, lint/test/build command selection, CI workflow policy, lockfile regeneration, PR-only artifacts, issue triage automation, and safe git workflow.

## Route First

- Use [references/repo-guidance.md](references/repo-guidance.md) for setup, validation command selection, lockfile regeneration, GitHub Actions pinning, PR artifact rules, and git safety.
- Use [references/automation-scripts.md](references/automation-scripts.md) for issue triage automation, duplicate-check behavior, good-first-issue criteria, and the safe bundled classifier probe.
- Use [references/troubleshooting.md](references/troubleshooting.md) when Poetry, pre-commit, Node, Playwright, tmux, session/API-key, lockfile, CI, or issue automation workflows fail.
- Use [scripts/issue_triage_classifier_probe.py](scripts/issue_triage_classifier_probe.py) for an offline, deterministic issue-title/body sanity check before touching GitHub-backed triage automation.

## Choose This Sub-Skill For

- Installing or repairing repository hooks, choosing pre-commit/lint/test/build commands, and selecting the smallest validation command set before handoff.
- Maintaining `Makefile`, `dev_config/python`, repository-level setup docs, CI workflow policy, GitHub Actions pinning, or dependency lockfiles.
- Handling `.pr/` review artifacts, PR-readiness process, safe staging practices, fetch/rebase guidance, or avoiding destructive git commands.
- Updating issue automation logic related to duplicate checks, `good first issue` auto-labeling, auto-close duplicate candidates, and their focused unit tests.

## Route Away

- Python backend APIs, settings, sandboxes, server startup, and backend unit-test implementation belong in `../backend-development/SKILL.md` when available.
- React UI, TanStack Query hooks, frontend i18n, and frontend route behavior belong in `../frontend-development/SKILL.md` when available.
- Enterprise SaaS code, migrations, org/billing/integration services, and enterprise-specific test commands belong in `../enterprise-extension/SKILL.md` when available.
- Skill or microagent authoring formats belong in `../skills-and-microagents/SKILL.md` when available.

## Safety Defaults

- Before changing code, attempt `make install-pre-commit-hooks`. If Poetry or dependency installation blocks it, record the blocker and keep edits focused.
- Prefer targeted validation: backend pre-commit for Python/backend changes, frontend lint/build for frontend changes, extension lint/compile for VS Code extension changes, and focused pytest/Vitest tests for touched behavior.
- Preserve original lockfile tool versions when regenerating lockfiles; do not accept broad lockfile churn caused by newer Poetry or uv versions.
- Pin external third-party GitHub Actions to a full 40-character SHA with a trailing version comment unless the action is GitHub-authored or first-party OpenHands.
- Do not run destructive git commands, broad staging, networked issue automation, Docker-heavy flows, or auto-close actions unless the task explicitly requires them and credentials/environment are confirmed.
