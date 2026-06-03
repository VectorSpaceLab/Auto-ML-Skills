# Checkpoint Conversion Troubleshooting

## Converted Checkpoint Produces Garbled Text

Check that the model recipe exactly matches the HF checkpoint. Same model family can still differ in `rotary-base`, vocab size, GQA groups, or plugin `--spec`.

## Training Cannot Resume

Use the checkpoint root for `--load`, not the iteration directory:

```bash
--load /checkpoints/model_slime
```

The root should contain `latest_checkpointed_iteration.txt`.

## HF Export Has Bad Embeddings

Megatron can pad embeddings for performance. Retry export with:

```bash
--vocab-size <original_vocab_size>
```

## Conversion Import Fails

Set `PYTHONPATH` to full Megatron-LM and run the root strict env check before conversion.
