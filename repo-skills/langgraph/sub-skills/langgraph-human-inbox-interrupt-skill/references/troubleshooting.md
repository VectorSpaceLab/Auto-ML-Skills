# Human Inbox Troubleshooting

## Resume Payload Shape Fails

Match the shape of the interrupt value. `interrupt([request])` should be resumed with a list such as `[{"type": "accept"}]`.

## Interrupt Does Not Pause

Compile with a checkpointer and pass `thread_id` config. Without persistence, resume state cannot be restored.

## Node Repeats Side Effects

Interrupted nodes re-run after resume. Move side effects after the interrupt result and make them idempotent.

## Response Type Missing

Check the request config. Do not assume `edit` or `respond` is allowed unless enabled.
