# HF Free Platform Spec V1

## Mission
Create a free-first Hugging Face delivery platform module inside `opt-trading` without moving canonical truth away from Git.

## Core decision
- Canonical development stays in `magikgmo4-ui/opt-trading`
- Base branch: `sot/mainline`
- Epic branch: `feature/hf-free-platform-v1`
- Hugging Face repos are publication targets only

## Product patterns
- portal public
- private tools space
- public MCP tool
- public assets dataset

## Guardrails
- no secrets in repo
- no live trading core on HF
- no persistent state assumptions on HF Free
