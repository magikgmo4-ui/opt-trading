---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01_CURRENT_STATE
doc_type: current_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 10_CURRENT_STATE - Current State

## Etat valide sur mainline

| Element | Etat |
| --- | --- |
| PR #250 | mergee |
| `sot/mainline` | contient la sequence admin-trading producer/consumer |
| Tests adapter + smoke | `40/40 passed` |
| Adapter `signal_event` V0->V1 | present dans `modules/desk_pro/signal_event_adapter.py` |
| Contract smoke | valide |
| `desk_snapshot` | confirme comme input fonctionnel |
| `visual_context` | disponible via snapshots / pipeline vision |
| `signal_event` | disponible via `events.jsonl` + adapter |

## Situation Desk Pro aujourd'hui

- Desk Pro est consommeur valide mais non automatise
- Le pipeline reste majoritairement manuel / on-demand
- `desk_snapshot` est le point d'entree le plus stable et le plus frais
- `signal_event` est lisible sans modifier le runtime via `read_events_v1()`
- `visual_context` est disponible indirectement par `desk_snapshot` et explicitement au niveau contrat

## Gaps restants confirmes

| Gap | Statut | Impact sur automation |
| --- | --- | --- |
| `desk/state/latest.json` stale | OPEN | necessite strategie de regeneration ou bypass |
| `desk/inputs/tv_inputs_latest.json` stale | OPEN | necessite clarifier si input obligatoire |
| Playwright absent | UPSTREAM | non bloquant si fallback ShareX suffit |
| Pas d'automatisation Desk Pro | OPEN | sujet principal de ce GO |
| Normalisation `BTCUSDT` vs `BTCUSDT.P` | DOCUMENTED | gate obligatoire avant join automatique |

## Conclusion d'etat

L'automatisation peut etre planifiee sans nouvelle recherche de faisabilite. Les contrats et le smoke local ont deja prouve la compatibilite producer/consumer. Le travail restant est un travail de sequencing, gating et observabilite.
