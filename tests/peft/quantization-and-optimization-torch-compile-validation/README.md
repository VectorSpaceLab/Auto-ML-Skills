# Torch Compile Validation

## User Persona
The user is a performance-focused engineer optimizing an existing PEFT inference path.

## Scenario Coverage
- Skill area: `quantization-and-optimization`
- Capability: `torch.compile`, multi-adapter load order, correctness validation
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `skills/peft/sub-skills/quantization-and-optimization/SKILL.md`, `skills/peft/sub-skills/quantization-and-optimization/references/performance.md`
- Trigger expectation: The prompt mentions PEFT adapters, inference, and `torch.compile`.

## Expected Successful Behavior
The agent should instruct the user to load all adapters before compiling, set active adapters before the compiled run, compare compiled and uncompiled outputs on a deterministic small batch, and warn that no exception does not prove correctness.

## Failure Signals
The answer fails if it compiles before loading adapters, tells the user to rely only on runtime success, or ignores dynamic adapter switching and graph-break risks.
