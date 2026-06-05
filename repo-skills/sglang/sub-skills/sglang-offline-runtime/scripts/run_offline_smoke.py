#!/usr/bin/env python3
"""Optional SGLang offline smoke helper."""

import argparse
import json
import pathlib
import sys
import time


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a minimal offline SGLang generation smoke if a model is provided.")
    parser.add_argument("--model", help="Public model ID or local path supplied by the user.")
    parser.add_argument("--prompt", default="Say hello in one short sentence.")
    parser.add_argument("--max-new-tokens", type=int, default=4)
    parser.add_argument("--context-length", type=int, default=512)
    parser.add_argument("--mem-fraction-static", type=float, default=0.25)
    parser.add_argument("--dtype", default="auto")
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--report-model-name", help="Safe model label to print in reports instead of echoing --model.")
    parser.add_argument("--out", help="Optional JSON output path.")
    parser.add_argument("--dry-run", action="store_true", help="Only print the intended configuration.")
    args = parser.parse_args()

    if args.report_model_name:
        model_label = args.report_model_name
    elif args.model:
        model_label = pathlib.Path(args.model).name if args.model.startswith("/") else args.model
    else:
        model_label = "<MODEL_ID>"

    config = {
        "model": model_label,
        "prompt": args.prompt,
        "max_new_tokens": args.max_new_tokens,
        "context_length": args.context_length,
        "mem_fraction_static": args.mem_fraction_static,
        "dtype": args.dtype,
        "trust_remote_code": args.trust_remote_code,
    }

    def emit(report: dict) -> None:
        text = json.dumps(report, indent=2, default=str)
        if args.out:
            pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            pathlib.Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(text)

    if args.dry_run or not args.model:
        emit({"dry_run": True, "config": config})
        return 0

    try:
        import sglang as sgl
    except Exception as exc:
        emit({"ok": False, "stage": "import", "config": config, "error_type": type(exc).__name__, "error": str(exc)})
        return 2

    engine = None
    try:
        started = time.time()
        engine = sgl.Engine(
            model_path=args.model,
            context_length=args.context_length,
            mem_fraction_static=args.mem_fraction_static,
            dtype=args.dtype,
            trust_remote_code=args.trust_remote_code,
        )
        result = engine.generate(
            prompt=args.prompt,
            sampling_params={"max_new_tokens": args.max_new_tokens, "temperature": 0.0},
        )
        report = {
            "ok": True,
            "model": model_label,
            "elapsed_sec": round(time.time() - started, 3),
            "result": result,
        }
        emit(report)
        return 0
    except Exception as exc:
        emit({
            "ok": False,
            "stage": "generate",
            "model": model_label,
            "elapsed_sec": round(time.time() - started, 3) if "started" in locals() else None,
            "error_type": type(exc).__name__,
            "error": str(exc),
        })
        return 1
    finally:
        if engine is not None:
            try:
                engine.shutdown()
            except Exception as exc:
                print(f"engine shutdown warning: {type(exc).__name__}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
