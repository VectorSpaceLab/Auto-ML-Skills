# Subgraph Multi-Agent Troubleshooting

- Parent and child state schemas must line up unless using a wrapper node.
- Add reducers for outputs from parallel `Send` workers.
- Avoid parallel writes to child-only keys in parent state. Wrap subgraph calls so fan-out workers write only reducer-backed parent keys.
- Infinite supervisor loops usually need an explicit step budget or done condition.
- Cross-agent shared message state can grow quickly; summarize or scope messages per agent.
- Use stable node names and `subgraphs=True` for traceable streams.
- Use `Command.PARENT` only when intentionally escaping subgraph control flow.
