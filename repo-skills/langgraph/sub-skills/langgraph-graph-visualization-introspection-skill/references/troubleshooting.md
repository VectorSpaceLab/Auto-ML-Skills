# Graph Visualization Troubleshooting

## Conditional Edge Shows Too Many Targets

Add `path_map` to `add_conditional_edges` or annotate the route function return type with `Literal[...]`.

## Mermaid PNG Fails

Use `draw_mermaid()` text output. PNG rendering can require extra dependencies or a renderer service.

## `destinations` Does Not Route

`destinations` is for graph rendering metadata. Implement routing with edges, conditional edges, `Command`, or `Send`.

## `get_graph()` Fails When Mixing Destinations And Conditional Edges

Some versions can hit diagram rendering bugs when a node combines rendering-only `destinations` metadata with conditional edge labels. Split the smoke into a conditional-edge graph and a separate `destinations` graph, or remove `destinations` from nodes that already have explicit conditional edges.

## Xray Output Is Large

Use normal `get_graph()` first. Load `xray=True` only when inspecting subgraphs or internals.
