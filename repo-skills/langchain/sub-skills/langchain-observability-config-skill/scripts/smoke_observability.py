#!/usr/bin/env python3
"""No-key smoke test for LangChain runnable config and callbacks."""

from __future__ import annotations

import json


def main() -> int:
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.runnables import RunnableLambda

    events = []

    class Recorder(BaseCallbackHandler):
        def on_chain_start(self, serialized, inputs, **kwargs):  # type: ignore[no-untyped-def]
            events.append("start")

        def on_chain_end(self, outputs, **kwargs):  # type: ignore[no-untyped-def]
            events.append("end")

    chain = RunnableLambda(lambda x: x.upper()).with_config(run_name="smoke", tags=["local"])
    output = chain.invoke(
        "ok",
        config={"callbacks": [Recorder()], "metadata": {"component": "observability-smoke"}},
    )
    result = {"output": output, "events": events}
    result["pass"] = output == "OK" and "start" in events and "end" in events
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
