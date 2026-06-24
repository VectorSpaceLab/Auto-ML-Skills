# Coverage Matrix

This matrix maps LLaMA-Factory user-facing capabilities to generated sub-skills.

| Capability | Sub-skill | Depth check |
| --- | --- | --- |
| Standalone PiSSA or LoftQ adapter initialization before training. | `sub-skills/llamafactory-adapter-init-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| LoRA variants such as LoRA+, rsLoRA, DoRA, PiSSA, OFT, and adapter continuation. | `sub-skills/llamafactory-adapter-variants-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| OpenAI-compatible client payload tests, tool calls, and image messages. | `sub-skills/llamafactory-api-client-tests-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| FLOPs, MFU, length CDF, Qwen benchmark, and training-stat utilities. | `sub-skills/llamafactory-benchmark-stats-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| HF-DCP checkpoint conversion, Megatron/Qwen-Omni merge, and tiny/llamafy utilities. | `sub-skills/llamafactory-checkpoint-convert-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Dataset registration, dataset_info mappings, tokenized cache creation, and cache inspection. | `sub-skills/llamafactory-dataset-preprocess-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| torchrun, DeepSpeed, FSDP/FSDP2, Ray, and multi-node launch setup. | `sub-skills/llamafactory-distributed-train-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Ascend NPU SFT/QLoRA/full tuning with FSDP/FSDP2 and Qwen/Qwen-VL recipes. | `sub-skills/llamafactory-ascend-npu-skill` | routes NPU device selection, `use_v1_kernels`, FSDP/FSDP2 accelerate pairing, Qwen/Qwen-VL/MoE config generation, and NPU troubleshooting |
| KTransformers MoE LoRA training with FSDP2 and AMX BF16/INT8/INT4 expert backends. | `sub-skills/llamafactory-ktransformers-skill` | covers `use_kt`, `kt_config`, backend choice, expert weight paths, FSDP2 accelerate pairing, and config validation |
| Megatron-Core full-parameter training for Qwen-VL and Qwen MoE models. | `sub-skills/llamafactory-megatron-core-skill` | covers MCore parallelism keys, Qwen-VL media limits, Qwen MoE expert parallelism, and full-tuning caveats |
| Dynamic batching, padding-free training, Liger kernels, and Ulysses context parallel settings. | `sub-skills/llamafactory-batching-kernels-skill` | covers batching strategy selection, kernel compatibility, context parallel sizing, and generated config snippets |
| DPO / ORPO / SimPO / pairwise preference optimization. | `sub-skills/llamafactory-dpo-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| BLEU, ROUGE, perplexity, learning-rate, and score inspection utilities. | `sub-skills/llamafactory-eval-metrics-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| LoRA adapter export, merge, Modelfile generation, and exported artifact inspection. | `sub-skills/llamafactory-export-merge-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Freeze tuning and partial-parameter training. | `sub-skills/llamafactory-freeze-tuning-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Offline chat, one-shot inference, batch prediction, and adapter inference. | `sub-skills/llamafactory-inference-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| KTO training from binary desirable/undesirable feedback. | `sub-skills/llamafactory-kto-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Vision-language or multimodal SFT data validation and training configs. | `sub-skills/llamafactory-multimodal-sft-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| OpenAI-compatible API server launch, health check, and shutdown. | `sub-skills/llamafactory-openai-api-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| PPO / RLHF policy optimization that requires a reward model or reward API. | `sub-skills/llamafactory-ppo-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Continued pretraining / causal LM pretraining on raw text. | `sub-skills/llamafactory-pt-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| QLoRA and 4-bit or 8-bit LoRA training. | `sub-skills/llamafactory-qlora-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| Reward model training and pairwise preference scoring. | `sub-skills/llamafactory-rm-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| SFT / supervised fine-tuning / instruction tuning / chat fine-tuning. | `sub-skills/llamafactory-sft-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| GaLore, APOLLO, BAdam, Muon, Adam-mini, DFT/ASFT/EAFT, FP8, and profiler settings. | `sub-skills/llamafactory-training-extensions-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| vLLM batch inference using LLaMA-Factory prompt/data formats. | `sub-skills/llamafactory-vllm-batch-infer-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
| LLaMA-Factory WebUI / LlamaBoard launch and health checks. | `sub-skills/llamafactory-webui-skill` | workflow router, bundled references, troubleshooting, and scripts copied/adapted from the extracted skill |
