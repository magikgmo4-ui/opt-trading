---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_NAMING_BLOCK_CLOSEOUT_REVIEW_01_READING
doc_type: chantier_note
repo: opt-trading
project: opt-trading
module: naming_normalizer
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_NAMING_BLOCK_CLOSEOUT_REVIEW_01
status: open
lifecycle_stage: analyse
topic_keys:
  - opt-trading
  - naming
  - reading_inventory
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/NAMING_CANON_POLICY_01.md
point_de_reprise: "Section Constat"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_PARENT_THREAD_MAP.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/03_decisions.md
  - modules/naming_normalizer/README.md
---

# 01_naming_reading_inventory

## Sources lues
- `docs/index/GO_INDEX.md`
- `docs/index/GO_CLOSED_INDEX.md`
- `docs/index/GO_PARENT_THREAD_MAP.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`
- `docs/index/BRANCH_STATE.md`
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/governance/NAMING_CANON_POLICY_01.md`
- `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`
- `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/02_go_map.md`
- `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/03_decisions.md`
- `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/00_cadrage.md`
- `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/00_cadrage.md`
- `modules/naming_normalizer/README.md`
- `modules/naming_normalizer/cmd.sh`
- `modules/naming_normalizer/sanity_check.sh`
- `modules/naming_normalizer/scripts/audit_naming.sh`
- `modules/naming_normalizer/app/cli.py`
- `modules/naming_normalizer/app/scanner.py`
- `modules/naming_normalizer/app/report.py`
- `modules/naming_normalizer/config/naming_rules.json`
- `modules/naming_normalizer/config/exceptions.json`

## Constat
- la politique naming canonique existe et reste stable
- le parent naming et les deux enfants sont encore `OPEN` dans `GO_INDEX.md`
- le module `naming_normalizer` existe avec README, wrappers shell, moteur Python et config declarative
- le module reste audit-only : il scanne le repo et ecrit des rapports markdown/json, sans renommage ni deplacement automatique
- aucun rapport existant n'est present sous `modules/naming_normalizer/output/`
- aucun livrable d'inventaire repo-first n'est present dans `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/`

## RISKS

- À qualifier.
