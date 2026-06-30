# Document Processing, Unstructured Data, and RAG Preparation

## When To Read

Document conversion, partitioning, OCR/table pipelines, Markdown conversion, document elements, chunking, extraction, cleaning, staging, remote document services, and RAG-ready document preparation.

## Repo Skill Options

<!-- DISCO_SCENARIO:document-processing-unstructured-data-and-rag-preparation:START -->
### `docling`

Role: Use Docling to convert, parse, configure, extract, chunk, serve, and maintain document-processing workflows across Python APIs, CLI commands, optional pipelines, and repository edits.
Read when: The request names `docling` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: advanced pipelines, cli and formats, conversion, document outputs, extraction, and 3 other focused workflows.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `docling/SKILL.md`, `docling/sub-skills/advanced-pipelines/`, `docling/sub-skills/cli-and-formats/`, `docling/sub-skills/conversion/`, `docling/sub-skills/document-outputs/`, `docling/sub-skills/extraction/`, `docling/sub-skills/pipeline-configuration/`, `docling/sub-skills/remote-service-client/`, `docling/sub-skills/repo-maintenance/`.

### `khoj`

Role: Khoj offers package-specific content ingestion, parser, indexing, and search preparation guidance for document-grounded chat and retrieval.
Read when: Tasks mention Khoj document upload, /api/content, Markdown or Org entries, PDF/DOCX/image/plaintext conversion, GitHub or Notion sync, parser entry fields, chunking, stale index visibility, or making personal docs searchable in Khoj.
Best for: Building or debugging Khoj content ingestion and parser flows before semantic search or chat grounding.
Avoid when: Use a generic document extraction skill when the task is about standalone conversion tools rather than Khoj's content API, parser classes, database entries, or search integration.
Useful entry points: `khoj/SKILL.md`, `khoj/sub-skills/content-indexing/SKILL.md`, `khoj/sub-skills/search-retrieval/SKILL.md`.

### `kotaemon`

Role: Kotaemon provides guidance for its loader/parser/splitter stack and document metadata expected by file indexing workflows.
Read when: The task mentions Kotaemon document ingestion, PDF/table/OCR loaders, Docling, PaddleOCR, Mathpix, Azure Document Intelligence, DOCX/HTML/XLSX/TXT readers, `Document` metadata, `table_origin`, `page_label`, or chunking before indexing.
Best for: Choosing a Kotaemon reader, validating document-like JSON records, diagnosing optional parser dependencies, preserving table metadata, and preparing chunks for the Kotaemon file index.
Avoid when: Avoid for document conversion tools outside Kotaemon or pure OCR/model tasks with no Kotaemon indexing or RAG-preparation context.
Useful entry points: `kotaemon/sub-skills/document-ingestion/SKILL.md`.

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

### `ragflow`

Role: RAGFlow skill for DeepDoc parsers, parser backend selection, file-type routing, parser_config, chunk metadata, and ingestion handoff into RAGFlow datasets.
Read when: Tasks mention DeepDoc, RAGFlow PDF parsing, OCR/layout/table recognition, MinerU, Docling, PaddleOCR, parser_config, Excel-to-HTML, scanned PDFs, empty chunks, bounding boxes, parser tests, or document parser backends.
Best for: Choosing or debugging RAGFlow parser backends and connecting parser outputs to dataset ingestion and retrieval behavior.
Avoid when: Use a standalone document-conversion skill when the task is not tied to RAGFlow parser_config, DeepDoc, or RAGFlow ingestion semantics.
Useful entry points: `ragflow/sub-skills/document-parsing/SKILL.md`, `ragflow/sub-skills/dataset-ingestion-retrieval/SKILL.md`.

### `unstructured`

Role: Use the Unstructured Python package to partition documents into elements, inspect element metadata, chunk outputs for RAG, clean/stage data, add embeddings, evaluate extraction quality, and diagnose optional dependency readiness.
Read when: The request names `unstructured` or asks for package-specific APIs, CLIs, configs, data/model artifacts, error messages, workflows, or repository maintenance that match this project.
Best for: chunking, data preparation, elements and metadata, embeddings, evaluation, and partitioning.
Avoid when: another repo skill in this scenario matches the user's task, package, model family, data format, serving backend, or workflow more directly.
Useful entry points: `unstructured/SKILL.md`, `unstructured/sub-skills/chunking/`, `unstructured/sub-skills/data-preparation/`, `unstructured/sub-skills/elements-and-metadata/`, `unstructured/sub-skills/embeddings/`, `unstructured/sub-skills/evaluation/`, `unstructured/sub-skills/partitioning/`.

<!-- DISCO_SCENARIO:document-processing-unstructured-data-and-rag-preparation:END -->

## How To Choose

Choose by document surface: MarkItDown for conversion to Markdown and MCP conversion, Marker for PDF/OCR extraction, Docling or Unstructured for richer document element pipelines. Choose `docling` when the request names `docling`, centers on Use Docling to convert, parse, configure, extract, chunk, serve, and maintain document-processing workflows across Python APIs, CLI commands, optional pipelines, and repository edits, uses its APIs or CLIs, references its configs/artifacts/errors, or asks for repository workflows in document processing unstructured data and rag preparation. Choose khoj when document processing is tied to Khoj uploads, parser outputs, indexed entries, or search/chat visibility in the Khoj app. Choose kotaemon for document preparation when the target output is Kotaemon `Document` records, ktem File Index data, or a Kotaemon RAG pipeline. Choose `marker` for practical Marker repository/package usage. Start at the root router, then select conversion-cli-api for file conversion, configuration-extension for custom internals, llm-extraction-services for use_llm or extraction schemas, and server-deployment for API/app/Modal surfaces. Choose `markitdown` over generic document/OCR/MCP skills when the user specifically uses MarkItDown package names, APIs, CLI flags, plugin entry points, converter errors, or the markitdown-mcp server.
