# Evaluation Workflows

Read this for benchmark-specific FlagEmbedding evaluation command templates.

## MTEB

MTEB primarily evaluates embedders and uses the official MTEB package.

```bash
python -m pip install mteb==1.15.0
python -m FlagEmbedding.evaluation.mteb \
  --eval_name mteb \
  --output_dir ./mteb/search_results \
  --languages eng \
  --tasks NFCorpus BiorxivClusteringS2S SciDocsRR \
  --eval_output_path ./mteb/mteb_eval_results.json \
  --embedder_name_or_path BAAI/bge-m3 \
  --devices cuda:0 \
  --cache_dir ./cache/model
```

## BEIR

BEIR supports datasets such as `arguana`, `climate-fever`, `cqadupstack`, `dbpedia-entity`, `fever`, `fiqa`, `hotpotqa`, `msmarco`, `nfcorpus`, `nq`, `quora`, `scidocs`, `scifact`, `trec-covid`, and `webis-touche2020`.

```bash
python -m FlagEmbedding.evaluation.beir \
  --eval_name beir \
  --dataset_dir ./beir/data \
  --dataset_names fiqa arguana cqadupstack \
  --splits test dev \
  --corpus_embd_save_dir ./beir/corpus_embd \
  --output_dir ./beir/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --cache_path ./cache/data \
  --overwrite False \
  --k_values 10 100 \
  --eval_output_method markdown \
  --eval_output_path ./beir/beir_eval_results.md \
  --eval_metrics ndcg_at_10 recall_at_100 \
  --ignore_identical_ids True \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 cuda:1 \
  --cache_dir ./cache/model \
  --reranker_max_length 1024
```

## MSMARCO

MSMARCO supports `passage` and `document` with splits such as `dev`, `dl19`, and `dl20`.

```bash
python -m FlagEmbedding.evaluation.msmarco \
  --eval_name msmarco \
  --dataset_dir ./msmarco/data \
  --dataset_names passage \
  --splits dev dl19 dl20 \
  --corpus_embd_save_dir ./msmarco/corpus_embd \
  --output_dir ./msmarco/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --cache_path ./cache/data \
  --overwrite True \
  --k_values 10 100 \
  --eval_output_method markdown \
  --eval_output_path ./msmarco/msmarco_eval_results.md \
  --eval_metrics ndcg_at_10 recall_at_100 \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 cuda:1 \
  --cache_dir ./cache/model \
  --reranker_max_length 1024
```

## MIRACL

MIRACL dataset names are languages. Examples include `ar`, `bn`, `en`, `es`, `fa`, `fi`, `fr`, `hi`, `id`, `ja`, `ko`, `ru`, `sw`, `te`, `th`, `zh`, `de`, and `yo`.

```bash
python -m FlagEmbedding.evaluation.miracl \
  --eval_name miracl \
  --dataset_dir ./miracl/data \
  --dataset_names bn hi sw te th yo \
  --splits dev \
  --corpus_embd_save_dir ./miracl/corpus_embd \
  --output_dir ./miracl/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --cache_path ./cache/data \
  --overwrite False \
  --k_values 10 100 \
  --eval_output_method markdown \
  --eval_output_path ./miracl/miracl_eval_results.md \
  --eval_metrics ndcg_at_10 recall_at_100 \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 cuda:1 \
  --cache_dir ./cache/model \
  --reranker_max_length 1024
```

## MLDR

MLDR language names include `ar`, `de`, `en`, `es`, `fr`, `hi`, `it`, `ja`, `ko`, `pt`, `ru`, `th`, and `zh`. Splits include `train`, `dev`, and `test`.

```bash
python -m FlagEmbedding.evaluation.mldr \
  --eval_name mldr \
  --dataset_dir ./mldr/data \
  --dataset_names hi \
  --splits test \
  --corpus_embd_save_dir ./mldr/corpus_embd \
  --output_dir ./mldr/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --cache_path ./cache/data \
  --overwrite False \
  --k_values 10 100 \
  --eval_output_method markdown \
  --eval_output_path ./mldr/mldr_eval_results.md \
  --eval_metrics ndcg_at_10 \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 cuda:1 \
  --cache_dir ./cache/model \
  --embedder_passage_max_length 8192 \
  --reranker_max_length 8192
```

## MKQA

MKQA examples use language dataset names such as `en` and `zh_cn`, metric `qa_recall_at_20`, and `k_values 20`.

```bash
python -m FlagEmbedding.evaluation.mkqa \
  --eval_name mkqa \
  --dataset_dir ./mkqa/data \
  --dataset_names en zh_cn \
  --splits test \
  --corpus_embd_save_dir ./mkqa/corpus_embd \
  --output_dir ./mkqa/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --cache_path ./cache/data \
  --overwrite False \
  --k_values 20 \
  --eval_output_method markdown \
  --eval_output_path ./mkqa/mkqa_eval_results.md \
  --eval_metrics qa_recall_at_20 \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 cuda:1 \
  --cache_dir ./cache/model \
  --reranker_max_length 1024
```

## BRIGHT

BRIGHT has `short` and `long` task types. Example short datasets include `biology`, `earth_science`, `economics`, `psychology`, `robotics`, `stackoverflow`, `sustainable_living`, `leetcode`, `pony`, `aops`, `theoremqa_questions`, and `theoremqa_theorems`.

```bash
python -m FlagEmbedding.evaluation.bright \
  --task_type short \
  --use_special_instructions True \
  --eval_name bright_short \
  --dataset_dir ./bright_short/data \
  --dataset_names pony theoremqa_theorems \
  --splits examples \
  --corpus_embd_save_dir ./bright_short/corpus_embd \
  --output_dir ./bright_short/search_results/examples \
  --search_top_k 2000 \
  --cache_path ./cache/data \
  --overwrite False \
  --k_values 1 10 100 \
  --eval_output_method markdown \
  --eval_output_path ./bright_short/eval_results_examples.md \
  --eval_metrics ndcg_at_10 recall_at_10 recall_at_100 \
  --embedder_name_or_path BAAI/bge-reasoner-embed-qwen3-8b-0923 \
  --embedder_model_class decoder-only-base \
  --query_instruction_format_for_retrieval "Instruct: {}\nQuery: {}" \
  --pooling_method last_token \
  --devices cuda:0 \
  --cache_dir ./cache/model \
  --embedder_batch_size 2 \
  --embedder_query_max_length 8192 \
  --embedder_passage_max_length 8192
```

## AIR-Bench

AIR-Bench uses arguments from `air_benchmark`. Its module prints a reminder that leaderboard metrics are computed through AIR-Bench's official process after search results are generated.

```bash
python -m FlagEmbedding.evaluation.air_bench \
  --benchmark_version AIR-Bench_24.05 \
  --task_types qa long-doc \
  --domains arxiv \
  --languages en \
  --splits dev test \
  --output_dir ./air_bench/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --cache_dir ./cache/data \
  --overwrite False \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 cuda:1 \
  --model_cache_dir ./cache/model \
  --reranker_max_length 1024
```

## Custom Dataset

```bash
python -m FlagEmbedding.evaluation.custom \
  --eval_name custom \
  --dataset_dir ./my_eval_data \
  --dataset_names my_dataset \
  --splits test \
  --corpus_embd_save_dir ./custom/corpus_embd \
  --output_dir ./custom/search_results \
  --search_top_k 1000 \
  --rerank_top_k 100 \
  --overwrite False \
  --k_values 10 100 \
  --eval_output_method markdown \
  --eval_output_path ./custom/eval_results.md \
  --eval_metrics ndcg_at_10 recall_at_100 \
  --embedder_name_or_path BAAI/bge-m3 \
  --reranker_name_or_path BAAI/bge-reranker-v2-m3 \
  --devices cuda:0 \
  --cache_dir ./cache/model
```

Validate the custom dataset layout before running.
