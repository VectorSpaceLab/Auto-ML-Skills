# Repository Provenance

## Purpose

Read this before deciding whether this skill is current for an OpenHands checkout. If the current repo commit, dirty state, package version, or major evidence paths differ from this snapshot, run `refresh-repo-skill`.

## Snapshot

```json
{
  "schema": "disco.repo-provenance.v1",
  "generated_at_utc": "2026-06-29T00:00:00Z",
  "repository": {
    "name": "OpenHands",
    "remote_url": "omitted-private-or-unknown",
    "vcs": "git",
    "branch": "main",
    "tag": null,
    "commit": "b34d67e19f093fd9a8dc33fb85eddb976680025c",
    "working_tree": "clean",
    "dirty_paths": []
  },
  "packages": [
    {
      "name": "openhands-ai",
      "version": "1.8.0",
      "import_names": ["openhands"]
    },
    {
      "name": "openhands-frontend",
      "version": "1.8.0",
      "import_names": []
    },
    {
      "name": "enterprise_server",
      "version": "0.0.1",
      "import_names": ["server", "storage", "sync", "integrations"]
    }
  ],
  "evidence": {
    "source_roots": ["openhands", "frontend/src", "enterprise"],
    "docs": ["README.md", "frontend/README.md", "enterprise/README.md", "openhands/app_server/README.md", "skills/README.md", "tests/unit/README.md"],
    "skills_and_microagents": ["skills", ".openhands/microagents"],
    "tests": ["tests/unit", "frontend/__tests__", "frontend/tests", "enterprise/tests/unit"],
    "scripts": ["scripts", "frontend/scripts", ".github/scripts", "enterprise/sync"],
    "configs": ["pyproject.toml", "enterprise/pyproject.toml", "frontend/package.json", "Makefile", "dev_config/python"]
  }
}
```

## Refresh Check

- If `git rev-parse HEAD` differs from `repository.commit`, treat this skill as potentially stale and run `refresh-repo-skill`.
- If the current working tree is dirty and this snapshot was clean, or dirty paths differ from this snapshot, run `refresh-repo-skill`.
- If package versions, public routes, frontend architecture, enterprise import patterns, validation commands, or skill/microagent loading behavior changed, run `refresh-repo-skill` even on the same commit.
- If this skill is imported into a different agent and used against a checkout without the evidence paths above, validate the repository layout before following route-specific guidance.
