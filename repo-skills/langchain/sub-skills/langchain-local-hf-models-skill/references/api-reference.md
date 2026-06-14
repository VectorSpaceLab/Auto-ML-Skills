# Local Hugging Face API Reference

Read this when wiring local Transformers weights into LangChain.

## Package Boundary

- `langchain-huggingface` provides LangChain wrappers such as `HuggingFacePipeline` and `ChatHuggingFace`.
- `transformers` loads tokenizers, configs, causal LM weights, and pipelines.
- `torch` supplies CPU/GPU tensors and dtype/device controls.
- `langchain` and `langchain-core` are not enough by themselves for local HF model loading.

## Common Imports

```python
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
```

If `langchain_huggingface` is not installed, use raw `transformers` for a smoke test first, then install the wrapper package.

## HuggingFacePipeline

Use for text-generation pipelines:

```python
llm = HuggingFacePipeline.from_model_id(
    model_id=model_path_or_id,
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 32,
        "do_sample": False,
        "return_full_text": False,
    },
)
text = llm.invoke("Explain LCEL in one sentence.")
```

Useful parameters:

| Parameter | Notes |
| --- | --- |
| `model_id` | Local directory or public model id. Local directories should contain `config.json`, tokenizer files, and weight files. |
| `task` | Usually `text-generation` for causal LMs. |
| `pipeline_kwargs` | Keep smoke tests short with `max_new_tokens` and deterministic decoding. |
| `model_kwargs` | Pass dtype/device/load options when supported by the wrapper version. |

## ChatHuggingFace

Use only when the underlying model and tokenizer can represent chat messages:

```python
llm = HuggingFacePipeline.from_model_id(model_id=model_path, task="text-generation")
chat = ChatHuggingFace(llm=llm)
reply = chat.invoke([("human", "Say OK.")])
```

If `ChatHuggingFace` fails on message conversion or tool binding, validate the plain `HuggingFacePipeline` path first. Local causal LMs often need a tokenizer chat template or a custom prompt adapter before they behave like provider chat models.

## Raw Transformers Fallback

Use raw Transformers when the LangChain wrapper is not installed or when debugging model loading:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
inputs = tokenizer("Say OK.", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=8, do_sample=False)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

This proves the model runtime works before LangChain wrapper issues are introduced.

## Tool Calling Boundary

Do not assume a local Transformers causal LM supports provider-style `bind_tools()` or structured tool-call messages. For tool agents, first validate normal text generation; then add a prompt/parser or a chat wrapper that explicitly supports tool-call formatting.
