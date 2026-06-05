# Observability Configuration

## LangSmith Environment

Typical variables:

- `LANGSMITH_TRACING=true`
- `LANGSMITH_API_KEY`
- `LANGSMITH_PROJECT`
- Optional endpoint variables for self-hosted or non-default deployments.

Do not print `LANGSMITH_API_KEY`. It is enough to report present/missing.

## Tags And Metadata

Use tags for low-cardinality labels such as `rag`, `agent`, or `smoke`. Use metadata for non-secret run context such as component name, dataset split, or experiment ID.

Avoid:

- API keys, tokens, passwords, raw user secrets.
- Full documents when privacy policy forbids tracing content.
- High-cardinality unbounded metadata values.

## Integration Debugging

When diagnosing a production run:

1. Confirm package versions and provider package names.
2. Run a no-key fake chain with callbacks.
3. Run a live minimal provider call without tracing.
4. Enable tracing with scrubbed inputs and clear tags.
