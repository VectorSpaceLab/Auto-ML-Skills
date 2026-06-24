# Workflows

## Supervisor Pattern

1. Parent graph maintains shared task state.
2. Supervisor node decides the next worker.
3. Worker nodes can be normal functions, compiled graphs, or prebuilt agents.
4. Supervisor routes until done.

## Handoff Pattern

Use `Command(goto=target, update=payload)` when one agent hands control to another. Keep handoff payloads explicit and typed.

## Hierarchical Teams

1. Create a subgraph for each team.
2. Parent graph routes tasks to teams.
3. Team subgraphs route internally.
4. Return summarized results to the parent state.

## Map-Reduce

1. Fan out with `Send`.
2. Worker processes one item.
3. Reducer accumulates outputs.
4. Join node summarizes.

## Multi-Agent With Tools

Each agent can be a `create_react_agent` graph or a custom model/tool graph. Keep shared durable memory intentional by using thread IDs and namespaced state keys.
