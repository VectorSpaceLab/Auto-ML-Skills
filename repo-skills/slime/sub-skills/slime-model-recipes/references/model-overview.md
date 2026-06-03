# Model Recipe Overview

slime uses explicit Megatron architecture arguments for conversion and training. This skill bundles verified static recipes extracted from public slime model argument blocks, so ordinary command generation does not need the original source checkout.

## Bundled Recipes

Run:

```bash
python /path/to/skill/slime/scripts/inspect_model_recipe.py --list
```

Bundled recipe names:

```text
deepseek-v3
deepseek-v3-20layer
deepseek-v3-5layer
glm4-32b
glm4-9b
glm4.5-106b-a12b
glm4.5-355b-a32b
glm4.7-30b-a3b
glm5-744b-a40b
gpt-oss-20b
kimi-k2
kimi-k2-thinking
llama3.1-8b-instruct
llama3.2-3b-instruct
llama3.2-3b-instruct-amd
mimo-7b-rl
minimax-m2
moonlight
qwen2.5-0.5b
qwen2.5-1.5b
qwen2.5-32b
qwen2.5-3b
qwen2.5-7b
qwen3-0.6b
qwen3-1.7b
qwen3-14b
qwen3-235b-a22b
qwen3-30b-a3b
qwen3-32b
qwen3-4b
qwen3-4b-instruct-2507
qwen3-8b
qwen3-next-80b-a3b
qwen3.5-0.8b
qwen3.5-27b
qwen3.5-35b-a3b
qwen3.5-4b
```

For an unlisted exact variant, start from the closest family recipe, compare against the Hugging Face `config.json`, and explicitly override differences. Do not silently reuse a near recipe when layer count, vocabulary size, RoPE settings, GQA groups, MoE experts, MLA fields, or plugin `--spec` differ.

## Fields To Match Exactly

- `--num-layers`
- `--hidden-size`
- `--ffn-hidden-size`
- `--num-attention-heads`
- `--group-query-attention`
- `--num-query-groups`
- `--kv-channels`
- `--normalization`
- `--norm-epsilon`
- `--rotary-base`
- `--vocab-size`
- Model plugin `--spec` when the architecture is not plain Qwen/Llama-style.

## Plugin Examples

Several families need plugin specs. Examples include:

```bash
--spec slime_plugins.models.glm4 get_glm_spec
--spec slime_plugins.models.qwen3_5 get_qwen3_5_spec
--spec slime_plugins.models.qwen3_next get_qwen3_next_spec
--spec slime_plugins.models.gpt_oss get_gpt_oss_spec
--spec slime_plugins.models.minimax_m2 get_minimax_m2_layer_spec
```

If the plugin import fails, check that `slime_plugins` is installed with the same public slime package version used by the training environment.

## MoE And Parallelism

Recipe model args are not enough for MoE training. Combine with training parallel flags:

```bash
--expert-model-parallel-size <ep>
--expert-tensor-parallel-size <etp>
```

Some large EP inference jobs also need SGLang flags such as `--sglang-ep-size`, `--sglang-enable-dp-attention`, or DeepEP-related settings.
