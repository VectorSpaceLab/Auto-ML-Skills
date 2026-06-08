# Troubleshooting

Read this when installation, imports, model loading, backend export, scoring, or migration behavior is confusing.

## Fast Environment Check

Run the bundled diagnostic:

```bash
python skills/sentence-transformers/scripts/check_sentence_transformers_env.py
```

Or run the essential import check manually:

```bash
python - <<'PY'
import sentence_transformers
from sentence_transformers import SentenceTransformer, CrossEncoder, SparseEncoder
print(sentence_transformers.__version__)
print(SentenceTransformer.__name__, CrossEncoder.__name__, SparseEncoder.__name__)
PY
```

## Install And Import Symptoms

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError: sentence_transformers` | package missing from current Python | Install with `pip install -U sentence-transformers`; verify `python -m pip show sentence-transformers` in the same interpreter. |
| import fails inside `transformers`, `tokenizers`, `torch`, `scipy`, or `sklearn` | mixed or incompatible environment | Use a clean Python 3.10+ env and reinstall; run `python -m pip check`. |
| multimodal import/input fails | missing extra or decoder package | Install `[image]`, `[audio]`, `[video]`, or `torchcodec` as required by the input type. |
| training imports fail | missing training extras | Install `pip install -U "sentence-transformers[train]"` plus optional tracker packages. |
| ONNX/OpenVINO backend cannot load | missing backend extra | Install `[onnx]`, `[onnx-gpu]`, or `[openvino]`. |

## Model Download And Hub Symptoms

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| private/gated model cannot download | missing Hub token or approval | Authenticate with `huggingface-cli login`, set `HF_TOKEN`, or pass `token=...`. |
| offline deployment fails | model files are not cached locally | Download once, save with `save_pretrained`, then load from that local directory with `local_files_only=True`. |
| custom model errors or asks for remote code | model requires custom code | Only pass `trust_remote_code=True` for repositories you trust and pin `revision`. |

## Retrieval And Scoring Issues

| Symptom | Cause | Fix |
| --- | --- | --- |
| asymmetric search performs poorly | query/doc prompts not used or wrong model family | Use retrieval-tuned models plus `encode_query` and `encode_document`. |
| cosine scores are low but ranking looks right | model trained for dot product or unnormalized embeddings | Use the model's recommended score function; for normalized embeddings dot product and cosine align. |
| CrossEncoder scores are outside 0-1 | MS MARCO and some rerankers emit logits | Ranking is still valid; for 0-1 scores load with `activation_fn=torch.nn.Sigmoid()`. |
| CrossEncoder is too slow | scoring too many pairs | First retrieve top-k with dense/sparse/BM25, then rerank only candidates. |
| `semantic_search` runs out of memory | chunks too large or corpus too large | Lower `query_chunk_size` and `corpus_chunk_size`, or switch to ANN/vector DB. |
| sparse search returns dense-looking tensors | sparse encoding conversion disabled | Use `convert_to_sparse_tensor=True` where supported and check `SparseEncoder.sparsity`. |

## Backend And Performance Issues

| Symptom | Cause | Fix |
| --- | --- | --- |
| CPU inference is too slow | using default PyTorch backend | Try ONNX dynamic quantization, OpenVINO, smaller model, output quantization, or Matryoshka truncation. |
| GPU inference is slower than expected | fp32, small batches, padding overhead, CPU tensors | Increase batch size, use fp16/bf16 on supported GPUs, keep tensors on GPU, consider flash attention. |
| ONNX export repeats on every run | exported model was not saved | Call `model.save_pretrained(...)` after loading with `backend="onnx"`. |
| ONNX outputs differ outside Sentence Transformers | pooling/normalization missing | ONNX export converts the Transformer component; apply the same pooling and normalization if using raw ONNX outside the package. |
| OpenVINO static quantization requires data | calibration dataset missing | Provide dataset name/split/column or use dynamic ONNX quantization instead. |

## Migration Symptoms

| Symptom | Fix |
| --- | --- |
| deprecation warning for `sentence_transformers.losses` | import from `sentence_transformers.sentence_transformer.losses`. |
| warning for `tokenizer_kwargs` | rename to `processor_kwargs`. |
| warning for trainer `tokenizer` | rename to `processing_class`. |
| custom CrossEncoder loss expects tuple/model output | update for `model(... )["scores"]` and optional `prompt`/`task` kwargs. |
| positional CrossEncoder constructor arguments warn | use keyword arguments such as `num_labels=`, `max_length=`, `activation_fn=`, `device=`. |

## Reproducible Debug Bundle

When reporting or investigating an issue, collect:

```bash
python -m pip check
python -m pip show sentence-transformers torch transformers huggingface-hub
python skills/sentence-transformers/scripts/check_sentence_transformers_env.py
```

For backend issues, also include the model id, backend (`torch`, `onnx`, `openvino`), `model_kwargs`, device, and whether the model was loaded from Hub or a local directory.
