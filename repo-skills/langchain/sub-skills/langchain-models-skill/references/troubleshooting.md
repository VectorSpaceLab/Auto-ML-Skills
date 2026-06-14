# Models Troubleshooting

- Missing provider import: install the specific provider integration package.
- Authentication failure: verify the provider key variable is set; do not print the key.
- Different output type than expected: chat models return message objects; LLMs return strings.
- Embedding dimension mismatch: rebuild the vector store or use the same embedding model/dimension as the index.
- Legacy import warning: replace `langchain.chat_models` and `langchain.llms` imports with provider package imports.
- Rate limits: lower concurrency in `.batch`/`.abatch` or set provider-specific retry/timeouts.
