---
doc_id: GO_OPT_TRADING_AI_TEAM_REGISTRY_CONSOLIDATION_01_SMOKE_MATRIX
doc_type: smoke_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_REGISTRY_CONSOLIDATION_01
status: open
lifecycle_stage: validation
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 02_SMOKE_MATRIX — Trace des smokes valides

## Matrice des smokes par task type

| Task Type | Date | GO parent | Criteres | Resultat | Denied | Git write | Chantiers |
|:----------|:-----|:----------|:---------|:---------|:-------|:----------|:----------|
| READ_INVENTORY | 2026-05-05 | SETUP_MVP_01 | 6 | 6/6 PASS | 0 | 0 | 34 |
| DOC_DRAFT | 2026-05-05 | OBSERVER_DOC_DRAFT_01 | 6 | 6/6 PASS | 0 | 0 | — |
| ANALYZE_INVENTORY | 2026-05-05 | MVP_V2_ORCHESTRATOR_ANALYZER_01 | 8 | 8/8 PASS | 0 | 0 | 34 |
| ORCHESTRATOR_CHAIN | 2026-05-05 | MVP_V2_ORCHESTRATOR_ANALYZER_01 | 7 | 7/7 PASS | 0 | 0 | 34 |

## Details par task type

### READ_INVENTORY (6 criteres)

1. runner_executes_without_error — PASS
2. output_contains_13_ESTABLISHED — PASS
3. output_contains_VERDICT_DRAFT_ONLY — PASS
4. no_git_write_ops — PASS
5. no_denied_inputs_read — PASS
6. at_least_one_chantier_listed — PASS (34)

### DOC_DRAFT (6 criteres)

1. runner_executes_without_error — PASS
2. draft_file_created_in_drafts_dir — PASS
3. output_contains_13_ESTABLISHED — PASS
4. output_contains_VERDICT_DRAFT_ONLY — PASS
5. no_git_write_ops — PASS
6. no_write_outside_drafts_dir — PASS

### ANALYZE_INVENTORY (8 criteres)

1. runner_executes_without_error — PASS
2. analysis_file_created_in_drafts_dir — PASS
3. output_contains_13_ESTABLISHED — PASS
4. output_contains_VERDICT_DRAFT_ONLY — PASS
5. domain_classification_present — PASS (6 domaines)
6. status_classification_present — PASS (12 CLOS, 22 ACTIVE)
7. no_git_write_ops — PASS
8. no_write_outside_drafts_dir — PASS

### ORCHESTRATOR_CHAIN (7 criteres)

1. chain_executes_completely — PASS
2. all_3_steps_exit_zero — PASS
3. intermediate_files_produced — PASS
4. final_draft_produced — PASS
5. no_git_write_ops — PASS
6. no_denied_inputs — PASS
7. no_write_outside_drafts_dir — PASS

## Total

| Metrique | Valeur |
|:---------|:------|
| Task types smokes | 4 |
| Criteres totaux | 27 |
| Criteres PASS | 27 |
| Criteres FAIL | 0 |
| Denied inputs (cumul) | 0 |
| Git write ops (cumul) | 0 |

## Verdict global

**PASS** — 4/4 task types smokes valides. 27/27 criteres PASS. 0 denied, 0 git write.
