# Checkpoint Serde Troubleshooting

## Deserialization Error

Check serializer config, package versions, and whether checkpoint data was written by an older graph/schema. Avoid enabling pickle fallback unless data is trusted.

## Encrypted Serializer Import Fails

Install required crypto dependencies for the package version in use. Import success still does not validate key management.

## Resume Fails After Upgrade

Test `get_state_history` and migrate or abandon old thread ids depending on business requirements.

## Strict Mode Blocks A Type

Add only the minimal trusted module/type allowlist needed. Do not allow all modules for untrusted stores.
