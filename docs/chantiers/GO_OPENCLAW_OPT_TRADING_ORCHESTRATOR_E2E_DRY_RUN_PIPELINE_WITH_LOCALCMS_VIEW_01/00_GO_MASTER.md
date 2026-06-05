---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_E2E_DRY_RUN_PIPELINE_WITH_LOCALCMS_VIEW_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #468  (TMUX Runtime Spine — merged)
  - PR #470  (LocalCMS central UI — open, mergeable)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_E2E_DRY_RUN_PIPELINE_WITH_LOCALCMS_VIEW_01

## Objectif

Prouver que le flux complet E2E en dry-run apparaît dans LocalCMS.

## Pipeline à valider

```text
signal_router
→ proposition_engine
→ validation_gate
→ trade_executor (dry-run)
→ result_tracker
→ datasheet_writer
→ learning_feeder
→ TMUX health
→ LocalCMS runtime view (/runtime/tmux + /menu)
```

## Entrées

- Tous les workers GO-03 à GO-10 (implémentés, mergés)
- TMUX Runtime Spine (PR #468, merged)
- LocalCMS Central UI (PR #470, à merger d'abord)
- `DRY_RUN=1 PAPER_MODE=1` sur strict-workers

## À produire

1. Merger PR #470 (LocalCMS)
2. Script E2E dry-run qui enchaîne les 7 workers
3. Vérifier que chaque étape écrit dans son artefact
4. Vérifier que TMUX health_check.py rapporte les sessions UP
5. Vérifier que LocalCMS GET /menu et GET /runtime/tmux retournent les états corrects
6. Documenter le résultat dans un rapport d'intégration

## Livrables

- `scripts/e2e/dry_run_pipeline.sh` — script d'enchaînement
- `tests/e2e/test_e2e_dry_run_pipeline.py` — tests automatisés
- Rapport d'intégration E2E

## Contraintes

- Pas de live trade
- `DRY_RUN=1 PAPER_MODE=1` verrouillés
- Ne pas modifier les sessions TMUX critiques
- LocalCMS reste lecture seule

## RISKS

- À qualifier.
