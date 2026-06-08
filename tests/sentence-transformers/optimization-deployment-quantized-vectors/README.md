# Quantized Vector Outputs

## User Persona
A search infrastructure engineer reducing embedding storage cost.

## Scenario Coverage
- Skill area: optimization-deployment
- Capability: output embedding quantization, calibration, smoke checking
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/optimization-deployment/SKILL.md`, `sub-skills/optimization-deployment/references/workflows.md`, `sub-skills/optimization-deployment/scripts/embedding_optimization_smoke.py`
- Trigger expectation: The prompt mentions vector store cost, int8/binary embeddings, calibration, and shape/dtype checks.

## Expected Successful Behavior
The agent should use `encode(..., precision="int8")` or `quantize_embeddings`, explain calibration for int8 ranges, mention recall validation, and point to the smoke script.

## Failure Signals
The response only discusses ONNX model quantization, omits output vector dtype/shape checks, or treats binary quantization as quality-neutral.
