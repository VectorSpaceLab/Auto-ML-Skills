# Dense Retriever Fine Tune

## User Persona
A machine learning engineer fine-tuning a bi-encoder retriever.

## Scenario Coverage
- Skill area: training-evaluation
- Capability: dense training data shape, MultipleNegativesRankingLoss, smoke test, IR evaluator
- Difficulty: advanced
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/training-evaluation/SKILL.md`, `sub-skills/training-evaluation/references/workflows.md`, existing `skills/train-sentence-transformers/` when available
- Trigger expectation: The prompt mentions fine-tune, dense retriever, sentence-transformers, loss, smoke test, and qrels.

## Expected Successful Behavior
The agent should map `question`/`answer` to anchor/positive pairs, use `SentenceTransformerTrainer`, `MultipleNegativesRankingLoss`, a one-step smoke test, and `InformationRetrievalEvaluator` with queries/corpus/relevant_docs.

## Failure Signals
The response chooses CrossEncoder, ignores qrels, omits smoke testing, or invents unsupported trainer arguments.
