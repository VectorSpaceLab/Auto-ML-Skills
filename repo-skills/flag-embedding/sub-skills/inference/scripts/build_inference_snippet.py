#!/usr/bin/env python3
"""Build deterministic FlagEmbedding inference snippets without loading models."""

from __future__ import annotations

import argparse
import sys
import textwrap


TEMPLATES = {
    "embedder": '''\
        from FlagEmbedding import FlagAutoModel

        model = FlagAutoModel.from_finetuned(
            "{model}",
            normalize_embeddings=True,
            use_fp16={use_fp16},
            devices={devices},
        )

        sentences = ["I love NLP", "I love text retrieval"]
        embeddings = model.encode(sentences, batch_size={batch_size}, max_length={max_length})
        print(embeddings.shape)
    ''',
    "query-corpus": '''\
        from FlagEmbedding import FlagAutoModel

        model = FlagAutoModel.from_finetuned(
            "{model}",
            query_instruction_for_retrieval={query_instruction},
            query_instruction_format={query_instruction_format},
            normalize_embeddings=True,
            use_fp16={use_fp16},
            devices={devices},
        )

        queries = ["how do dense retrievers work?"]
        corpus = [
            "Dense retrievers encode text into vectors and compare vector similarity.",
            "Cross-encoders rerank query-document pairs directly.",
        ]
        query_vectors = model.encode_queries(queries, batch_size={batch_size}, max_length=128)
        passage_vectors = model.encode_corpus(corpus, batch_size={batch_size}, max_length={max_length})
        scores = query_vectors @ passage_vectors.T
        print(scores)
    ''',
    "bge-m3": '''\
        from FlagEmbedding import BGEM3FlagModel

        model = BGEM3FlagModel(
            "{model}",
            normalize_embeddings=True,
            use_fp16={use_fp16},
            devices={devices},
        )

        queries = ["what is vector search?"]
        passages = [
            "Vector search compares dense embeddings.",
            "Sparse retrieval matches weighted lexical terms.",
        ]
        query_outputs = model.encode_queries(
            queries,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs={return_colbert_vecs},
        )
        passage_outputs = model.encode_corpus(
            passages,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs={return_colbert_vecs},
        )
        dense_scores = query_outputs["dense_vecs"] @ passage_outputs["dense_vecs"].T
        sparse_scores = model.compute_lexical_matching_score(
            query_outputs["lexical_weights"],
            passage_outputs["lexical_weights"],
        )
        print("dense", dense_scores)
        print("sparse", sparse_scores)
    ''',
    "reranker": '''\
        from FlagEmbedding import FlagAutoReranker

        reranker = FlagAutoReranker.from_finetuned(
            "{model}",
            use_fp16={use_fp16},
            devices={devices},
            query_max_length=256,
            max_length={max_length},
        )

        pairs = [
            ["what is panda?", "hi"],
            ["what is panda?", "The giant panda is a bear species endemic to China."],
        ]
        scores = reranker.compute_score(pairs, normalize={normalize_scores})
        print(scores)
    ''',
    "custom-embedder": '''\
        from FlagEmbedding import FlagAutoModel

        model = FlagAutoModel.from_finetuned(
            "{model}",
            model_class="{embedder_model_class}",
            pooling_method="{pooling_method}",
            query_instruction_for_retrieval={query_instruction},
            query_instruction_format={query_instruction_format},
            normalize_embeddings=True,
            use_fp16={use_fp16},
            devices={devices},
        )

        query_vectors = model.encode_queries(["query text"], batch_size={batch_size}, max_length=128)
        passage_vectors = model.encode_corpus(["candidate passage"], batch_size={batch_size}, max_length={max_length})
        print(query_vectors @ passage_vectors.T)
    ''',
    "custom-reranker": '''\
        from FlagEmbedding import FlagAutoReranker

        reranker = FlagAutoReranker.from_finetuned(
            "{model}",
            model_class="{reranker_model_class}",
            use_fp16={use_fp16},
            devices={devices},
            query_max_length=256,
            max_length={max_length},
        )

        score = reranker.compute_score(["query text", "candidate passage"], normalize={normalize_scores})
        print(score)
    ''',
    "layerwise-reranker": '''\
        from FlagEmbedding import LayerWiseFlagLLMReranker

        reranker = LayerWiseFlagLLMReranker(
            "{model}",
            use_fp16={use_fp16},
            devices={devices},
            query_max_length=256,
            max_length={max_length},
        )

        score = reranker.compute_score(
            ["query text", "candidate passage"],
            cutoff_layers={cutoff_layers},
            normalize={normalize_scores},
        )
        print(score)
    ''',
    "lightweight-reranker": '''\
        from FlagEmbedding import LightWeightFlagLLMReranker

        reranker = LightWeightFlagLLMReranker(
            "{model}",
            use_fp16={use_fp16},
            devices={devices},
            query_max_length=256,
            max_length={max_length},
        )

        score = reranker.compute_score(
            ["query text", "candidate passage"],
            cutoff_layers={cutoff_layers},
            compress_ratio={compress_ratio},
            compress_layers={compress_layers},
            normalize={normalize_scores},
        )
        print(score)
    ''',
}

DEFAULT_MODELS = {
    "embedder": "BAAI/bge-base-en-v1.5",
    "query-corpus": "BAAI/bge-large-en-v1.5",
    "bge-m3": "BAAI/bge-m3",
    "reranker": "BAAI/bge-reranker-base",
    "custom-embedder": "./my-local-embedder",
    "custom-reranker": "./my-local-reranker",
    "layerwise-reranker": "BAAI/bge-reranker-v2-minicpm-layerwise",
    "lightweight-reranker": "BAAI/bge-reranker-v2.5-gemma2-lightweight",
}


def _python_literal(value: str) -> str:
    return repr(value)


def _bool_literal(value: bool) -> str:
    return "True" if value else "False"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a deterministic FlagEmbedding inference snippet. This generator does not import FlagEmbedding or download models."
    )
    parser.add_argument(
        "kind",
        choices=sorted(TEMPLATES),
        help="Snippet kind to generate.",
    )
    parser.add_argument("--model", help="Model id or local checkpoint path to place in the snippet.")
    parser.add_argument("--device", default="cpu", help="Device string to place in the snippet, for example cpu or cuda:0.")
    parser.add_argument("--fp16", action="store_true", help="Set use_fp16=True in the snippet.")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size used in generated snippets.")
    parser.add_argument("--max-length", type=int, default=512, help="Max length used in generated snippets.")
    parser.add_argument(
        "--query-instruction",
        default="Represent this sentence for searching relevant passages: ",
        help="Query instruction for embedder snippets.",
    )
    parser.add_argument(
        "--query-instruction-format",
        default="{}{}",
        help="Two-slot query instruction format for embedder snippets.",
    )
    parser.add_argument(
        "--embedder-model-class",
        default="encoder-only-base",
        choices=["encoder-only-base", "encoder-only-m3", "decoder-only-base", "decoder-only-icl", "decoder-only-pseudo_moe"],
        help="Explicit embedder model_class for custom-embedder snippets.",
    )
    parser.add_argument(
        "--reranker-model-class",
        default="encoder-only-base",
        choices=["encoder-only-base", "decoder-only-base", "decoder-only-layerwise", "decoder-only-lightweight"],
        help="Explicit reranker model_class for custom-reranker snippets.",
    )
    parser.add_argument(
        "--pooling-method",
        default="cls",
        choices=["cls", "mean", "last_token"],
        help="Pooling method for custom embedder snippets.",
    )
    parser.add_argument("--normalize-scores", action="store_true", help="Set reranker normalize=True.")
    parser.add_argument("--return-colbert-vecs", action="store_true", help="Set return_colbert_vecs=True for BGE-M3 snippets.")
    parser.add_argument("--cutoff-layers", default="[28]", help="Python list expression for layerwise cutoff layers.")
    parser.add_argument("--compress-ratio", type=int, default=2, help="Compression ratio for lightweight reranker snippets.")
    parser.add_argument("--compress-layers", default="[24, 40]", help="Python list expression for lightweight compress layers.")
    args = parser.parse_args()

    model = args.model or DEFAULT_MODELS[args.kind]
    snippet = TEMPLATES[args.kind].format(
        model=model,
        devices=_python_literal(args.device),
        use_fp16=_bool_literal(args.fp16),
        batch_size=args.batch_size,
        max_length=args.max_length,
        query_instruction=_python_literal(args.query_instruction),
        query_instruction_format=_python_literal(args.query_instruction_format),
        embedder_model_class=args.embedder_model_class,
        reranker_model_class=args.reranker_model_class,
        pooling_method=args.pooling_method,
        normalize_scores=_bool_literal(args.normalize_scores),
        return_colbert_vecs=_bool_literal(args.return_colbert_vecs),
        cutoff_layers=args.cutoff_layers,
        compress_ratio=args.compress_ratio,
        compress_layers=args.compress_layers,
    )
    print(textwrap.dedent(snippet).strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
