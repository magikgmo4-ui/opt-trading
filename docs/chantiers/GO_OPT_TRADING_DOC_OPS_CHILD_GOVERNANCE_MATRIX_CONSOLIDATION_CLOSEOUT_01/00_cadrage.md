---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - governance
  - matrix
  - continuity
  - closeout
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan d execution"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_PARENT_THREAD_MAP.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 00_cadrage

## Objet

Auditer puis consolider les GO de gouvernance, matrice et methode pour separer :
- les GO reellement clos mais encore signales ouverts
- les GO encore actifs avec gap reel
- les GO a garder ouverts
- les GO strictement de reference pour ce lot

## Contraintes

- doc-only
- aucun runtime
- aucun push sans instruction explicite
- ne pas modifier `BRANCH_STATE.md` sauf preuve
- ne pas rouvrir `PROJECT_MACHINE_SPLIT`
- ne pas absorber `MULTI_AGENTS_CANON_PARENT`
- ne pas fermer `PARENT_NAMING_CANON` tant que ses enfants ne sont pas reels et clos

## Plan d execution

1. relire les index et les surfaces maitres
2. qualifier l etat reel des GO imposes
3. produire une matrice de decision opposable
4. appliquer seulement les patchs d index necessaires
5. fermer ce lot avec un verdict explicite

## Point de reprise

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_MATRIX_CONSOLIDATION_CLOSEOUT_01/01_go_reading_inventory.md`
