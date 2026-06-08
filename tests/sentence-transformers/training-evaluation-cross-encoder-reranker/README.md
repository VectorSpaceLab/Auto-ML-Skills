# CrossEncoder Reranker Training

## User Persona
An ML practitioner training a pairwise reranker.

## Scenario Coverage
- Skill area: training-evaluation
- Capability: CrossEncoder binary relevance training and reranking evaluation
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/training-evaluation/SKILL.md`, `sub-skills/training-evaluation/references/api-reference.md`, existing `skills/train-sentence-transformers/` when available
- Trigger expectation: The prompt names CrossEncoder, reranker, triples, binary relevance, and early stopping.

## Expected Successful Behavior
The agent should choose `CrossEncoderTrainer`, `BinaryCrossEntropyLoss`, `CrossEncoderRerankingEvaluator`, keyword constructor args, and mention early stopping/metric monitoring.

## Failure Signals
The response uses dense losses, ignores labels, lacks reranking evaluator structure, or omits the warning about reranker regression.
