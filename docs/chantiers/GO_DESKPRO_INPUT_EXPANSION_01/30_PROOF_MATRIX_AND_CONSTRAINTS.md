---
doc_id: GO_DESKPRO_INPUT_EXPANSION_01_PROOF_MATRIX_AND_CONSTRAINTS
doc_type: matrix
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 30_PROOF_MATRIX_AND_CONSTRAINTS

## Invariants

- aucun ordre live
- aucune écriture Sheets globale
- aucun Telegram live
- pas de lecture de fichiers runtime non nécessaires (objectif: contracts + tests)

## Preuves minimales attendues

| Preuve | Description | Critère |
| --- | --- | --- |
| Dry-run synthesis | `signal_event + visual_context + desk_snapshot` | `errors=[]`, safety flags true |
| Tests smoke | `tests/test_desk_pro_combined_input_smoke.py` | passe localement |
| E2E dry-run pipeline | `scripts/e2e/dry_run_pipeline.py` | passe et reste sans side effects |
| Join policy | mismatch timeframes/symbols produit warnings (pas de PASS silencieux) | visible dans outputs |

## Constraints de jointure

- `symbol` : mismatch toléré seulement si explicitement détecté (warning)
- `timeframe` : mismatch doit bloquer un claim “PASS” (au moins WARN)
- `visual_context_ref` / `desk_snapshot_ref` : restent optionnels tant que les producers ne les remplissent pas
