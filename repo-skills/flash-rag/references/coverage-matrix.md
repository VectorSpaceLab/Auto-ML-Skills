# Coverage Matrix

This matrix maps FlashRAG user-facing capabilities to generated sub-skills.

| Capability | Sub-skill | Depth check |
| --- | --- | --- |
| SelfRAG, FLARE, SelfAsk, IRCOT, and RQ-RAG active retrieval workflows. | `sub-skills/flashrag-active-rag-pipeline-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| BM25s lexical index building and search without dense models. | `sub-skills/flashrag-bm25-retrieval-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Conditional and adaptive pipeline routing by judger decisions. | `sub-skills/flashrag-conditional-pipeline-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Corpus chunking and long-document passage preparation. | `sub-skills/flashrag-corpus-chunking-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Offline metric evaluation on saved predictions and dataset splits. | `sub-skills/flashrag-dataset-eval-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Dense retrieval, embedding index command generation, and search inspection. | `sub-skills/flashrag-dense-retrieval-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| HF/vLLM/FastChat/OpenAI-compatible generator config and fake generation smoke. | `sub-skills/flashrag-generator-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Iterative multi-round retrieval-generation pipeline smoke. | `sub-skills/flashrag-iterative-pipeline-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| SKR and adaptive judger data validation and fake route checks. | `sub-skills/flashrag-judger-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| KG-Trace triple extraction and evidence-chain context smoke workflows. | `sub-skills/flashrag-kg-trace-refiner-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Named methods from FlashRAG examples, including naive, zero-shot, SKR, TRACE, reasoning, and refiner variants. | `sub-skills/flashrag-methods-runner-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| BM25+dense/CLIP multi-retriever configuration and merge settings. | `sub-skills/flashrag-multi-retriever-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| CLIP/openai-clip/chinese-clip multimodal index preflight and smoke tests. | `sub-skills/flashrag-multimodal-index-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| MMSequentialPipeline and multimodal no-retrieval/RAG smoke workflows. | `sub-skills/flashrag-multimodal-pipeline-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Multi-turn generator prompt rendering and conversation smoke tests. | `sub-skills/flashrag-multiturn-generator-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| RAG prompt rendering and LLMLingua/SelectiveContext/RECOMP-style refiner checks. | `sub-skills/flashrag-prompt-refiner-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Reasoning-search pipelines such as SimpleDeepSearcher, SearchR1, AutoRefine, O2Searcher, ReaRAG, and CoRAG. | `sub-skills/flashrag-reasoning-pipeline-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| REPLUG document-score weighted generation workflows. | `sub-skills/flashrag-replug-pipeline-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Reranker configuration, offline rerank checks, and reranked-output inspection. | `sub-skills/flashrag-reranker-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Sequential retrieve-generate-evaluate RAG pipeline smoke and real-run transition. | `sub-skills/flashrag-sequential-pipeline-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| SuRe candidate, summary, validation, ranking, and final-answer pipeline smoke. | `sub-skills/flashrag-sure-pipeline-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| FlashRAG WebUI launch, health check, and shutdown. | `sub-skills/flashrag-webui-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
