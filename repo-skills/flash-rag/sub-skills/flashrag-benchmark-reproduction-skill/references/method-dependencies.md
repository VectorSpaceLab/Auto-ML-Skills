# Method Dependency Matrix

Read this before running a named benchmark method.

| Method family | Extra assets beyond base generator/retriever/index | Notes |
| --- | --- | --- |
| `naive`, `zero-shot` | None beyond base generator and dataset | Good first smoke tests |
| `AAR-contriever` | AAR retriever and separate index | Pooling often differs from E5; rebuild the index |
| `llmlingua` | Llama2-7B or compatible compressor model | Compression changes prompt content; compare exact prompt settings |
| `recomp` | Abstractive compressor checkpoints per dataset where available | Missing dataset-specific checkpoints may use fallback choices |
| `selective-context` | GPT2 or configured refiner model | Uses retrieved documents as refiner input in FlashRAG setup |
| `ret-robust` | Base Llama2-13B plus LoRA checkpoint | Dataset-specific LoRA choice affects results |
| `sure`, `replug`, `flare`, `iterretgen`, `ircot`, `trace` | Usually base assets plus method prompt/config choices | TRACE needs triple extraction and chain construction prompts |
| `skr` | Encoder model plus inference-time training data | Validate training data JSON before a long run |
| `selfrag` | Self-RAG generator checkpoint and vLLM support | Documented as vLLM-only in the benchmark notes |
| `spring` | Virtual token embedding file and HF backend | Do not run with unsupported generator families |
| `adaptive` | Query classifier checkpoint | Public notes indicate classifier may be non-official |
| `rqrag`, `r1searcher` | Dedicated generator/checkpoint | Treat as separate model-family setup |

Use the bundled `method_dependency_matrix.py` script for a machine-readable reminder.
