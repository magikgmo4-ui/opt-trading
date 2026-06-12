---
doc_id: INTEGRATION_SMOKE_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 60_NEXT_GO_DECISION — Integration Smoke

## Verdict

**PASS** — Integration complete validee. Pipeline automatise stable depuis 2h+.

## Chaine operationnelle

```
bot-vision-headless-capture.timer (10 min)
  → vision_inbox (PNG + JSON)
  → vision_bot (OCR, ~10s)
  → vision_processed + vision_outbox (.md/.txt)
  → desk_bridge.timer (10 min)
  → crop 2x2 → desk/snapshots/
  → Desk Pro (PAPER, 11/11 OK)
```

## Prochain GO recommande (P1)

### GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01

**Objectif**: Ajouter `[ -s "$file" ]` dans bridge_vision_to_desk_inbox.sh.

La chaine est stable. Le seul point fragile restant est l'absence de garde-fou anti 0-byte
dans le script bridge. C'est une modification legere (~2 lignes) qui empeche les futures
corruptions PIL.

## Backlog

| GO | Priorite | Description |
| --- | --- | --- |
| GO_BRIDGE_GUARD_ADD_01 | P1 | Garde-fou [ -s ] dans bridge |
| GO_WEBHOOK_RUNTIME_REVIEW_01 | P2 | Audit webhook runtime |
| GO_BOT_VISION_HEADLESS_CLOSEOUT_01 | P3 | Closeout chantier headless |

## RISKS

- À qualifier.
