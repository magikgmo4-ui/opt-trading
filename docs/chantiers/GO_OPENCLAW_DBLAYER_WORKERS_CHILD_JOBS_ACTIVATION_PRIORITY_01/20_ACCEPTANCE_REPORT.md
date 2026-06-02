---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_ACTIVATION_PRIORITY_01_ACCEPTANCE
doc_type: acceptance_report
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_ACTIVATION_PRIORITY_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: PASS
closed_at: 2026-06-01
---

# 20_ACCEPTANCE_REPORT — Matrice d'activation priorisée

## Verdict

```
STATUS = PASS
116 jobs analysés — matrice complète produite
```

## Résultats

| lot | count | verdict |
|---|---|---|
| Lot 0 — déjà actifs (GHA) | 7 | ALREADY_ACTIVE |
| Lot 1 — activation immédiate | 15 | NOW |
| Lot 2 — semaine suivante | 20 | NEXT |
| Lot 3 — phase 04-06 HITL/cockpit | 23 | LATER |
| MANUAL_ONLY | 10 | jamais scheduler |
| BLOCKED apps externes | 41 | bridges non prouvés |

## Lot 1 identifié (15 jobs)

```
14 jobs script_direct (scripts/ai/workers/*.py confirmés)
 1 job dispatcher  (GO_STRICT_WORKERS_READONLY_SMOKE_01, dispatcher opérationnel)

Tous phase_01 ou phase_03 PASS.
Aucun write externe. dry_run=True sur le seul job dispatcher.
```

## Invariants respectés

```
✓ Aucun LLM dans la boucle de dispatch
✓ Apps externes restent BLOCKED (41 jobs) tant que bridge non prouvé
✓ MANUAL_ONLY identifiés explicitement (kill-switch-fullstop-test etc.)
✓ GHA déjà actifs comptabilisés séparément (Lot 0)
✓ Prochaine étape définie : LOT1_SMOKE chantier
✓ Parent non fermé
```

## Prochaine étape

```
GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_SMOKE_01
Valider les 15 jobs Lot 1 en run réel → rapport d'activation → cron.
```
