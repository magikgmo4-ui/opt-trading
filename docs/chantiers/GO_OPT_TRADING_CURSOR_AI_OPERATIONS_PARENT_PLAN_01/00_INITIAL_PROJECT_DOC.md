---
doc_id: OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01
status: active
lifecycle_stage: parent_opening
topic_keys:
  - opt-trading
  - cursor-ai
  - operations
  - bundles
  - alert_webhook
  - claude
  - live_artifacts
surface: chantiers
source_kind: canonical
reference_canonique_principale: docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
point_de_reprise: "Section 17_RESUME_POINT"
updated_at: 2026-05-06
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/GO_INDEX.md
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01.md
---

# GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01

## 1_MASTER_TARGET

Parent operatoire `cursor-ai` pour regrouper les chantiers et continuites actives propres a la machine `cursor-ai`, sans melanger les blocs `admin-trading`, `db-layer`, `student` et `fantome`.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de reference initiale du parent.

Il fige le plan valide par l'utilisateur :

- `Bundles` passe en continuite active a valider dans la matrice / workflow.
- `alert_webhook` reste en continuite active.
- `Claude / Live artifacts` passe en continuite active.
- Le reste du bloc `cursor-ai` est valide comme reference, historique, closed ou blocked selon la fiche machine.

## 3_INITIAL_NEED

Clarifier les chantiers a placer dans le bloc `cursor-ai` et creer un parent dedie :

`GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01`

## 4_MASTER_PROJECT_PLAN

Le parent `cursor-ai` doit servir de plan operatoire local pour :

1. garder un point de pilotage unique pour les surfaces `cursor-ai` ;
2. distinguer les continuites actives des historiques fermes ;
3. eviter de rouvrir les branches fermees ou supprimees ;
4. eviter de deplacer des chantiers appartenant a `admin-trading`, `db-layer`, `student` ou `fantome`.

## 5_GO_PLAN

### Continuites actives rattachees

| Bloc | Statut retenu | Effet |
| --- | --- | --- |
| `alert_webhook` | `ACTIVE_CONTINUITY` | application non fermee, suivi cursor-ai |
| `Bundles` | `ACTIVE_CONTINUITY_TO_VALIDATE_WORKFLOW` | application documentee, a valider dans matrice / workflow |
| `Claude / Live artifacts` | `ACTIVE_CONTINUITY` | support artefacts / IDE / cowork a garder actif |

### References validees hors actif

| Bloc | Statut retenu |
| --- | --- |
| `TradingView MCP Observer` | `CLOSED` |
| `DOC_OPS — HISTORICAL` | `REFERENCE_HISTORY` |
| `DOC_OPS — BLOCKED` | `BLOCKED` |
| `CURSOR_AI — References audit Git` | `REFERENCE_AUDIT` |

## 6_FINAL_TARGET

Livrer une structure documentaire parent pour `cursor-ai`, raccordee a la matrice machine et a `GO_INDEX`, permettant de reprendre les trois continuities actives sans re-arbitrage global.

## 7_CANONICAL_STATE

- Source de routage machine : `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`.
- Bloc concerne : `CURSOR_AI`.
- Parent cree : `GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01`.
- Branche dediee : `go/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01`.
- Runtime touche : non.
- Machines hors perimetre : `admin-trading`, `db-layer`, `student`, `fantome`.

## 8_VALIDATED_PLAN

1. Creer le dossier chantier parent.
2. Ajouter l'entree inbox courte.
3. Mettre a jour le bloc `CURSOR_AI` pour marquer `Bundles`, `alert_webhook` et `Claude / Live artifacts` en continuite active.
4. Ajouter le parent dans `GO_INDEX` comme `ACTIVE`.
5. Ne pas modifier les autres machines.

## 9_SELECTED_SOLUTION

Patch documentaire minimal sur la branche dediee existante.

## 10_SELECTED_SETUP

- Support Git : `go/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01`.
- Surface principale : `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01/`.
- Surface de routage : `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`.
- Surface de liste : `docs/index/GO_INDEX.md`.
- Inbox courte : `docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01.md`.

## 11_KEY_DECISIONS

- `alert_webhook` est actif.
- `Bundles` est a valider comme continuite active dans matrice / workflow.
- `Claude / Live artifacts` est actif.
- Le reste du bloc est valide comme non-actif sauf `DOC_OPS — BLOCKED`.

## 12_INVARIANTS

- Ne pas deplacer `ClickUp` dans `cursor-ai` : il reste cote `fantome`.
- Ne pas deplacer OpenClaw dans `cursor-ai` : il reste cote `db-layer`.
- Ne pas ouvrir de runtime admin-trading depuis ce parent.
- Ne pas transformer une branche supprimee en chantier actif.

## 13_ESTABLISHED

- Le bloc `CURSOR_AI` existe dans la fiche machine.
- Les blocs `alert_webhook`, `Bundles`, `Claude / Live artifacts`, `DOC_OPS` et audit Git y sont deja listes.
- L'utilisateur a valide le reste du classement.

## 14_HYPOTHESIS

- Le detail workflow a appliquer pour `Bundles` devra etre precise dans un GO child ou une passe dediee si une modification runtime/workflow est requise.

## 15_REMAINING_GAP

- Validation fine de `Bundles` dans la matrice / workflow.
- Definition du premier child actif du parent si une action concrete doit suivre.

## 16_TODO

- Reprendre depuis ce parent.
- Ouvrir un child si besoin pour `Bundles` workflow validation.
- Garder `alert_webhook` et `Claude / Live artifacts` en continuite active sans toucher aux machines hors perimetre.

## 17_RESUME_POINT

Reprendre sur `GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01` depuis la branche `go/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01`.

Prochain geste logique : valider `Bundles` dans la matrice / workflow via un child dedie, sans modifier le runtime.

## 18_TO_DOCUMENT

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/index/GO_INDEX.md`
- `docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01.md`

## 19_TO_REMEMBER

- `cursor-ai` a un parent operatoire dedie : `GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01`.
- Continuites actives du parent : `alert_webhook`, `Bundles`, `Claude / Live artifacts`.
