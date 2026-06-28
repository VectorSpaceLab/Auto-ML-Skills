# @auto-ml-skills/disco-tui

Terminal UI primitives used by DisCo.

This package provides the renderer, input handling, editor widgets, overlays,
selectors, and terminal helpers used by the DisCo CLI. It is kept in the
workspace so the CLI can be built and packaged from tracked source.

## Environment

DisCo TUI diagnostics and behavior flags use `DISCO_*` variables,
including `DISCO_TUI_WRITE_LOG`, `DISCO_HARDWARE_CURSOR`, and
`DISCO_CLEAR_ON_SHRINK`.

## License

Apache-2.0.

## Acknowledgement

This package is part of DisCo, which builds on
[pi](https://github.com/earendil-works/pi). We thank the pi authors and
contributors for their work.

## Development

```bash
npm run build
```

The root `src/package.json` builds this package before the DisCo CLI.
