---
doc_id: INTEGRATION_SMOKE_01_DESK_BRIDGE
doc_type: desk_bridge_integration
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_DESK_BRIDGE_INTEGRATION

## desk_bridge automatique

- **Timer**: desk_bridge.timer (every 10 min)
- **Dernier run**: 19:41, exit 0/SUCCESS
- **Input**: headless capture depuis vision_processed
- **Pipeline**: crop 2x2 (PIL) → 4 quadrants → desk/snapshots/

## Dernier run (log)

```
bridge_vision_to_desk_inbox.sh: exit 0/SUCCESS
Quadrants generes:
  - BTCUSDT.P_H1 → desk/snapshots/BTCUSDT.P/
  - XAUUSD_H1 → desk/snapshots/XAUUSD/
  - SOLUSDT.P_H1 → desk/snapshots/SOLUSDT.P/
  - ETHUSDT.P_H1 → desk/snapshots/ETHUSDT.P/
```

## Verifications

| Check | Resultat |
| --- | --- |
| PIL crash | NON (0 erreur) |
| 0-byte input | NON (0 fichier) |
| Exit code | 0/SUCCESS |
| Output vers desk/snapshots/ | OUI (4 quadrants) |
| Timer auto | OUI (every 10 min) |

## Verdict desk_bridge

**PASS** — desk_bridge integre les captures headless sans erreur.
Le pipeline crop 2x2 vers Desk Pro est fonctionnel en automatique.

## RISKS

- À qualifier.
