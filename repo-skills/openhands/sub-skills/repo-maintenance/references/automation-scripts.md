# OpenHands Automation Scripts

This reference covers repo-level automation, especially issue triage workflows. It is intentionally conservative because the production automation can label, comment on, or close GitHub issues.

## Issue Opened Workflow

The issue-opened automation has these main paths:

- `issue-duplicate-check`: runs when an issue opens, or manually in issue-check mode. It delegates duplicate classification to the OpenHands issue duplicate checker plugin.
- `issue-good-first-issue-check`: runs after the duplicate check succeeds or is skipped, unless precheck rules block it.
- `auto-close-duplicates`: runs on schedule or manual mode to close aged duplicate candidates through the OpenHands extension plugin.
- `smoke-clone`: manual smoke path that shallow-clones the repository.

The good-first-issue path is intentionally guarded by duplicate results. It skips auto-labeling when the issue is already labeled `good first issue`, is marked `duplicate-candidate`, is a pull request, is closed or locked, or the duplicate check classified it as duplicate or overlapping-scope.

## Good First Issue Criteria

The upstream script asks an OpenHands Cloud conversation to decide whether a new issue is safe for newcomers. The criteria are conservative:

- The work is narrow and should be solvable as one issue.
- The expected outcome is clear enough that a contributor does not need major discovery.
- The likely fix is well bounded and avoids deep architecture, enterprise-only context, migrations, security-sensitive work, infrastructure, or cross-repo coordination.
- Validation is straightforward and can be described with ordinary How-to-Test steps; screenshots or video should be practical for user-facing changes.
- Review does not require special credentials, paid services, or hard-to-reproduce environments.

The result is normalized so `should_apply_label` is false unless confidence is `high` and no disqualifiers remain. Criteria and disqualifier lists are capped to short lists.

## Duplicate Check Behavior

The duplicate-check script and plugin are networked. They inspect GitHub issues, search open and recently closed issues, and distinguish:

- `duplicate`: exact or near-exact duplicate; may become an auto-close candidate only with high confidence and a clear canonical issue.
- `overlapping-scope`: not identical, but discussion or fix planning should likely happen in one canonical issue; never auto-close automatically.
- `related-but-distinct`: similar area but should remain separate.
- `no-match`: no strong candidate.

Do not run duplicate or auto-close automation casually. Confirm credentials, target issue number, repository, event mode, and whether the command can comment, label, or close issues.

## Bundled Offline Probe

Use `scripts/issue_triage_classifier_probe.py` as a local, deterministic sanity check before editing issue triage prompts or reviewing proposed labels. It accepts one JSON issue document from a file or stdin and emits classification hints without network calls, GitHub credentials, OpenHands API calls, comments, labels, or state changes.

Example fixture:

```json
{
  "title": "Typo in settings tooltip",
  "body": "The settings page tooltip says teh. Expected: the.",
  "labels": ["frontend", "docs"]
}
```

Example commands from the sub-skill directory:

```bash
python scripts/issue_triage_classifier_probe.py --help
python scripts/issue_triage_classifier_probe.py issue.json
cat issue.json | python scripts/issue_triage_classifier_probe.py -
```

Treat the output as hints only. It is not a replacement for the production OpenHands/GitHub workflow, maintainer judgment, or focused unit tests.

## Updating Automation Safely

When changing issue triage automation:

- Keep networked behavior in production scripts or workflows; keep test/probe helpers offline and deterministic.
- Preserve the duplicate-check veto before good-first-issue auto-labeling.
- Update focused tests for prompt content, result normalization, confidence handling, and disqualifier behavior.
- Use `tests/unit/test_issue_good_first_issue_check_openhands.py` as the primary native unit-test candidate for good-first-issue changes.
- For duplicate-check prompt or normalization changes, inspect the duplicate script behavior carefully and add focused tests if the changed code lacks coverage.
- Never store real GitHub or OpenHands API keys in fixtures, `.pr/`, or runtime skill content.

## Native Verification Candidates

Safe native candidates after automation edits include:

- `poetry run pytest tests/unit/test_issue_good_first_issue_check_openhands.py`
- Focused pytest selectors for the changed normalization or prompt tests.
- `python scripts/issue_good_first_issue_check_openhands.py --help` only if dependencies are available; avoid running it against live issues unless credentials and side effects are intentional.

Avoid running live duplicate checks or auto-close paths in a development shell unless explicitly requested and authorized.
