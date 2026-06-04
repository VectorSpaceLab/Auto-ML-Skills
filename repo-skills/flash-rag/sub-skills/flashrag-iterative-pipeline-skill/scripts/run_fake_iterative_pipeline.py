#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

from offline_import_stubs import install_offline_import_stubs


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakePromptTemplate:
    def format_reference(self, retrieval_result: list[dict[str, Any]]) -> str:
        chunks = []
        for idx, doc in enumerate(retrieval_result, start=1):
            contents = str(doc.get("contents", ""))
            title = contents.splitlines()[0] if contents else str(doc.get("title", "Doc"))
            text = "\n".join(contents.splitlines()[1:]) if "\n" in contents else contents
            chunks.append(f"Doc {idx}(Title: {title}) {text}")
        return "\n".join(chunks)

    def get_string(self, question=None, retrieval_result=None, **_: Any) -> str:
        reference = self.format_reference(retrieval_result or [])
        return f"Use the evidence to answer.\n{reference}\nQuestion: {question}\nAnswer:"


class FakeRetriever:
    def __init__(self, answers_by_question: dict[str, str], topk: int):
        self.answers_by_question = answers_by_question
        self.topk = topk
        self.queries: list[str] = []

    def batch_search(self, query, num=None, return_score=False):
        queries = [query] if isinstance(query, str) else list(query)
        self.queries.extend(queries)
        k = num or self.topk
        all_docs = []
        all_scores = []
        for idx, item_query in enumerate(queries):
            base_question = item_query.split(" The answer is ")[0].strip()
            answer = self.answers_by_question.get(base_question, "")
            if not answer:
                for known_question, known_answer in self.answers_by_question.items():
                    if known_question in item_query:
                        answer = known_answer
                        break
            docs = [
                {
                    "id": f"iter-{idx}-{rank}",
                    "title": f"Iterative evidence {rank}",
                    "contents": f"Iterative evidence {rank}\nThe answer is {answer}. Query seen: {item_query}",
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
    def __init__(self, answers_by_question: dict[str, str]):
        self.answers_by_question = answers_by_question

    def generate(self, prompts, **_: Any):
        prompt_list = [prompts] if isinstance(prompts, str) else list(prompts)
        outputs = []
        for prompt in prompt_list:
            text = "\n".join(prompt) if isinstance(prompt, list) else str(prompt)
            match = re.search(r"Question:\s*(.*?)\nAnswer:", text, flags=re.DOTALL)
            question = match.group(1).strip() if match else ""
            outputs.append(self.answers_by_question.get(question, ""))
        return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--iter-num", type=int, default=None)
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args()

    import flashrag
    package_root = Path(flashrag.__file__).resolve().parent
    install_offline_import_stubs()
    from flashrag.config import Config
    from flashrag.dataset import Dataset

    core = load_module("_flashrag_pipeline_core", package_root / "pipeline" / "pipeline.py")
    fake_pkg = type(sys)("flashrag.pipeline")
    fake_pkg.BasicPipeline = core.BasicPipeline
    sys.modules["flashrag.pipeline"] = fake_pkg
    active = load_module("_flashrag_active_pipeline_core", package_root / "pipeline" / "active_pipeline.py")
    IterativePipeline = active.IterativePipeline

    config = Config(str(args.config))
    dataset_path = Path(config["dataset_path"]) / f"{args.split}.jsonl"
    if not dataset_path.is_file():
        raise FileNotFoundError(dataset_path)
    dataset = Dataset(config, str(dataset_path), sample_num=config["test_sample_num"], random_sample=config["random_sample"])

    answers_by_question = {
        question: (answers[0] if answers else "")
        for question, answers in zip(dataset.question, dataset.golden_answers)
    }
    iter_num = args.iter_num if args.iter_num is not None else (config["iter_num"] or 2)
    retriever = FakeRetriever(answers_by_question, config["retrieval_topk"])
    pipeline = IterativePipeline(
        config,
        prompt_template=FakePromptTemplate(),
        iter_num=int(iter_num),
        retriever=retriever,
        generator=FakeGenerator(answers_by_question),
    )
    output_dataset = pipeline.run(dataset, do_eval=True)
    payload = {
        "records": len(output_dataset),
        "iter_num": int(iter_num),
        "save_dir": config["save_dir"],
        "first_question": output_dataset.question[0] if len(output_dataset) else None,
        "first_pred": output_dataset.pred[0] if len(output_dataset) else None,
        "retriever_queries": retriever.queries[: min(6, len(retriever.queries))],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
