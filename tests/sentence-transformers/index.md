# Sentence Transformers Usability Test Cases

These cases exercise the generated `sentence-transformers` repo skill across dense embeddings, reranking, sparse retrieval, training/evaluation, and optimization/deployment.

| Case | Skill area | User role | Scenario | Capability | Difficulty |
| --- | --- | --- | --- | --- | --- |
| `dense-embeddings-asymmetric-search` | dense-embeddings | developer | FAQ semantic search | `encode_query`, `encode_document`, `semantic_search` | basic |
| `dense-embeddings-multimodal-image-search` | dense-embeddings | product engineer | text-to-image retrieval | multimodal extras and modality checks | intermediate |
| `reranking-retrieve-and-rerank` | reranking | search engineer | BM25 candidate reranking | CrossEncoder rank with original id mapping | intermediate |
| `reranking-logit-score-debugging` | reranking | developer | unexpected score ranges | MS MARCO logits and sigmoid activation | troubleshooting |
| `sparse-retrieval-explain-hit` | sparse-retrieval | search developer | explain sparse hit | SPLADE search plus active token decoding | intermediate |
| `sparse-retrieval-qdrant-integration` | sparse-retrieval | backend engineer | repeated sparse vector DB queries | Qdrant helper and index reuse | advanced |
| `training-evaluation-dense-retriever-finetune` | training-evaluation | ML engineer | dense retriever fine-tune | MNRL, smoke test, IR evaluator | advanced |
| `training-evaluation-cross-encoder-reranker` | training-evaluation | ML practitioner | reranker training | BCE loss, reranking evaluator, early stopping | advanced |
| `optimization-deployment-onnx-export` | optimization-deployment | deployment engineer | CPU ONNX deployment | backend export, optimized filename loading | intermediate |
| `optimization-deployment-quantized-vectors` | optimization-deployment | search infrastructure engineer | storage reduction | output vector quantization | intermediate |

## Coverage Note

The case set covers every generated sub-skill and the major public capability groups identified in the coverage matrix: dense embedding/search, multimodal embeddings, CrossEncoder reranking and score troubleshooting, sparse search and sparse vector DB integration, dense/CrossEncoder training, ONNX deployment, and output vector quantization. Sparse training and OpenVINO static quantization are covered in references but not as dedicated test cases because they are advanced variants of the training and optimization routes.
