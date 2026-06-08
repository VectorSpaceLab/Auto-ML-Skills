# Dense Multimodal Image Search

## User Persona
A product engineer adding text-to-image retrieval and aware that multimodal dependencies may be needed.

## Scenario Coverage
- Skill area: dense-embeddings
- Capability: multimodal `SentenceTransformer` inputs, modality checks, image extra
- Difficulty: intermediate
- Prompt file: `user_request.txt`
- Expected references/scripts: `sub-skills/dense-embeddings/SKILL.md`, `sub-skills/dense-embeddings/references/workflows.md`, root `references/package-overview.md`
- Trigger expectation: The prompt mentions multimodal embedding, image search, local image files, and sentence-transformers.

## Expected Successful Behavior
The agent should recommend the `[image]` extra, inspect `model.modalities` and `model.supports("image")`, use local image paths or PIL images, encode text and image inputs with the same model, and compute similarities.

## Failure Signals
The answer uses URL-only examples despite the prompt, skips modality checks, omits the image extra, or assumes every embedding model supports images.
