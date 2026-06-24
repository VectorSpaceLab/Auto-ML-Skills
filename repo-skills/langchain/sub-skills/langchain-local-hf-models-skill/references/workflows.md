# Local HF Workflows

Read this for practical local model validation and integration.

## Preflight

1. Check model files:
   - `config.json`
   - tokenizer file such as `tokenizer.json`, `tokenizer.model`, or `vocab.json`
   - weight file such as `model.safetensors`, `pytorch_model.bin`, or sharded variants
2. Check imports:

   ```bash
   python scripts/check_hf_local_env.py --model-path /path/to/model
   ```

3. Keep first load small: CPU or a single GPU, `max_new_tokens=8-32`, deterministic decoding.

## Raw Generation Smoke

Run:

```bash
python scripts/smoke_local_hf_model.py --model-path /path/to/model --max-new-tokens 16
```

The script prints JSON with:

- whether `torch`, `transformers`, and `langchain_huggingface` are importable
- resolved model file checks
- device and dtype selected
- generated text length and excerpt
- whether the LangChain wrapper path ran

## LangChain LCEL Composition

After local generation works:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(model_id=model_path, task="text-generation")
prompt = PromptTemplate.from_template("Answer in one sentence: {question}")
chain = prompt | llm | StrOutputParser()
print(chain.invoke({"question": "What is LCEL?"}))
```

## Chat Template Path

For Qwen-style and other chat-tuned models, prefer tokenizer chat templates when using raw Transformers:

```python
messages = [{"role": "user", "content": "Say OK."}]
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)
```

Some tokenizers support extra template parameters such as disabling thinking. Treat those as model-specific runtime knobs, not LangChain-wide behavior.

## Validation Boundaries

- A successful raw Transformers generation proves the local model and runtime can generate.
- A successful `HuggingFacePipeline.invoke()` proves the LangChain LLM wrapper can call the model.
- A successful `ChatHuggingFace.invoke()` proves chat-message conversion works for that wrapper/model pair.
- Tool calling, JSON mode, and provider-native structured output need separate validation.
