# Coding-Agent Sandbox Notes

Read this when preparing the sandbox side of coding-agent RL.

## Required Capabilities

The sandbox backend must support:

- Booting a clean isolated environment for each sample.
- Running shell commands with timeout.
- Reading and writing files.
- Capturing a patch/diff after the agent edits code.
- Running the evaluator in a clean state to reduce test cheating.
- Allowing the sandbox to reach the adapter endpoint on the slime head node.

## Environment Knobs

Keep these as runtime environment variables rather than public config constants:

- Head host reachable from sandbox.
- Adapter bind host and port.
- Sandbox provider API key.
- Sandbox metadata JSON path.
- Host-side tarballs or boot artifacts for agent CLI dependencies.
- Per-run time budgets and boot concurrency.

## Network Rule

Do not bind the adapter only to loopback if the sandbox runs outside the same network namespace. The sandbox must reach the adapter over a routable address.

## Security Rule

Use a second clean sandbox for grading when possible. The agent-run sandbox may contain edited files, caches, or generated state; the grader should evaluate only the submitted patch under controlled conditions.
