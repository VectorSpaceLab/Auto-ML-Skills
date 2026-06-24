# Agents And Tools Troubleshooting

- Tool has empty schema: add type hints and avoid `*args`/`**kwargs`.
- Tool name is unclear: set a precise function name or explicit tool name.
- Provider ignores tools: verify the specific model supports tool calling.
- Agent loops: tighten system prompt, cap recursion/steps if available, and simplify tool descriptions.
- Side effects in smoke tests: replace with fake/list/debug mode.
- Legacy agent imports fail: modern code should use `langchain.agents.create_agent`; old classic agents may require `langchain-classic`.
