# @auto-ml-skills/disco-ai

Model and provider utilities used by DisCo.

This package contains the LLM provider adapters used by the DisCo CLI,
including OpenAI-compatible APIs, Anthropic, Google, Vertex AI, Bedrock, Mistral,
OpenRouter, and other supported providers. End users normally configure models
through DisCo rather than importing this package directly.

## Environment

Provider API keys use their provider-native environment variables, such as
`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`,
`GOOGLE_CLOUD_API_KEY`, and `OPENROUTER_API_KEY`.

DisCo-specific runtime options use `DISCO_*` environment variables.

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
