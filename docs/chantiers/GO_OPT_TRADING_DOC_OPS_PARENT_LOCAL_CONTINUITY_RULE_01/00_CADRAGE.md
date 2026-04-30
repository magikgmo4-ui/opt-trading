---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01
status: draft
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - doc_ops
  - parent_chantier
  - local_continuity
  - indexation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01/01_RULE.md
updated_at: 2026-04-30
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01/01_RULE.md
  - docs/index/inbox/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01.md
---

# GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01 — cadrage

## 1_MASTER_TARGET

Formaliser comme methode de travail globale la regle suivante : chaque nouveau parent conserve sa continuite locale dans son propre dossier chantier, avec une entree atomique dans `docs/index/inbox/`, afin d'eviter de modifier les index globaux a chaque micro-avancement.

## 3_INITIAL_NEED

Transformer la regle deja utilisee sur `GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` en methode reutilisable pour les prochains parents.

## 4_MASTER_PROJECT_PLAN

1. Documenter la regle locale parent.
2. Definir quand utiliser le dossier parent, l'inbox et les index globaux.
3. Preparer une future integration dans `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.
4. Ne pas modifier la matrice directement dans ce lot tant que la branche n'est pas realignee.

## 7_CANONICAL_STATE

- Regle appliquee au parent strategy / indicator.
- Besoin de generalisation aux prochains parents.
- Ce chantier documente la methode avant propagation dans la matrice.

## 17_RESUME_POINT

Lire `01_RULE.md`, puis appliquer la regle aux prochains parents et ouvrir un batch d'integration matrice si necessaire.
