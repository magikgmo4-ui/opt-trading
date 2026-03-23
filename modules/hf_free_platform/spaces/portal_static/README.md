---
title: OT Portal
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
license: mit
---

# OT Portal

Public entry point for the `hf_free_platform` module.

## Role
- Static public portal
- Links to available surfaces (tools, datasets, docs)
- Zero secret material — read-only, no live trading logic

## Surfaces
| Surface | Type | Role |
|---|---|---|
| portal (this) | static HF Space | public entry point |
| tools_private | private HF Space | private tooling |
| mcp_public | public HF Space | public MCP tool |
| public_assets | HF Dataset | public reference data |

## Source of truth
Canonical development lives in `magikgmo4-ui/opt-trading`, branch `sot/mainline`.
This HF Space is a publication target only — not a development surface.

## Constraints
- No secrets
- No live exchange connections
- No persistent state assumptions on HF Free tier
