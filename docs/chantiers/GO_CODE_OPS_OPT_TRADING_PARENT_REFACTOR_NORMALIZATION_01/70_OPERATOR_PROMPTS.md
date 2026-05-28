---
doc_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01_OPERATOR_PROMPTS
doc_type: operator_prompts
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: execution_support
topic_keys:
  - go_prompt
  - cursor_ai
  - ide
  - operator
  - code_ops
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 70_OPERATOR_PROMPTS

## GO_PROMPT — ouverture du premier sous-GO inventaire

ROLE: Code Ops / Repo Inventory Operator

GO_PARENT:
GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01

NEXT_GO:
GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01

OBJECTIF:
Produire l'inventaire réel du code opt-trading avant tout refactor.

CONTRAINTES:
- Ne modifier aucun code.
- Ne supprimer aucun fichier.
- Ne renommer aucun fichier.
- Ne modifier aucun index global.
- Partir de origin/sot/mainline à jour ou de la branche dédiée validée.
- Lire docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md.
- Lire docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/00_INITIAL_PROJECT_DOC.md.
- Appliquer le protocole docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/10_CODE_INVENTORY_PROTOCOL.md.

LIVRABLES:
- docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/00_INITIAL_PROJECT_DOC.md
- docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/10_FILE_INVENTORY.md
- docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/20_ENTRYPOINTS.md
- docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/30_VALIDATORS_AND_SCHEMAS.md
- docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/40_RISK_MAP.md
- docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/50_NEXT_REGISTRY_INPUT.md

VERDICT:
PASS_INVENTORY_READY ou BLOCKED_WITH_REASON.

---

## GO_PROMPT — registre initial

ROLE: Code Ops / Registry Builder

GO_PARENT:
GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01

INPUT:
Résultats du sous-GO GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01.

OBJECTIF:
Créer un registre initial du code à partir de l'inventaire réel.

CONTRAINTES:
- Ne pas inventer de chemins.
- Marquer unknown quand un consommateur est incertain.
- Ne pas déprécier sans preuve.
- Ne pas supprimer.
- Respecter docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/20_CODE_REGISTRY_SPEC.md.

LIVRABLES:
- registre initial Markdown ou JSON
- table des champs manquants
- liste des éléments high-risk
- proposition de validateur si utile

VERDICT:
PASS_REGISTRY_DRAFT_READY ou BLOCKED_WITH_REASON.

---

## GO_PROMPT — audit anti-doublon

ROLE: Code Ops / Dedup Auditor

GO_PARENT:
GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01

OBJECTIF:
Qualifier les doublons suspects sans suppression.

CONTRAINTES:
- Lire le registre initial.
- Lire docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/30_DEDUP_AUDIT_PROTOCOL.md.
- Un doublon suspect n'est pas une suppression.
- Identifier les consommateurs avant toute décision.
- Sortir une matrice de décision.

VERDICT:
PASS_DEDUP_AUDIT_READY ou BLOCKED_WITH_REASON.

---

## GO_PROMPT — compatibilité

ROLE: Code Ops / Compatibility Auditor

GO_PARENT:
GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01

OBJECTIF:
Renseigner la matrice de compatibilité des surfaces réellement utilisées.

CONTRAINTES:
- Ne pas modifier le code.
- Ne pas déclarer compatible sans preuve.
- Différencier Bash, PowerShell, WSL, tmux, GitHub Actions et lecture mobile.
- Marquer N/A si une surface n'est pas concernée.

VERDICT:
PASS_COMPATIBILITY_MATRIX_READY ou BLOCKED_WITH_REASON.

---

## Note opératoire

Ce parent fixe le cadre. Les commandes terminal complètes doivent être produites et validées dans les sous-GO, selon l'environnement réel de la machine utilisée.