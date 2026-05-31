---
doc_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_PAPER_STABILITY_WINDOW_01_STABILITY_REPORT
doc_type: stability_window_report
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_PAPER_STABILITY_WINDOW_01
machine: db-layer
mode: PAPER
produced_at: 2026-05-31
---

# STABILITY_WINDOW_REPORT — Fenêtre Stabilité PAPER db-layer

## Runs documentés (nouveaux)

| run_id | timestamp | modules_ok | modules_failed | verdict |
| --- | --- | --- | --- | --- |
| desk_run_20260531_055602 | 2026-05-31 05:56:02 UTC | 11/11 | 0 | PASS |
| desk_run_20260531_055612 | 2026-05-31 05:56:12 UTC | 11/11 | 0 | PASS |
| desk_run_20260531_055620 | 2026-05-31 05:56:20 UTC | 11/11 | 0 | PASS |
| desk_run_20260531_055647 | 2026-05-31 05:56:47 UTC | 11/11 | 0 | PASS |

## Runs historiques (référence PAPER_PROMOTION_GATE)

| run_id | source | modules_ok | verdict |
| --- | --- | --- | --- |
| desk_run_20260518_094615 | READONLY_WORKFLOW_SMOKE_01 | 11/11 | PASS |
| desk_run_20260518_195528 | PAPER_FIRST_REGULAR_OPERATION_01 | 11/11 | PASS |

## Vérification seuil gate

| Critère | Requis | Observé | |
| --- | --- | --- | --- |
| Runs nouveaux documentés | >= 4 | 4 | ✓ |
| modules_ok par run | 11/11 | 11/11 | ✓ |
| modules_failed | 0 | 0 | ✓ |
| mode | PAPER | PAPER | ✓ |
| secrets dans commits | 0 | 0 | ✓ |
| live trading | aucun | aucun | ✓ |
| git status post-run | clean | clean | ✓ |

## Verdict stabilité

```
GATE = PASS
Fenêtre de stabilité PAPER validée sur db-layer.
6 runs consécutifs (historique + nouveaux) — 11/11 OK, 0 failed.
Recommandation : prêt pour CHILD_FIRST_LOOP_JOB_01 (boucle FORMAT 1→5).
```

## Observations comportementales

```
- Tous les modules s'exécutent en séquence sans interruption
- Mode PAPER respecté sur toute la série
- Aucune action hors périmètre (pas d'ordre réel, pas de write gated trading)
- Durée moyenne des runs : ~10 secondes
- git status clean post-run sur chaque exécution
```
