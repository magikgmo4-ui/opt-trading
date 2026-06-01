---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_OPERATOR_TOOLS_BUNDLE_01__CADRAGE
doc_type: cadrage
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_OPERATOR_TOOLS_BUNDLE_01
status: open
owner: OpenCode
created_at: 2026-05-31
---

# Cadrage

## Objectif

Regrouper les outils opérateur bot-vision nécessaires sur `admin-trading` pour :

- vérifier la capacité runtime réelle
- maintenir un checkout canonique propre séparé du runtime mutable
- stabiliser de façon reproductible le runtime opérateur `/opt/trading`

## Bundle visé

- `scripts/e2e/bot_vision_runtime_real_preflight.py`
- `scripts/e2e/bot_vision_admin_trading_canonical_checkout.py`
- `scripts/e2e/bot_vision_admin_trading_runtime_stabilize.py`

## Règle opératoire

Ordre recommandé :

1. `bot_vision_runtime_real_preflight.py`
2. `bot_vision_admin_trading_canonical_checkout.py`
3. `bot_vision_admin_trading_runtime_stabilize.py`
