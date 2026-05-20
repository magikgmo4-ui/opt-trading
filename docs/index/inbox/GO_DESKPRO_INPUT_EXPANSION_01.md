---
doc_id: GO_DESKPRO_INPUT_EXPANSION_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - desk_pro
  - input_map
  - consumer
  - signal_chain
  - contracts
links:
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/10_CURRENT_INPUT_SURFACES.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/20_TARGET_INPUT_CLASSES.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/90_REPRISE_POINT.md
---

# INBOX - GO_DESKPRO_INPUT_EXPANSION_01

## Objet

Fixer la cartographie des inputs consommés par Desk Pro (hub consumer) et la cible d’expansion, à partir des surfaces réelles existantes (desk_snapshot, signal_event, visual_context) et des gaps du produit “signal chain total”.

## Résultat

État établi :

- surfaces Desk Pro relues et reconfirmees pour `modules/desk_pro/dry_run.py`, `modules/desk_pro/api/routes.py`, `modules/desk_pro/ui/page.py` et `tests/test_desk_pro_combined_input_smoke.py`
- les inputs reellement prouves restent `desk_snapshot`, `signal_event` et `visual_context`
- validation relancee dans cette passe : `python -m pytest tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q` -> `31 passed`
- aucune mutation runtime introduite ; le chantier reste doc-first et contract-first

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total via le hub consumer Desk Pro
- `Tableau Kanban du bundle` : reste la reference principale
- `Prochain item Kanban exact` : `GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01`
- `Gaps encore ouverts` : wrappers read-only, refs de jointure, inputs cibles encore non materialises

## Point de reprise

```text
docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/20_TARGET_INPUT_CLASSES.md
docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/40_GAPS_AND_NEXT_GO.md
```
