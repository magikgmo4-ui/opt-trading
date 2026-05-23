# GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01

Ajout de la règle de création structurée des GO dans la matrice.

## Objet

- Définir `GO_STRUCTURAL_ROLE` obligatoire.
- Autoriser uniquement : `GO_CHILD`, `GO_CHILD_ATTACHED_TO_PARENT`, `GO_PARENT`, `GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN`, `GO_MASTER_PROJECT_PLAN`.
- Exclure `GO_ORPHAN` comme rôle canonique.
- Imposer `NEXT_ATTACH_TARGET` pour les GO non encore rattachés.
- Confirmer `index global = MASTER_PROJECT_PLAN_INDEX`.

## Livrables

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01.md`
- `docs/chantiers/GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01/00_INITIAL_PROJECT_DOC.md`
- `bundles/GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01/`

## Règle

Cette passe ne migre pas les anciens GO. Elle fixe la règle applicable aux nouvelles ouvertures et aux corrections progressives.
