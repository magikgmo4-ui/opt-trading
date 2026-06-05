---
doc_id: HEADLESS_CLOSEOUT_01_RUNTIME
doc_type: runtime_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_RUNTIME_STATE — Etat final

## Timers actifs

| Timer | Intervalle | Prochain |
| --- | --- | --- |
| bot-vision-headless-capture | 10 min | ~2 min |
| desk_bridge | 10 min | ~1 min |

## Services

| Service | Statut | Notes |
| --- | --- | --- |
| tv-webhook | active | Webhook TradingView |
| tv-perf | active | Perf API |
| vision_bot | active | OCR watch loop |
| bot_vision_step2 | active | Telegram + OpenAI |
| ngrok-tv | active | Tunnel TradingView |
| bot-vision-headless-capture | oneshot (inactive dead) | Lance par timer |
| desk_bridge | oneshot (inactive dead) | Lance par timer |
| macro-xau.timer | disabled + inactive | Obsolète |

## Inbox

| Dossier | Fichiers | Corruption |
| --- | --- | --- |
| vision_inbox | ~0 PNG (traites) | 0 |
| vision_processed | 17+ PNG | 0 |
| vision_outbox | .md + .txt | 0 |

## Desk Pro

- Dernier run: desk_run_20260504_234500
- Mode: PAPER
- Resultat: 11/11 OK
- Runner status: OK

## Bridges / guards

- desk_bridge.timer: exit 0/SUCCESS
- 3 guards anti 0-byte/.uploading en place
- Aucun crash PIL depuis le deploiement du guard

## RISKS

- À qualifier.
