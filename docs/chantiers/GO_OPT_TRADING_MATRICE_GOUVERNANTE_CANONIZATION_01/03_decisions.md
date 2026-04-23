---
doc_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01
status: pass
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - governance
  - matrice_gouvernante
  - canonization
  - decisions
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/INDEX.md
---

# 03_decisions — GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01

## Decision

| sujet | constat | decision | justification |
| --- | --- | --- | --- |
| surface canonique | la matrice V2 existe dans le bundle clos mais pas encore en surface canonique repo | `PROMOTE_TO_GOVERNANCE` | `docs/governance/` est la bonne couche pour une regle stable de structure |
| verite de liste | la matrice bundle retenait deja `GO_INDEX.md` comme verite de liste | `KEEP_GO_INDEX_AS_LIST_AUTHORITY` | aucune regression autorisee sur la souverainete de liste |
| reprise | la matrice bundle releguait deja `REPRISE.md` au role operatoire | `KEEP_REPRISE_AS_OPERATIONAL_SURFACE_ONLY` | eviter toute seconde verite de liste |
| branches | la matrice bundle limitait `BRANCH_STATE.md` a la surface branches | `KEEP_BRANCH_STATE_BRANCH_SURFACE_ONLY` | ne pas transformer l'etat branches en doctrine generale |
| metadata / tags | le lot demande explicitement de ne pas lancer ce chantier | `DEFER_METADATA_TAGS_RESEARCH` | les derives viennent apres la structure |
| cas AI team | limite deja bornee dans le bundle clos | `KEEP_AI_TEAM_LIMIT_AS_REPORTED` | reserve locale non bloquante, a ne pas rouvrir ici |
| indexation | le GO est canonise et clos dans le meme lot | `REGISTER_IN_GO_CLOSED_INDEX` | respecter la separation GO ouvert / GO clos |

## Gardes

- aucune reouverture des PASS du bundle
- aucune correction de fond de la matrice apres promotion
- aucune elevation de `REPRISE.md` dans le noyau
- aucune elevation de `BRANCH_STATE.md` au-dessus de la surface branches
- aucune activation du chantier metadata / tags / recherche
