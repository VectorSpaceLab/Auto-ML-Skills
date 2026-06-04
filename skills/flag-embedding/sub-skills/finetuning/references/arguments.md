# Fine-Tuning Arguments

Read this for the important FlagEmbedding fine-tuning argument groups. The training modules use Hugging Face `HfArgumentParser`, so standard `transformers.TrainingArguments` flags also apply.

## Common Model Arguments

Embedders:

| Argument | Meaning |
| --- | --- |
| `--model_name_or_path` | Base checkpoint or local model path |
| `--config_name`, `--tokenizer_name` | Optional config/tokenizer override |
| `--cache_dir` | Model cache directory |
| `--trust_remote_code` | Allow remote model code when required |
| `--use_fast_tokenizer` | Use fast tokenizer |
| `--token` | Hugging Face token, if needed |

Rerankers add:

| Argument | Meaning |
| --- | --- |
| `--model_type` | `encoder` or `decoder` |

Decoder-only reranker and embedder workflows commonly add LoRA arguments:

| Argument | Meaning |
| --- | --- |
| `--use_lora` | Enable LoRA |
| `--lora_rank` | LoRA rank |
| `--lora_alpha` | LoRA alpha |
| `--lora_dropout` | LoRA dropout |
| `--target_modules` | Module names, e.g. `q_proj k_proj v_proj o_proj` |
| `--modules_to_save` | Modules to save outside adapters |
| `--use_flash_attn` | Enable flash attention |
| `--save_merged_lora_model` | Save merged model |

## Common Data Arguments

| Argument | Default | Meaning |
| --- | --- | --- |
| `--train_data` | `None` | One or more JSONL files or directories |
| `--cache_path` | `None` | Dataset cache path |
| `--train_group_size` | `8` | One positive plus negatives per query group |
| `--query_max_len` | `32` | Query token max length unless overridden |
| `--passage_max_len` | `128` | Passage token max length unless overridden |
| `--max_len` | `512` | Reranker combined sequence max length |
| `--pad_to_multiple_of` | `None` | Padding multiple, often `8` |
| `--max_example_num_per_dataset` | `100000000` | Per-dataset cap |
| `--knowledge_distillation` | `False` | Use `pos_scores` and `neg_scores` |
| `--shuffle_ratio` | `0.0` | Text shuffling ratio |

Embedder-specific:

| Argument | Meaning |
| --- | --- |
| `--query_instruction_for_retrieval` | Instruction added to queries |
| `--query_instruction_format` | Format string, often `{}` + `{}` or `<instruct>{}\n<query>{}` |
| `--passage_instruction_for_retrieval` | Optional passage instruction |
| `--passage_instruction_format` | Passage instruction format |
| `--same_dataset_within_batch` | Keep a batch within one dataset |
| `--small_threshold`, `--drop_threshold` | Merge/drop small datasets |

Reranker-specific:

| Argument | Meaning |
| --- | --- |
| `--query_instruction_for_rerank` | Query prefix/instruction |
| `--query_instruction_format` | Query instruction format |
| `--passage_instruction_for_rerank` | Passage prefix/instruction |
| `--passage_instruction_format` | Passage instruction format |
| `--sep_token` | Separator for LLM reranker inputs |

ICL embedder data arguments:

| Argument | Default | Meaning |
| --- | --- | --- |
| `--example_query_max_len` | `64` | Example query length |
| `--example_passage_max_len` | `96` | Example passage length |
| `--retrieval_use_examples` | `True` | Use examples for retrieval |
| `--icl_suffix_str` | `\nResponse:` | ICL suffix string |

## Important Training Arguments

FlagEmbedding extends `TrainingArguments` with:

| Argument | Default | Meaning |
| --- | --- | --- |
| `--negatives_cross_device` | `False` | Share negatives across devices |
| `--temperature` | `0.02` | Similarity temperature |
| `--fix_position_embedding` | `False` | Freeze position embeddings |
| `--sentence_pooling_method` | `cls` | `cls`, `mean`, or `last_token` |
| `--normalize_embeddings` | `True` | Normalize embeddings |
| `--sub_batch_size` | `None` | Sub-batch size |
| `--kd_loss_type` | `kl_div` | `kl_div` or `m3_kd_loss` |
| `--use_mrl` | `False` | Use Matryoshka Representation Learning |
| `--mrl_dims` | required if used | MRL layer dimensions |

M3 training adds:

| Argument | Meaning |
| --- | --- |
| `--unified_finetuning` | Train M3 multi-function modes together |
| `--use_self_distill` | Enable self distillation |
| `--fix_encoder` | Freeze encoder when configured |
| `--self_distill_start_step` | Start step for self distillation |

Use standard `TrainingArguments` flags such as `--output_dir`, `--overwrite_output_dir`, `--learning_rate`, `--num_train_epochs`, `--per_device_train_batch_size`, `--gradient_accumulation_steps`, `--fp16`, `--bf16`, `--gradient_checkpointing`, `--deepspeed`, `--logging_steps`, and `--save_steps`.
