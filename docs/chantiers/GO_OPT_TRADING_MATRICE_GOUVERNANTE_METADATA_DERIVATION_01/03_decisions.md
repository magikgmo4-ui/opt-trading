---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
status: open
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - matrice_gouvernante
  - metadata
  - search_tags
  - decisions
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/01_plan.md
  - docs/index/GO_INDEX.md
---

# 03_decisions — GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01

## Decision

| sujet | constat | decision | justification |
| --- | --- | --- | --- |
| priorite canonique | la matrice V2 est deja canonique | `MATRIX_FIRST_DERIVATION_SECOND` | la structure doit rester au-dessus des derives |
| frontmatter enrichi | peut etre utile pour recroisement et lecture | `ALLOW_PROVABLE_ENRICHMENT_ONLY` | aucun champ derive ne doit inventer une structure absente |
| search tags | utiles pour recherche | `KEEP_SEARCH_TAGS_DERIVED_AND_CONTROLLED` | les tags ne doivent pas gouverner la structure |
| groupes d'objets | utiles comme vues de recroisement | `ALLOW_GROUP_BUCKETS_AS_DERIVED_VIEWS` | eviter toute seconde taxonomie souveraine |
| registry derive | utile comme index machine-readable | `KEEP_REGISTRY_DERIVED_NON_SOVEREIGN` | ne jamais remplacer frontmatter ou matrice |
| reprise | reste fixee par la matrice deja canonisee | `KEEP_REPRISE_OPERATIONAL_ONLY` | aucune regression autorisee |
| branches | hors centre du lot | `KEEP_BRANCH_STATE_BRANCH_SURFACE_ONLY` | aucune elevation de la surface branches |
| cas AI team | limite deja reportee ailleurs | `EXCLUDE_AI_TEAM_SYNC_FROM_THIS_LOT` | le present GO n'ouvre pas le chantier de synchronisation reelle |
| pilote d'application | une campagne large serait prematuree | `PILOT_ONLY_BEFORE_ANY_WIDER_APPLICATION` | figer la doctrine d'abord, tester ensuite sur quelques documents structurants |

## Gardes

- pas de reouverture de la matrice
- pas de correction documentaire reelle hors doctrine
- pas de chantier metadata / tags comme moteur de gouvernance
- pas de requalification de `GO_INDEX.md`, `REPRISE.md`, `BRANCH_STATE.md`
- pas de tagging massif dans ce lot
