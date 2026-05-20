# GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01

**État:** En cours
**Branche:** `go/GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01`
**Parent:** `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` (PR #618)

Smoke tests mobile SSH/tmux — CI-safe + checklist humaine Termius/Termux.

## Livrables

- `scripts/tmux/mobile_smoke.sh` — 16/16 PASS CI
- `tests/mobile/test_mobile_smoke.py` — 37/37 PASS
- `docs/chantiers/.../10_HUMAN_CHECKLIST.md` — 20 items device réel

## Constats de cette passe (workspace Windows)

- `python -m unittest tests.mobile.test_mobile_smoke -v` passe avec `OK` et `skipped=12` (bash indisponible ici)
- `bash scripts/tmux/mobile_smoke.sh` reste bloque sans distribution WSL Linux
- la validation Android device reel reste PENDING (checklist humaine)

## Continuité umbrella

- `MASTER_TARGET` : parent `GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`
- item Kanban exact toujours ouvert : `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## NEXT_GO

Aucun obligatoire. GAP-03 PARTIAL — validation Android device PENDING.
