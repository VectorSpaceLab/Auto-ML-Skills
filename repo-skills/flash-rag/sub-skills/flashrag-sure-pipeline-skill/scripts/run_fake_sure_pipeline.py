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
    def get_string(self, question=None, formatted_reference=None, **params: Any) -> str:
        text = formatted_reference or params.get("reference", "")
        if "pred" in params and "summary" in params:
            return f"VALIDATE\nQuestion: {question}\nPrediction: {params['pred']}\nPassage: {params['summary']}\nAnswer:"
        if "summary1" in params and "summary2" in params:
            return f"RANK\nQuestion: {question}\nPassage 1: {params['summary1']}\nPassage 2: {params['summary2']}\nAnswer:"
        if "pred" in params:
            return f"SUMMARIZE\nQuestion: {question}\nPrediction: {params['pred']}\nReference:\n{text}\nPassage:"
        return f"CANDIDATES\nQuestion: {question}\nReference:\n{text}\nAnswer:"


class FakeRetriever:
    def __init__(self, answers_by_question: dict[str, str], topk: int):
        self.answers_by_question = answers_by_question
        self.topk = topk

    def batch_search(self, query, num=None, return_score=False):
        queries = [query] if isinstance(query, str) else list(query)
        k = num or self.topk
        all_docs = []
        all_scores = []
        for idx, question in enumerate(queries):
            answer = self.answers_by_question.get(question, "")
            docs = [
                {
                    "id": f"sure-{idx}-{rank}",
                    "title": f"SuRe evidence {rank}",
                    "contents": f"SuRe evidence {rank}\nThe supported answer for {question} is {answer}.",
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

    @staticmethod
    def _flatten_prompt(prompt: Any) -> str:
        if isinstance(prompt, str):
            return prompt
        if isinstance(prompt, dict):
            return str(prompt.get("content", prompt))
        if isinstance(prompt, list):
            return "\n".join(FakeGenerator._flatten_prompt(item) for item in prompt)
        return str(prompt)

    @staticmethod
    def _extract_question(prompt: str) -> str:
        match = re.search(r"Question:\s*(.*?)(?:\n|$)", prompt)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_prediction(prompt: str) -> str:
        match = re.search(r"Prediction:\s*(.*?)(?:\n|$)", prompt)
        return match.group(1).strip() if match else ""

    def generate(self, prompts, **_: Any):
        prompt_list = [prompts] if isinstance(prompts, str) else list(prompts)
        outputs = []
        for prompt in prompt_list:
            text = self._flatten_prompt(prompt)
            question = self._extract_question(text)
            answer = self.answers_by_question.get(question, "")
            if "provide two correct candidates" in text or text.startswith("CANDIDATES"):
                outputs.append(f"(a) {answer}, (b) distractor")
            elif "Prediction:" in text and "Passage:" in text and "Does the passage correctly support" not in text:
                pred = self._extract_prediction(text)
                if pred == answer:
                    outputs.append(f"The passages support {pred} as the answer.")
                else:
                    outputs.append(f"The passages do not support {pred}.")
            elif "Does the passage correctly support" in text or text.startswith("VALIDATE"):
                pred = self._extract_prediction(text)
                outputs.append("True" if pred == answer else "False")
            elif "Passage 1:" in text and "Passage 2:" in text:
                passage1 = re.search(r"Passage 1:\s*(.*?)\nPassage 2:", text, flags=re.DOTALL)
                p1 = passage1.group(1) if passage1 else ""
                outputs.append("Passage 1" if "support" in p1 and "do not support" not in p1 else "Passage 2")
            else:
                outputs.append(answer)
        return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
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
    branching = load_module("_flashrag_branching_pipeline_core", package_root / "pipeline" / "branching_pipeline.py")
    SuRePipeline = branching.SuRePipeline

    config = Config(str(args.config))
    dataset_path = Path(config["dataset_path"]) / f"{args.split}.jsonl"
    if not dataset_path.is_file():
        raise FileNotFoundError(dataset_path)
    dataset = Dataset(config, str(dataset_path), sample_num=config["test_sample_num"], random_sample=config["random_sample"])

    answers_by_question = {
        question: (answers[0] if answers else "")
        for question, answers in zip(dataset.question, dataset.golden_answers)
    }
    pipeline = SuRePipeline(
        config,
        prompt_template=FakePromptTemplate(),
        retriever=FakeRetriever(answers_by_question, config["retrieval_topk"]),
        generator=FakeGenerator(answers_by_question),
    )
    output_dataset = pipeline.run(dataset, do_eval=True)
    payload = {
        "records": len(output_dataset),
        "save_dir": config["save_dir"],
        "first_question": output_dataset.question[0] if len(output_dataset) else None,
        "first_pred": output_dataset.pred[0] if len(output_dataset) else None,
        "first_candidates": output_dataset.candidates[0] if len(output_dataset) else [],
        "first_val_scores": output_dataset.val_scores[0] if len(output_dataset) else [],
        "first_ranking_scores": output_dataset.ranking_scores[0] if len(output_dataset) else [],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
