---
title: OT MCP Public Starter
emoji: "🧰"
colorFrom: blue
colorTo: gray
sdk: gradio
app_file: app.py
pinned: false
license: mit
---

# OT MCP Public Starter

Minimal public starter for the `hf_free_platform` MCP lane.

## What it is
- one safe callable utility
- public and stateless
- no secrets
- no privileged operations

## What it is not
- not a full MCP server
- not a backend service
- not a trading or admin surface

## Utility
This Space exposes a small text-normalization utility for machine-first blocks.
It trims empty lines, normalizes spacing, and returns a short deterministic summary.

## Source of truth
Canonical development lives in `magikgmo4-ui/opt-trading`, base `sot/mainline`.
This HF Space is a publication target only.
