# Benchmark Reproduction Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Scores differ substantially from expected | Corpus, split, sample count, prompt, or model version drift | Compare the result alignment checklist before debugging code |
| Method crashes on missing model path | Method-specific extra asset not configured | Run the dependency matrix script for that method |
| Retriever returns empty docs | Index/corpus mismatch or wrong index path | Rebuild index from the same corpus and retriever |
| vLLM-only method fails under HF | Backend mismatch | Switch backend or choose a method supported by HF |
| Compression/refiner method produces odd prompts | Refiner model or compression target mismatch | Inspect rendered prompts before scoring |

Always run a tiny sample first. Reproduction workflows have many external assets and should fail fast before consuming GPU hours.
