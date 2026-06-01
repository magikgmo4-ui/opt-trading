---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_OPERATOR_TOOLS_BUNDLE_01__USAGE
doc_type: usage
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_OPERATOR_TOOLS_BUNDLE_01
status: delivered
owner: OpenCode
created_at: 2026-05-31
---

# Usage

## 1. Preflight runtime réel

```bash
python3 scripts/e2e/bot_vision_runtime_real_preflight.py
```

Produit un JSON avec :

- dépendances runtime
- secrets/env requis
- blockers explicites
- stage maximal prouvable

## 2. Checkout canonique propre

```bash
python3 scripts/e2e/bot_vision_admin_trading_canonical_checkout.py \
  --source https://github.com/magikgmo4-ui/opt-trading.git \
  --target /home/ghost/opt-trading-mainline-clean \
  --branch sot/mainline
```

Effet :

- clone propre si absent
- sinon `fetch + checkout + reset --hard + clean -fd`

## 3. Stabilisation runtime opérateur

Dry-run :

```bash
python3 scripts/e2e/bot_vision_admin_trading_runtime_stabilize.py \
  --source-root /home/ghost/opt-trading-mainline-clean \
  --runtime-root /opt/trading \
  --backup-root /opt/trading/_ops
```

Apply :

```bash
python3 scripts/e2e/bot_vision_admin_trading_runtime_stabilize.py \
  --source-root /home/ghost/opt-trading-mainline-clean \
  --runtime-root /opt/trading \
  --backup-root /opt/trading/_ops \
  --apply
```

## Séparation canonique

- runtime mutable : `/opt/trading`
- checkout canonique propre : `/home/ghost/opt-trading-mainline-clean`
