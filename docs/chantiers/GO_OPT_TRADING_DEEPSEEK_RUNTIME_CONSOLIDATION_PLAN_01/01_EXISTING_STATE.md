---
doc_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01_EXISTING_STATE
doc_type: existing_state
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_state
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
topic_keys:
  - opt-trading
  - deepseek
  - existing-state
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/01_EXISTING_STATE.md
point_de_reprise: "Documenter l'etat existant du cluster DeepSeek."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01/01_DEEPSEEK_CLUSTER_INVENTORY.md
---

# 01_EXISTING_STATE

## 1_SURFACES DU CLUSTER

| Surface | Emplacement | Role | Etat |
|---|---|---|---|
| deepseek_hub | modules/deepseek_hub/ | facade unifiee | survivant candidat |
| deepseek_student | modules/deepseek_student/ | transition incomplete | non runtime |
| deepseek_response | modules/deepseek_response/ | reponses finales | compat |
| deepseek_thinking | modules/deepseek_thinking/ | thinking chain | compat |
| scripts/student/ | scripts/student/ | runtime legacy | legacy actif |
| student/ | student/ | workspace canonique | cible |

## 2_DECISIONS DEJA FIXEES (PR #252)

```text
Point d'entree canonique operateur : student/
Facade module survivante candidate : modules/deepseek_hub/
Satellites de compatibilite : modules/deepseek_response/, modules/deepseek_thinking/
Transition incomplete : modules/deepseek_student/
Legacy a resorber : scripts/student/
```

## 3_CROSS-REFERENCES RUNTIME

```text
scripts/post_change.sh
  - appelle cmd-deepseek_response et cmd-deepseek_thinking

modules/workflow_post_change_v2/
  - appelle aussi ces commandes

modules/deepseek_hub/patches/
  - patch deepseek_response_cmd.sh et deepseek_thinking_cmd.sh

modules/deepseek_hub/scripts/apply_patches.sh
  - backup + patch des cmd existants

student/scripts/
  - deepseek_hub/ scripts dupliques
  - deepseek_student/ scripts dupliques
  - wrappers/ compatibilite
```

## 4_DOUBLONS CONNUS

```text
student/scripts/deepseek_hub/       vs modules/deepseek_hub/scripts/
student/scripts/deepseek_student/   vs modules/deepseek_student/scripts/
student/scripts/wrappers/           vs scripts/student/
scripts/student/                    vs student/scripts/
```

## 5_LIMITES CONNUES

```text
- pas de scheduling autonome fiable (daily-ai-report timer optionnel)
- scripts legacy utilisent encore des chemins absolus /opt/trading
- post_change workflow non teste apres migration
- pas de validation que les patches deepseek_hub sont appliques partout
```
