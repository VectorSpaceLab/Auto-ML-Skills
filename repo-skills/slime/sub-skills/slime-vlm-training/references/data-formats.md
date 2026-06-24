# VLM Data Formats

Example:

```json
{
  "messages": [{"role":"user","content":"Solve the geometry problem in the image."}],
  "answer": "270",
  "images": ["relative/or/absolute/path.png"]
}
```

Use:

```bash
--input-key messages
--label-key answer
--multimodal-keys '{"image":"images"}'
--apply-chat-template
```

If images are URLs, ensure the environment can fetch them or preprocess to local paths before training.
