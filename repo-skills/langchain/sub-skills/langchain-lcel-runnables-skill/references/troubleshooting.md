# LCEL Troubleshooting

- Raw string input to a multi-variable prompt fails; pass a dict with all variables.
- Dict output from a parallel mapping may not match downstream prompt variables; insert `RunnablePassthrough.assign` or a lambda to normalize.
- Fallbacks must return the same broad type as the primary runnable.
- Async methods require awaiting; avoid `asyncio.run` inside active event loops.
- Metadata and tags may be sent to tracing; scrub secrets before config.
- `batch` order follows input order, but provider rate limits may still fail when concurrency is too high.
