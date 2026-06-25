# Repository Provenance

## Purpose

Read this before deciding whether this skill is current for a checkout of FlagEmbedding. If the current repo commit, dirty state, package version, public API signatures, examples, or packaging metadata differ from this snapshot, run `refresh-skill-from-repo`.

## Snapshot

```json
{
  "schema": "skillsmith.repo-provenance.v1",
  "generated_at_utc": "2026-06-21T00:00:00Z",
  "repository": {
    "name": "FlagEmbedding",
    "remote_url": "omitted-private-or-unknown",
    "vcs": "git",
    "branch": "master",
    "tag": "v1.4.0",
    "commit": "7ed43d67ec03fbe5c31c0992dbfa941fb1860549",
    "working_tree": "clean",
    "dirty_paths": []
  },
  "packages": [
    {
      "name": "FlagEmbedding",
      "version": "1.4.0",
      "import_names": ["FlagEmbedding"]
    }
  ],
  "evidence": {
    "source_roots": [
      "FlagEmbedding"
    ],
    "docs": [
      "README.md",
      "README_zh.md",
      "docs/source/Introduction",
      "docs/source/API",
      "docs/source/tutorial",
      "docs/source/bge",
      "Tutorials",
      "dataset/README.md"
    ],
    "examples": [
      "examples/inference",
      "examples/finetune",
      "examples/evaluation"
    ],
    "scripts": [
      "scripts/hn_mine.py",
      "scripts/add_reranker_score.py",
      "scripts/split_data_by_length.py",
      "scripts/README.md"
    ],
    "tests": [
      "tests/test_imports_v5.py",
      "tests/test_infer_embedder_basic.py",
      "tests/test_infer_reranker_basic.py",
      "tests/README.md"
    ],
    "excluded_or_deprioritized": [
      "research",
      "imgs",
      ".github",
      "build/cache/environment directories"
    ]
  },
  "inspection": {
    "status": "passed",
    "backend": "CPU package inspection",
    "verified_imports": [
      "FlagEmbedding",
      "FlagEmbedding.inference.auto_embedder",
      "FlagEmbedding.inference.auto_reranker",
      "FlagEmbedding.abc.inference.AbsEmbedder",
      "FlagEmbedding.abc.inference.AbsReranker"
    ],
    "verified_signatures": [
      "FlagAutoModel.from_finetuned",
      "FlagAutoReranker.from_finetuned",
      "AbsEmbedder.__init__",
      "AbsEmbedder.encode_queries",
      "AbsEmbedder.encode_corpus",
      "AbsEmbedder.encode",
      "AbsReranker.__init__",
      "AbsReranker.compute_score"
    ]
  }
}
```

## Refresh Check

- If `git rev-parse HEAD` differs from `repository.commit`, treat the skill as potentially stale.
- If the current working tree is dirty and this snapshot is clean, or dirty paths differ, refresh before relying on exact API details.
- If `setup.py`, public imports, model mappings, inference/fine-tune/evaluation modules, examples, or docs changed, refresh even when the package version remains `1.4.0`.
- If the package introduces new optional extras or changes Torch/Transformers compatibility, refresh install and troubleshooting guidance.
