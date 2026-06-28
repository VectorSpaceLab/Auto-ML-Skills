# AI Pipelines, Workflows, RAG, and Agents

## When To Read

Pipeline and workflow frameworks that combine embeddings, LLMs, agents, task chains, services, and RAG orchestration.

## Repo Skill Options

<!-- DISCO_SCENARIO:ai-pipelines-workflows-and-rag:START -->
### `txtai`

Role: Helps agents choose between deterministic txtai workflows and agentic/LLM/RAG orchestration, then use the correct sub-skill.
Read when: txtai Workflow, Task, pipeline, Textractor, Summary, Translation, RAG, LLM, Agent, tools, smolagents, workflow YAML, generator not consumed.
Best for: Composing task pipelines, debugging lazy workflows, selecting LLM/RAG/agent backends, configuring tools, and producing safe no-download templates.
Avoid when: The user only needs a generic LangChain/LlamaIndex answer or asks for a non-txtai orchestration framework.
Useful entry points: `txtai/SKILL.md`, `txtai/sub-skills/pipelines-and-workflows/SKILL.md`, `txtai/sub-skills/agents-and-llm-orchestration/SKILL.md`.

<!-- DISCO_SCENARIO:ai-pipelines-workflows-and-rag:END -->

## How To Choose

Use this scenario when the package is primarily an end-to-end AI workflow system rather than only a retriever, vector database, or model-serving backend. Choose pipelines-and-workflows for deterministic batch/stream processing; choose agents-and-llm-orchestration for RAG, model backends, tool choice, and multi-step reasoning.
