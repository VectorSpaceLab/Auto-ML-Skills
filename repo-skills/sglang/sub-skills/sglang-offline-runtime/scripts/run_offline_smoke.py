#!/usr/bin/env python3
"""Optional SGLang offline smoke helper."""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a minimal offline SGLang generation smoke if a model is provided.")
    parser.add_argument("--model", help="Public model ID or local path supplied by the user.")
    parser.add_argument("--prompt", default="Say hello in one short sentence.")
    parser.add_argument("--max-new-tokens", type=int, default=16)
    parser.add_argument("--dry-run", action="store_true", help="Only print the intended configuration.")
    args = parser.parse_args()

    config = {"model": args.model or "<MODEL_ID>", "prompt": args.prompt, "max_new_tokens": args.max_new_tokens}
    if args.dry_run or not args.model:
        print(json.dumps({"dry_run": True, "config": config}, indent=2))
        return 0

    try:
        import sglang as sgl
    except Exception as exc:
        print(f"failed to import sglang: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    try:
        runtime = sgl.Runtime(model_path=args.model)
        sgl.set_default_backend(runtime)

        @sgl.function
        def program(s, prompt):
            s += prompt + "\n" + sgl.gen("out", max_tokens=args.max_new_tokens, temperature=0.0)

        state = program.run(args.prompt)
        print(state["out"])
        runtime.shutdown()
        return 0
    except Exception as exc:
        print(f"offline smoke failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
