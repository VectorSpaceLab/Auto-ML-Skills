#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from fr_skill_common import read_simple_yaml


class SimpleMMDataset:
    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows

    def __len__(self) -> int:
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    @property
    def question(self):
        return [row.get("question") for row in self.rows]

    @property
    def text(self):
        return [row.get("text") or row.get("question") for row in self.rows]

    @property
    def image(self):
        return [row.get("image") for row in self.rows]

    def update_output(self, key: str, values: list[Any]) -> None:
        assert len(values) == len(self.rows)
        for row, value in zip(self.rows, values):
            row.setdefault("output", {})[key] = value


class FakeMMPromptTemplate:
    def get_string(self, item: dict[str, Any]) -> str:
        docs = item.get("output", {}).get("retrieval_result", [])
        refs = "\n".join(str(doc.get("contents", "")) for doc in docs)
        question = item.get("question") or item.get("text", "")
        image = item.get("image")
        return f"Image: {image}\nReference:\n{refs}\nQuestion: {question}\nAnswer:"


class FakeMMRetriever:
    def __init__(self, topk: int):
        self.topk = topk

    def batch_search(self, queries, target_modal="text"):
        if isinstance(queries, str):
            queries = [queries]
        docs = []
        for idx, query in enumerate(queries):
            docs.append(
                [
                    {
                        "id": f"{target_modal}-{idx}-{rank}",
                        "title": f"{target_modal} evidence {rank}",
                        "contents": f"{target_modal} evidence {rank}\nEvidence for {query}.",
                    }
                    for rank in range(1, self.topk + 1)
                ]
            )
        return docs


class FakeMMGenerator:
    def generate(self, prompts):
        outputs = []
        for prompt in prompts:
            lines = [line for line in str(prompt).splitlines() if line.startswith("Question:")]
            question = lines[-1].split("Question:", 1)[1].strip() if lines else "unknown"
            outputs.append(f"fake multimodal answer for {question}")
        return outputs


def load_rows(path: Path, sample_num: int | None) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                row.setdefault("question", row.get("text", ""))
                row.setdefault("golden_answers", row.get("answers", []))
                rows.append(row)
    return rows[:sample_num] if sample_num else rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args()

    config = read_simple_yaml(args.config)
    dataset_path = Path(str(config["data_dir"])) / str(config["dataset_name"]) / f"{args.split}.jsonl"
    if not dataset_path.is_file():
        raise FileNotFoundError(dataset_path)
    dataset = SimpleMMDataset(load_rows(dataset_path, config.get("test_sample_num")))
    prompt_template = FakeMMPromptTemplate()
    generator = FakeMMGenerator()
    retriever = FakeMMRetriever(int(config.get("retrieval_topk") or 1))

    if config.get("mode") == "rag":
        retrieval_result = []
        text_docs = retriever.batch_search(dataset.text, target_modal="text")
        image_docs = retriever.batch_search(dataset.image, target_modal="image")
        for text_group, image_group in zip(text_docs, image_docs):
            retrieval_result.append(text_group + image_group)
        dataset.update_output("retrieval_result", retrieval_result)
    else:
        dataset.update_output("retrieval_result", [[] for _ in dataset.rows])

    prompts = [prompt_template.get_string(row) for row in dataset]
    preds = generator.generate(prompts)
    dataset.update_output("prompt", prompts)
    dataset.update_output("pred", preds)

    save_dir = Path(str(config["save_dir"]))
    save_dir.mkdir(parents=True, exist_ok=True)
    intermediate = save_dir / "intermediate_data.json"
    intermediate.write_text(json.dumps(dataset.rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload = {
        "records": len(dataset),
        "mode": config.get("mode"),
        "save_dir": str(save_dir),
        "intermediate_data": str(intermediate),
        "first_question": dataset.rows[0].get("question") if dataset.rows else None,
        "first_pred": preds[0] if preds else None,
        "first_retrieved": len(dataset.rows[0].get("output", {}).get("retrieval_result", [])) if dataset.rows else 0,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
