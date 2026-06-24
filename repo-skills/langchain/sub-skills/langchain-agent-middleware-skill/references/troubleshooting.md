# Agent Middleware Troubleshooting

- Middleware symbol missing: inspect installed `langchain.agents.middleware`; APIs can move across LangChain 1.x releases.
- Middleware does not run: verify it is passed to `create_agent` through the current version's expected parameter.
- Tool behavior is wrong: check tool schema/provider support before blaming middleware.
- Agent loops after middleware rejection: tighten prompts, add explicit termination, or route to LangGraph for durable control.
- Secrets leaked: remove API keys/tokens from prompts, state dumps, tags, metadata, and traces.
