# Custom CrossEncoder Models

Read this for custom module chains, causal-LM rerankers, `LogitScore`, and saved CrossEncoder layouts.

## Standard Patterns

### Encoder / Sequence Classification

Traditional BERT/RoBERTa-style rerankers use one `Transformer` module with `transformer_task="sequence-classification"`. They output classification or regression scores for the pair.

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
```

When starting from a generic encoder:

```python
model = CrossEncoder("google-bert/bert-base-uncased", num_labels=1)
```

### CausalLM / Text Generation + LogitScore

Causal-LM rerankers use:

1. `Transformer` with `transformer_task="text-generation"` to output causal logits.
2. `LogitScore` to compute a scalar from true/false token logits.

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder("Qwen/Qwen3-Reranker-0.6B")
```

If `true_token_id` and `false_token_id` are both set, `LogitScore` computes a log-odds style score: true logit minus false logit.

## Custom True/False Tokens

```python
from sentence_transformers import CrossEncoder
from sentence_transformers.cross_encoder.modules import LogitScore, Transformer

transformer = Transformer("Qwen/Qwen3-Reranker-0.6B", transformer_task="text-generation")
true_id = transformer.tokenizer.convert_tokens_to_ids("1")
false_id = transformer.tokenizer.convert_tokens_to_ids("0")
model = CrossEncoder(modules=[transformer, LogitScore(true_token_id=true_id, false_token_id=false_id)])
```

Verify tokenization before assuming a string maps to one token. Some tokenizers treat leading spaces differently.

## Feature Extraction + Pooling + Dense

For a lighter causal-LM-style scorer, use a base model without the language-model head, last-token pooling, and a dense score head:

```python
from sentence_transformers import CrossEncoder
from sentence_transformers.cross_encoder.modules import Dense, Transformer
from sentence_transformers.sentence_transformer.modules import Pooling

transformer = Transformer("Qwen/Qwen3.5-0.8B", transformer_task="feature-extraction")
pooling = Pooling(transformer.get_embedding_dimension(), pooling_mode="lasttoken")
dense = Dense(transformer.get_embedding_dimension(), 1, activation_function=None, module_output_name="scores")
model = CrossEncoder(modules=[transformer, pooling, dense])
```

This pattern avoids computing a full-vocabulary LM head for every pair.

## Saved Model Layout

`save_pretrained` writes:

- `modules.json`
- `config_sentence_transformers.json`
- module folders such as `1_LogitScore/`
- tokenizer/config/model weight files
- `README.md` model card when enabled

For causal-LM rerankers, inspect `1_LogitScore/config.json` for `true_token_id`, `false_token_id`, and `module_input_name`.

## Prompt And Message Formats

Causal-LM or multimodal rerankers may store prompts and message-format metadata. The message format may be:

- `structured`: content is a list of typed dictionaries.
- `flat`: content is the direct value.

Let the model processor/chat template handle formatting when possible. Avoid manually concatenating multimodal prompts unless the model card requires it.
