# Changelog

## 0.0.2

- Initial DisCo release under the `@auto-ml-skills` npm scope.
- Derived from PI `0.79.1`; DisCo uses its own package version series
  starting at `0.0.2`.
- Rebranded the adapted coding-agent runtime as DisCo.
- Bundled DisCo meta-skills for repo skill creation, environment
  preparation, repo-drift refresh, existing skill extension, imported
  repo-skill routing, and explicit export into other agent tools.
- Generated and refreshed repo skills now include `references/repo-provenance.md`
  so future agents can compare source commit, dirty state, package version, and
  evidence paths before deciding whether a skill is stale.
- Repo skill creation now requires complete per-sub-skill briefs for workflow
  subagents, canonical sub-skill id/name consistency, and main-agent review
  against explicit depth, evidence, routing, self-containment, and artifact
  boundary rubrics before integration.
- Added structured import confirmation and DisCo-first
  `repo-skills-router` updates after a user approves importing a verified
  repo-specific skill. Exporting DisCo's managed skill library into other
  agent tools is handled by the explicit `import-repo-skills-to-agent` meta skill.
- Removed default calls to upstream update and install telemetry endpoints.
- Fixed source builds when the optional interactive assets directory is absent
  in a fresh checkout.
