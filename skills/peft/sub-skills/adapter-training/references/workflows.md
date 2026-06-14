# Adapter Training Workflows

Use this reference for end-to-end training patterns.

## LoRA With Transformers Trainer

```python
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

base_model = AutoModelForSequenceClassification.from_pretrained(
    "model-id",
    num_labels=2,
)

config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=16,
    lora_alpha=16,
    target_modules=["query", "value"],
    lora_dropout=0.1,
    bias="none",
    modules_to_save=["classifier"],
)
model = get_peft_model(base_model, config)
model.print_trainable_parameters()

args = TrainingArguments(
    output_dir="adapter-output",
    learning_rate=5e-4,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    save_strategy="epoch",
    eval_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    processing_class=tokenizer,
    data_collator=data_collator,
)
trainer.train()
model.save_pretrained("adapter-output")
```

Use `modules_to_save` for task heads that are randomly initialized or not part of adapter layers.

## Causal LM LoRA Or QLoRA Skeleton

```python
from peft import LoraConfig, TaskType, get_peft_model

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    target_modules="all-linear",
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(base_model, config)
```

Use `"all-linear"` for QLoRA-style training. For smaller adapters, target attention projections only.

## IA3 Custom Loop Skeleton

```python
from peft import IA3Config, TaskType, get_peft_model

config = IA3Config(task_type=TaskType.SEQ_2_SEQ_LM)
model = get_peft_model(base_model, config)

for batch in train_dataloader:
    batch = {key: value.to(device) for key, value in batch.items()}
    outputs = model(**batch)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    scheduler.step()
    optimizer.zero_grad()
```

For custom architectures, provide `target_modules` and `feedforward_modules` explicitly.

## Prompt Tuning Skeleton

```python
from peft import PromptTuningConfig, PromptTuningInit, get_peft_model

prompt_text = "Classify the input.\n"
config = PromptTuningConfig(
    task_type="CAUSAL_LM",
    prompt_tuning_init=PromptTuningInit.TEXT,
    num_virtual_tokens=len(tokenizer(prompt_text)["input_ids"]),
    prompt_tuning_init_text=prompt_text,
    tokenizer_name_or_path="base-model-id",
)
model = get_peft_model(base_model, config)
```

Prompt tuning changes the input/prompt path and works best when the task is naturally expressed as generation or prompt-conditioned prediction.

## AdaLoRA Training Note

AdaLoRA needs budget updates during training. If the user uses `AdaLoraConfig`, make sure the training loop or Trainer subclass calls the method that updates and allocates the rank budget at training steps. A plain Trainer loop without this update can miss the adaptive step.

## Trainable Tokens For Added Vocabulary

```python
new_tokens = ["<think>", "</think>"]
tokenizer.add_tokens(new_tokens)
base_model.resize_token_embeddings(len(tokenizer))

config = LoraConfig(
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj"],
    trainable_token_indices={
        "embed_tokens": tokenizer.convert_tokens_to_ids(new_tokens),
    },
)
model = get_peft_model(base_model, config)
```

At inference time, add the same tokens and resize the base model before loading the adapter.

## Save Adapter

```python
model.save_pretrained("adapter-output")
tokenizer.save_pretrained("adapter-output")
```

Saving PEFT adapters saves adapter weights/config by default, not the full base model.

If the adapter name is not `default`, PEFT saves it under a subdirectory named after the adapter.

If embeddings were resized, decide whether `save_embedding_layers="auto"`, `True`, or `False` is correct. Use `False` only when tracked trainable tokens or another explicit strategy guarantees the needed embedding changes can be reconstructed.

## Validation Before Handoff

Run a small forward pass or generation before and after saving/loading:

```python
model.eval()
with torch.no_grad():
    output = model(**batch)
print(output.loss if hasattr(output, "loss") else type(output))
```

Then load through `PeftModel.from_pretrained` or an `AutoPeftModel*` class and compare expected behavior.
