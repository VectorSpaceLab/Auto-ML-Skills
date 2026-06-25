# Document Processing, Unstructured Data, and RAG Preparation

## When To Read

Document conversion, partitioning, OCR/table pipelines, Markdown conversion, document elements, chunking, extraction, cleaning, staging, remote document services, and RAG-ready document preparation.

## Repo Skill Options

<!-- SKILLQED_SCENARIO:document-processing-unstructured-data-and-rag-preparation:START -->
### `docling`

Role: Use Docling to convert, parse, configure, extract, chunk, serve, and maintain document-processing workflows across Python APIs, CLI commands, optional pipelines, and repository edits.
Read when: The request names `docling` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: advanced pipelines, cli and formats, conversion, document outputs, extraction, and 3 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `docling/SKILL.md`, `docling/sub-skills/advanced-pipelines/`, `docling/sub-skills/cli-and-formats/`, `docling/sub-skills/conversion/`, `docling/sub-skills/document-outputs/`, `docling/sub-skills/extraction/`, `3 more sub-skills`.

### `marker`

Role: Provides self-contained guidance for using Marker CLI, Python APIs, LLM extraction, configuration extension, and local app/server deployment.
Read when: User mentions Marker, marker-pdf, marker_single, marker, marker_server, PdfConverter, TableConverter, OCRConverter, ExtractionConverter, document conversion, OCR, tables, markdown/json/html/chunks, use_llm, Gemini/OpenAI/Ollama/Claude, Streamlit GUI, FastAPI server, or Modal deployment.
Best for: Generating Marker commands or Python snippets, choosing output formats, configuring processors/renderers/providers, validating extraction schemas, troubleshooting optional dependencies, and adapting local API/server deployment.
Avoid when: The task is about an unrelated document conversion library, general OCR theory without Marker, cloud Datalab managed API usage not tied to Marker package workflows, or reproducing full benchmark datasets unless explicitly requested.
Useful entry points: `marker/SKILL.md`, `marker/sub-skills/conversion-cli-api/SKILL.md`, `marker/sub-skills/configuration-extension/SKILL.md`, `marker/sub-skills/llm-extraction-services/SKILL.md`, `marker/sub-skills/server-deployment/SKILL.md`.

### `markitdown`

Role: Provides repo-specific guidance for using MarkItDown's Python API, CLI, optional converters, plugins, OCR add-on, Azure integrations, and MCP server.
Read when: User mentions MarkItDown, markitdown CLI, MarkItDown Python API, DocumentConverter, StreamInfo, UnsupportedFormatException, MissingDependencyException, markitdown-ocr, markitdown-mcp, Azure Content Understanding, Azure Document Intelligence, or markitdown.plugin. User mentions markitdown-mcp, convert_to_markdown(uri), Claude Desktop MarkItDown server, MCP Inspector, Streamable HTTP, SSE, STDIO, MARKITDOWN_ENABLE_PLUGINS, or Docker-mounted document conversion.
Best for: Converting heterogeneous documents to Markdown for LLM pipelines, diagnosing MarkItDown conversion failures, enabling plugins/OCR, using Azure extraction, developing custom converters, and exposing conversion via local MCP. Safe local/loopback MCP server setup, Docker mount guidance, plugin-enabled MarkItDown MCP conversion, and MCP troubleshooting tied to MarkItDown conversion semantics.
Avoid when: The task needs high-fidelity visual document rendering, generic OCR unrelated to MarkItDown, cloud service provisioning outside conversion, or MCP server design not using markitdown-mcp. The user wants a general authenticated public MCP service, an unrelated MCP server, or non-MarkItDown document processing.
Useful entry points: `markitdown/SKILL.md`, `markitdown/sub-skills/core-conversion/SKILL.md`, `markitdown/sub-skills/cloud-integrations/SKILL.md`, `markitdown/sub-skills/ocr-plugin/SKILL.md`, `markitdown/sub-skills/plugin-development/SKILL.md`, `markitdown/sub-skills/mcp-server/SKILL.md`.

### `unstructured`

Role: Use the Unstructured Python package to partition documents into elements, inspect element metadata, chunk outputs for RAG, clean/stage data, add embeddings, evaluate extraction quality, and diagnose optional dependency readiness.
Read when: The request names `unstructured` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: chunking, data preparation, elements and metadata, embeddings, evaluation, and partitioning.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `unstructured/SKILL.md`, `unstructured/sub-skills/chunking/`, `unstructured/sub-skills/data-preparation/`, `unstructured/sub-skills/elements-and-metadata/`, `unstructured/sub-skills/embeddings/`, `unstructured/sub-skills/evaluation/`, `1 more sub-skills`.

<!-- SKILLQED_SCENARIO:document-processing-unstructured-data-and-rag-preparation:END -->

## How To Choose

Choose by document surface: MarkItDown for conversion to Markdown and MCP conversion, Marker for PDF/OCR extraction, Docling or Unstructured for richer document element pipelines. Choose `docling` when the request names `docling`, centers on Use Docling to convert, parse, configure, extract, chunk, serve, and maintain document-processing workflows across Python APIs, CLI commands, optional pipelines, and repository edits, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in document processing unstructured data and rag preparation. Choose `marker` for practical Marker repository/package usage. Start at the root router, then select conversion-cli-api for file conversion, configuration-extension for custom internals, llm-extraction-services for use_llm or extraction schemas, and server-deployment for API/app/Modal surfaces. Choose `markitdown` over generic document/OCR/MCP skills when the user specifically uses MarkItDown package names, APIs, CLI flags, plugin entry points, converter errors, or the markitdown-mcp server. Start at the root router, then follow the workflow-specific sub-skill. Use the MCP sub-skill when MarkItDown is being exposed as a local agent tool; route conversion-format errors back to core-conversion and plugin setup to plugin-development or ocr-plugin.
