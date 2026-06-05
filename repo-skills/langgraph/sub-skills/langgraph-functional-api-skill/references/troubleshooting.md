# Functional API Troubleshooting

- Decorator missing: inspect installed `langgraph.func` version.
- State behavior unclear: choose StateGraph for explicit schemas and reducers.
- Checkpoints not working: verify checkpointer and `thread_id` rules.
- Streaming differs from graph builder: inspect runtime outputs and route to streaming sub-skill.
- Complex graph is hard to debug: migrate to explicit StateGraph.
