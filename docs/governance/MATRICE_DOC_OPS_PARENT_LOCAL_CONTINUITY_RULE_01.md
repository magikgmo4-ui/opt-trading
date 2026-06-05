---
doc_id: OPT_TRADING_MATRICE_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01
doc_type: governance_addendum
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02
status: draft
lifecycle_stage: governance_patch
topic_keys:
  - opt-trading
  - matrice_doc_ops
  - parent_chantier
  - local_continuity
  - index_inbox
surface: governance
source_kind: canonical_candidate
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02/01_PATCH_PROPOSAL.md
updated_at: 2026-04-30
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02/00_CADRAGE.md
---

# MATRICE DOC OPS — règle de continuité locale des parents

## Statut

Addendum gouvernance candidat à intégrer dans `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.

## Règle

Pour tout nouveau chantier parent :

1. La continuité courante est conservée dans `docs/chantiers/<GO_PARENT>/`.
2. Le dossier parent doit contenir le cadrage, le plan ou état courant, les décisions locales, les gaps, les TODO et le point de reprise.
3. Une entrée courte atomique est créée dans `docs/index/inbox/<GO_PARENT>.md`.
4. Les index globaux (`GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md`, `BRANCH_STATE.md`) ne sont pas modifiés à chaque micro-avancement.
5. Les index globaux sont modifiés seulement lors d'un batch d'agrégation, d'une ouverture/fermeture significative, d'un changement de statut global, d'un changement de next GO global ou d'un arbitrage branche.

## Effet attendu

- Réduire les conflits sur les gros index globaux.
- Rendre chaque parent autonome pour la reprise.
- Préserver une trace courte d'agrégation future via `docs/index/inbox/`.
- Empêcher les index globaux de devenir des journaux de session.

## Surface d'application

Cette règle s'applique aux prochains parents, sauf consigne explicite contraire ou cas où la matrice impose une propagation globale immédiate.

## RISKS

- À qualifier.
