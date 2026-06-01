# CrossEncoder Troubleshooting

## Scores Are Outside 0 To 1

This is normal for many rerankers, especially MS MARCO models. They return raw logits or ranking scores.

Use sigmoid only if the user needs probability-like binary scores:

```python
import torch
scores = model.predict(pairs, activation_fn=torch.nn.Sigmoid())
```

For ranking, raw logits are fine because monotonic activation does not change order.

## Pair Formatting Errors

`predict` expects one pair or a list of pairs:

```python
model.predict([("query", "document")])
```

For `rank`, pass one query and a list of documents:

```python
model.rank("query", ["doc 1", "doc 2"])
```

Do not pass a list of queries to `rank` unless you loop over queries yourself.

## Reranking Is Too Slow

Reduce candidate count, batch size, or model size. Use first-stage retrieval first. Consider ONNX/OpenVINO backends for repeated inference.

If the user is scoring a whole corpus with a Cross Encoder, redesign as retrieve-and-rerank.

## Classification Probabilities Look Wrong

For multi-class models, use `apply_softmax=True`. For binary single-logit models, use sigmoid. For raw reranking logits, do not expect calibrated probabilities.

## Model Has Wrong Number Of Outputs

When starting from a generic Transformers checkpoint, set `num_labels` to match the task:

- `num_labels=1` for reranking/regression/binary relevance score.
- `num_labels=N` for N-way classification.

Training loss and evaluator must match the output shape.

## Multimodal Inputs Fail

Install the matching extra and verify support:

```python
print(model.modalities)
print(model.supports(("image", "text")))
```

If support is false, choose a multimodal Cross Encoder model. Extras do not add modalities to a text-only checkpoint.

## Backend Output Differs Slightly

ONNX/OpenVINO outputs can differ slightly from PyTorch because of export, precision, and activation handling. For Cross Encoders used outside Sentence Transformers, apply the same activation function manually if needed.
