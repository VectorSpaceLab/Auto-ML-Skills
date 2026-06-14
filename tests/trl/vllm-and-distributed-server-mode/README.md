# vLLM Server Mode

## User Persona
An ML platform engineer separating generation and training resources.

## Scenario Coverage
- Skill area: `vllm-and-distributed`
- Capability: `trl vllm-serve`, GRPO server mode, backend verification, memory flags
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `vllm-and-distributed/SKILL.md`, `references/vllm-reference.md`, root environment reference
- Trigger expectation: The prompt names TRL GRPO, vLLM server mode, and backend checks.

## Expected Successful Behavior
The agent should provide `pip install "trl[vllm]"`, `import vllm`, `trl vllm-serve --help`, a `trl vllm-serve --model ... --host ... --port ...` command, and `GRPOConfig(use_vllm=True, vllm_mode="server", vllm_server_base_url=...)`. It should warn that TRL import success is not enough to prove vLLM works.

## Failure Signals
The response only shows colocate mode, omits server startup, fails to mention vLLM install/backend checks, or claims GPU support without verification.
