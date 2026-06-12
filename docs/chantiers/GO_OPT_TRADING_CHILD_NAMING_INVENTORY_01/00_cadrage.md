---
doc_id: GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: naming_normalizer
go_id: GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - naming
  - inventory
  - audit
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-22
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/NAMING_CANON_POLICY_01.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md
---

# 00_cadrage - GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01

## Identite
- GO : `GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01`
- Repo : `opt-trading`
- Branche : `sot/mainline`
- Statut : `open`
- Type : audit repo-first

## Intention
Recenser les ecarts de nommage reels sans appliquer de correction.

## Objectif du lot
Produire un inventaire borne et classe des ecarts de nommage pour :
- `docs/chantiers`
- `docs/governance`
- `modules`
- scripts
- branches locales si utile

## Plan valide
1. lire la politique canonique
2. executer le module `naming_normalizer`
3. classer les ecarts :
   - canon
   - legacy tolere
   - a corriger plus tard
4. produire un rapport lisible
5. preparer le next GO

## PASS / FAIL
- PASS : un inventaire verifiable existe avec propositions de nommage ou marquage review-required
- FAIL : le chantier derive vers des renommages reels ou des hypotheses non prouvees

## Next GO
- `GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01`

## RISKS

- À qualifier.
