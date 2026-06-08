# ONNX Export For Deployment

## User Persona
A deployment engineer optimizing CPU inference.

## Scenario Coverage
- Skill area: optimization-deployment
- Capability: ONNX backend, export, optimization, save/reload, file_name
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/optimization-deployment/SKILL.md`, `sub-skills/optimization-deployment/references/workflows.md`
- Trigger expectation: The prompt names sentence-transformers, ONNX, CPU inference, export, and optimized filename loading.

## Expected Successful Behavior
The agent should recommend `[onnx]`, load with `backend="onnx"`, call `export_optimized_onnx_model`, save artifacts, and reload with `model_kwargs={"file_name": "onnx/model_O3.onnx"}` or equivalent.

## Failure Signals
The response omits saving, re-exports on every startup, uses GPU-only O4 for CPU without caveat, or ignores `file_name`.
