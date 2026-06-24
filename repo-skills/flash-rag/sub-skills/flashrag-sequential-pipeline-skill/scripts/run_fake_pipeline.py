#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import load_jsonl, read_simple_yaml


class FakePromptTemplate:
    def format_reference(self, retrieval_result: list[dict[str, Any]]) -> str:
        chunks: list[str] = []
        for idx, doc in enumerate(retrieval_result, start=1):
            contents = str(doc.get("contents", ""))
            title = contents.splitlines()[0] if contents else str(doc.get("title", "Doc"))
            text = "\n".join(contents.splitlines()[1:]) if "\n" in contents else contents
            chunks.append(f"Doc {idx}(Title: {title}) {text}")
        return "\n".join(chunks)

    def get_string(self, question=None, retrieval_result=None, formatted_reference=None, **_: Any) -> str:
        if formatted_reference is None:
            formatted_reference = self.format_reference(retrieval_result or [])
        return (
            "Answer the question based on the given document. Only give the answer.\n\n"
            f"{formatted_reference}\n\n"
            f"Question: {question}\nAnswer:"
        )


class FakeRetriever:
    def __init__(self, answers_by_question: dict[str, str], topk: int):
        self.answers_by_question = answers_by_question
        self.topk = topk

    def batch_search(self, query, num=None, return_score=False):
        if isinstance(query, str):
            query = [query]
        k = num or self.topk
        all_docs = []
        all_scores = []
        for idx, question in enumerate(query):
            answer = self.answers_by_question.get(question, "")
            docs = [
                {
                    "id": f"fake-{idx}-{rank}",
                    "title": f"Synthetic evidence {rank}",
                    "contents": f"Synthetic evidence {rank}\nThe answer to {question} is {answer}.",
                }
                for rank in range(1, k + 1)
            ]
            all_docs.append(docs)
            all_scores.append([1.0 / rank for rank in range(1, k + 1)])
        if return_score:
            return all_docs, all_scores
        return all_docs

    def _save_cache(self):
        return None


class FakeGenerator:
    def __init__(self, answers_by_question: dict[str, str], fallback: str = ""):
        self.answers_by_question = answers_by_question
        self.fallback = fallback

    def generate(self, prompts):
        outputs: list[str] = []
        for prompt in prompts:
            text = "\n".join(prompt) if isinstance(prompt, list) else str(prompt)
            match = re.search(r"Question:\s*(.*?)\nAnswer:", text, flags=re.DOTALL)
            question = match.group(1).strip() if match else ""
            outputs.append(self.answers_by_question.get(question, self.fallback))
        return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--summary", type=Path, default=None)
    parser.add_argument("--no-eval", action="store_true")
    args = parser.parse_args()

    try:
        from flashrag.config import Config
        from flashrag.utils import get_dataset

        # Loading the file directly avoids package-level imports from
        # flashrag.pipeline.__init__, which pulls in optional reasoning pipelines.
        import flashrag

        pipeline_path = Path(flashrag.__file__).resolve().parent / "pipeline" / "pipeline.py"
        spec = importlib.util.spec_from_file_location("_flashrag_pipeline_core", pipeline_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load {pipeline_path}")
        pipeline_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pipeline_module)
        SequentialPipeline = pipeline_module.SequentialPipeline

        config = Config(str(args.config))
        split_map = get_dataset(config)
        dataset = split_map.get(args.split)
        if dataset is None:
            raise FileNotFoundError(f"split not loaded: {args.split}")

        answers_by_question = {
            question: (answers[0] if answers else "")
            for question, answers in zip(dataset.question, dataset.golden_answers)
        }
        pipeline = SequentialPipeline(
            config,
            prompt_template=FakePromptTemplate(),
            retriever=FakeRetriever(answers_by_question, config["retrieval_topk"]),
            generator=FakeGenerator(answers_by_question),
        )
        output_dataset = pipeline.run(dataset, do_eval=not args.no_eval)
        payload = {
            "mode": "flashrag-package",
            "records": len(output_dataset),
            "save_dir": config["save_dir"],
            "first_question": output_dataset.question[0] if len(output_dataset) else None,
            "first_pred": output_dataset.pred[0] if len(output_dataset) else None,
            "first_retrieved": len(output_dataset.retrieval_result[0]) if len(output_dataset) else 0,
        }
    except ModuleNotFoundError as exc:
        if exc.name != "flashrag":
            raise
        config = read_simple_yaml(args.config)
        data_path = Path(str(config["data_dir"])) / str(config["dataset_name"]) / f"{args.split}.jsonl"
        rows = load_jsonl(data_path)
        topk = int(config.get("retrieval_topk") or 2)
        records = []
        for idx, row in enumerate(rows):
            question = str(row.get("question", ""))
            answers = row.get("golden_answers") or [""]
            answer = str(answers[0])
            docs = [
                {
                    "id": f"offline-{idx}-{rank}",
                    "title": f"Synthetic evidence {rank}",
                    "contents": f"Synthetic evidence {rank}\nThe answer to {question} is {answer}.",
                    "score": 1.0 / rank,
                }
                for rank in range(1, topk + 1)
            ]
            prompt = FakePromptTemplate().get_string(question=question, retrieval_result=docs)
            records.append({"question": question, "retrieval_result": docs, "prompt": prompt, "pred": answer})
        payload = {
            "mode": "self-contained-fallback",
            "records": len(records),
            "save_dir": config.get("save_dir"),
            "first_question": records[0]["question"] if records else None,
            "first_pred": records[0]["pred"] if records else None,
            "first_retrieved": len(records[0]["retrieval_result"]) if records else 0,
            "items": records,
        }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
