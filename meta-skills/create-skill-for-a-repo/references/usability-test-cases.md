# Usability Test Cases

## Purpose

Read this reference after creating the generated skill files. It defines how to automatically generate usability test case directories that simulate realistic future users asking agents to use the generated repo skill.

These test cases are separate from the generated skill's runtime content and separate from optional `evals/` development artifacts.

## Output Location

- If the user specified a test case output path, write the test case directories there.
- Otherwise write them under `<active-skills-root>/tests/<chosen-skill-id>/`.
- Do not create standalone markdown case files such as `inference/basic-user.md`. Each case must be a directory with the required files below.

Do not put these usability test cases inside the generated skill directory unless the user requested that layout. Do not link them from generated `SKILL.md` files as runtime documentation.

## Case Directory Format

Each test case is one directory named from the target skill area plus the scenario being tested:

```text
tests/<chosen-skill-id>/
  <sub-skill-id>-<scenario-slug>/
    user_request.txt
    README.md
```

Use the generated sub-skill id as the prefix when the case targets a sub-skill, for example `inference-minimal-smoke-test` or `training-invalid-config-debugging`. If the generated skill has no sub-skills, use the root skill id as the prefix. Normalize the full directory name to lowercase hyphen style, keep it descriptive, and avoid generic names such as `case-1` or `basic`.

A single sub-skill can and usually should have multiple case directories when it has multiple important scenarios. For example, `inference-minimal-smoke-test`, `inference-batch-inputs`, and `inference-missing-model-debugging` can all target the same `inference` sub-skill.

Every case directory must contain:

- `user_request.txt`: the exact future-user prompt. The whole file must be directly copyable into an agent input box. Do not add a title, markdown heading, metadata, explanation, "User Prompt:" label, or surrounding commentary.
- `README.md`: the reviewer-facing explanation of the case, including the user persona, scenario coverage, expected successful behavior, failure signals, and any important notes about why the case should trigger the generated skill.

## Default Generation Strategy

If the user explicitly asks for a specific type, number, format, role, workflow, or difficulty of cases, follow that request while preserving the required case-directory shape unless the user explicitly overrides it. Otherwise use this default strategy.

Create enough test cases to exercise the generated skill's actual surface area:

- For small single-workflow repos, create at least 4-6 case directories.
- For medium repos with several sub-skills, create roughly 2-4 case directories per major sub-skill.
- For large repos, create a broad representative set across all major user-facing capabilities identified in the coverage/depth matrix. Do not create hundreds of cases; prioritize coverage of distinct workflows, CLIs, APIs, data formats, configuration paths, and troubleshooting situations.

Design cases for diversity along three axes:

- User role and familiarity: include novice users who only know the repo's broad purpose, users who know the task but not the repo API, experienced users who name specific modules/classes/CLIs, maintainers integrating the package into a larger project, and users debugging a failure.
- Scenario difficulty: include minimal setup or smoke-test prompts, ordinary end-to-end workflows, parameter/config changes, migration or integration tasks, edge cases, and challenging troubleshooting prompts involving errors, missing dependencies, invalid data, performance constraints, or confusing API behavior.
- Functional breadth: cover every major sub-skill and public capability from the coverage/depth matrix when practical. If a capability is too minor for a dedicated case, include it in a broader case or explain in an index why it was not tested.

## `user_request.txt` Requirements

Write the prompt exactly as a real user might ask later:

- Usually do not mention the generated skill by name. The point is to test whether the skill triggers and routes correctly from a natural request.
- Include enough task context for an agent to act, such as the user's goal, relevant files or data shape, constraints, error messages, or desired output.
- Do not expose research notes, the original repo checkout path, the temporary inspection environment, or the fact that this is a test case.
- Keep the prompt copy-pasteable as a single complete request. If the scenario needs multiline input, include it naturally in the request body without adding explanatory wrappers outside the user's voice.

## `README.md` Template

Each case `README.md` must explain the test case without being the prompt itself. Use this structure unless the user requested additional sections:

```markdown
# [Short Case Title]

## User Persona
[Who the user is, their repo familiarity, and what they already know.]

## Scenario Coverage
- Skill area: [root skill or sub-skill id]
- Capability: [workflow/API/CLI/config/troubleshooting target]
- Difficulty: [basic/intermediate/advanced/troubleshooting]
- Prompt file: `user_request.txt`
- Expected references/scripts: [generated skill files the future agent should naturally use]
- Trigger expectation: [why the generated skill should trigger for this prompt, or why the case intentionally tests a borderline trigger]

## Expected Successful Behavior
[Concrete behavior that would show the skill is usable: commands, files, APIs, decisions, troubleshooting steps, or verification checks the agent should produce.]

## Failure Signals
[Observable signs that the generated skill is too thin, missing routing, missing references/scripts, relying on original repo paths, leaking local environment details, disabling auto-invocation unexpectedly, or giving unverified claims.]
```

## Index

Also write an `index.md` in the test case output directory. The index must list every case directory, the target root skill or sub-skill, user role, scenario, covered capability, and difficulty.

Include a short coverage note comparing the case set against the coverage/depth matrix. If any generated sub-skill or major capability has no test case directory, mark that as a coverage gap unless the user explicitly scoped the cases.
