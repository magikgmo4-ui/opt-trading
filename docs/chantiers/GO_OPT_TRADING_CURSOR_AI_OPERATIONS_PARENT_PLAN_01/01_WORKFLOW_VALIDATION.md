---
doc_id: OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01_WORKFLOW_VALIDATION
doc_type: workflow_validation_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01
status: active
lifecycle_stage: workflow_validation
topic_keys:
  - cursor-ai
  - bundles
  - alert_webhook
  - claude
  - live_artifacts
  - workflow
surface: chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section 17_RESUME_POINT"
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01.md
---

# Workflow validation — GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01

## 7_CANONICAL_STATE

Parent operatoire `cursor-ai` ouvert sur branche dediee.

Continuites retenues :

| Bloc | Statut retenu | Validation |
| --- | --- | --- |
| `alert_webhook` | `ACTIVE_CONTINUITY` | deja actif, conserver |
| `Bundles` | `ACTIVE_CONTINUITY_TO_VALIDATE_WORKFLOW` | a valider dans workflow, sans runtime |
| `Claude / Live artifacts` | `ACTIVE_CONTINUITY` | actif, conserver |

## 8_VALIDATED_PLAN

1. Ne pas modifier les blocs machines hors `CURSOR_AI`.
2. Ne pas toucher au runtime reel.
3. Garder `alert_webhook` comme application non fermee.
4. Reclasser `Bundles` comme application documentee a valider en continuite active.
5. Reclasser `Claude / Live artifacts` comme continuite active.
6. Garder TradingView MCP Observer, DOC_OPS historical et audit Git comme references non actives.
7. Garder DOC_OPS blocked comme bloc bloque, non rouvert sans GO explicite.

## 9_SELECTED_SOLUTION

Validation documentaire d'abord. Toute action concrete sur `Bundles` devra passer par un child dedie si elle implique un patch workflow ou un changement operatoire.

## 11_KEY_DECISIONS

- `Bundles` n'est pas ferme comme produit : il devient une continuite active a valider.
- `Claude / Live artifacts` n'est pas seulement historique : il reste support actif cursor-ai.
- `alert_webhook` reste actif et rattache au parent cursor-ai.

## 12_INVARIANTS

- Pas de `ClickUp` dans `cursor-ai`.
- Pas d'OpenClaw dans `cursor-ai`.
- Pas d'admin-trading dans `cursor-ai`.
- Pas de runtime touch.
- Pas de secret.

## 16_TODO

- Mettre a jour la matrice machine si un patch complet du fichier est effectue.
- Ajouter le parent au tableau canonique `GO_INDEX.md` lors de l'indexation globale.
- Ouvrir un child seulement si `Bundles` necessite une action concrete.

## 17_RESUME_POINT

Reprendre ici pour le prochain child possible :

`GO_OPT_TRADING_CURSOR_AI_BUNDLES_WORKFLOW_VALIDATION_01`

Objectif child potentiel : valider le workflow `Bundles` cote cursor-ai, sans toucher au runtime ni aux autres machines.
