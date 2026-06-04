#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import write_yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--save-dir", required=True)
    parser.add_argument("--mode", choices=["no-ret", "rag"], default="no-ret")
    parser.add_argument("--generator-model", default="qwen2-vl-2B")
    parser.add_argument("--sample-num", type=int, default=3)
    parser.add_argument("--bm25-corpus", default=None)
    parser.add_argument("--bm25-index", default=None)
    parser.add_argument("--clip-method", default="openai-clip")
    parser.add_argument("--clip-corpus", default=None)
    parser.add_argument("--clip-image-index", default=None)
    parser.add_argument("--clip-text-index", default=None)
    parser.add_argument("--bm25-topk", type=int, default=1)
    parser.add_argument("--clip-topk", type=int, default=1)
    parser.add_argument("--perform-modality", default="text,image")
    args = parser.parse_args()

    cfg = {
        "gpu_id": None,
        "dataset_name": args.dataset_name,
        "split": [args.split],
        "test_sample_num": args.sample_num,
        "random_sample": False,
        "save_intermediate_data": True,
        "save_metric_score": True,
        "data_dir": args.data_dir,
        "save_dir": args.save_dir,
        "save_note": f"mm-{args.mode}",
        "disable_save": False,
        "framework": "hf",
        "generator_model": args.generator_model,
        "generator_model_path": None,
        "generation_params": {"max_new_tokens": 128},
        "generator_max_input_len": 4096,
        "generator_batch_size": 1,
        "retrieval_topk": max(args.bm25_topk, args.clip_topk),
        "metrics": ["acc", "f1", "em"],
        "metric_setting": {"tokenizer_name": "gpt-4", "retrieval_recall_topk": 1},
        "mode": args.mode,
        "perform_modality": [x.strip() for x in args.perform_modality.split(",") if x.strip()],
        "use_multi_retriever": args.mode == "rag",
        "refiner_name": None,
    }
    if args.mode == "rag":
        retrievers = [
            {
                "retrieval_method": "bm25",
                "corpus_path": args.bm25_corpus,
                "index_path": args.bm25_index,
                "retrieval_topk": args.bm25_topk,
                "bm25_backend": "bm25s",
            }
        ]
        if args.clip_image_index or args.clip_text_index:
            retrievers.append(
                {
                    "retrieval_method": args.clip_method,
                    "corpus_path": args.clip_corpus,
                    "multimodal_index_path_dict": {
                        "image": args.clip_image_index,
                        "text": args.clip_text_index,
                    },
                    "retrieval_topk": args.clip_topk,
                }
            )
        cfg["multi_retriever_setting"] = {"merge_method": "concat", "retriever_list": retrievers}
    write_yaml(args.output, cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
