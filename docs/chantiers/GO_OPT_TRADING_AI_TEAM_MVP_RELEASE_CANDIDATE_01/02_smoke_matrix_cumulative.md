---
doc_id: GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01_SMOKE_MATRIX_CUMULATIVE
doc_type: smoke_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01
status: open
lifecycle_stage: validation
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 02_SMOKE_MATRIX_CUMULATIVE — Smokes cumules AI Team MVP

## Total

| Metrique | Valeur |
|:---------|:------|
| Task types smokes | 5 |
| Criteres totaux | 35 |
| Criteres PASS | 35 |
| Criteres FAIL | 0 |
| Denied inputs (cumul) | 0 |
| Git write ops (cumul) | 0 |
| Date derniere execution | 2026-05-05 |

## Detail par task type

### READ_INVENTORY (6 criteres) — SETUP_MVP_01

1. runner_executes_without_error — PASS
2. output_contains_13_ESTABLISHED — PASS
3. output_contains_VERDICT_DRAFT_ONLY — PASS
4. no_git_write_ops — PASS
5. no_denied_inputs_read — PASS
6. at_least_one_chantier_listed — PASS (34)

### DOC_DRAFT (6 criteres) — OBSERVER_DOC_DRAFT_01

1. runner_executes_without_error — PASS
2. draft_file_created_in_drafts_dir — PASS
3. output_contains_13_ESTABLISHED — PASS
4. output_contains_VERDICT_DRAFT_ONLY — PASS
5. no_git_write_ops — PASS
6. no_write_outside_drafts_dir — PASS

### ANALYZE_INVENTORY (8 criteres) — MVP_V2_ORCHESTRATOR_ANALYZER_01

1. runner_executes_without_error — PASS
2. analysis_file_created_in_drafts_dir — PASS
3. output_contains_13_ESTABLISHED — PASS
4. output_contains_VERDICT_DRAFT_ONLY — PASS
5. domain_classification_present — PASS (6 domaines)
6. status_classification_present — PASS (12 CLOS, 22 ACTIVE)
7. no_git_write_ops — PASS
8. no_write_outside_drafts_dir — PASS

### ORCHESTRATOR_CHAIN (7 criteres) — MVP_V2_ORCHESTRATOR_ANALYZER_01

1. chain_executes_completely — PASS
2. all_3_steps_exit_zero — PASS
3. intermediate_files_produced — PASS
4. final_draft_produced — PASS
5. no_git_write_ops — PASS
6. no_denied_inputs — PASS
7. no_write_outside_drafts_dir — PASS

### PATCH_DRAFT (8 criteres) — PATCH_DRAFT_01

1. runner_executes_without_error — PASS
2. patch_proposal_created_in_patches_dir — PASS
3. target_file_not_modified — PASS
4. output_contains_PATCH_PROPOSAL — PASS
5. output_contains_VERDICT_DRAFT_ONLY — PASS
6. no_git_write_ops — PASS
7. no_file_modification_outside_patches — PASS
8. no_denied_inputs_touched — PASS

## Verdict

**PASS** — 5/5 task types smokes valides. 35/35 criteres PASS. 0 denied, 0 git write.
