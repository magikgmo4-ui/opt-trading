---
doc_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01_README
doc_type: chantier_parent_readme
repo: opt-trading
project: opt-trading
module: botpress_operator
go_id: GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01
status: open
lifecycle_stage: cadrage
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - botpress
  - telegram
  - openclaw
  - student
  - trading_labs
  - lona
  - opt_trading
  - orchestration
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/00_cadrage_parent.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/01_recherche_botpress.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/02_architecture_cible.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/03_plan_implementation_execution.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/05_safety_gate.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/BRANCH_STATE.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/CHECKPOINT_PARENT.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/GAP_INDEXATION.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/SESSION_REPRISE.txt
---

# GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01

## 1_MASTER_TARGET

Ouvrir un chantier parent autonome pour utiliser Botpress comme couche d'orchestration conversationnelle du pipeline trading :

```text
Telegram Screener
→ Botpress Operator
→ OpenClaw Gateway
→ student / Trading Labs
→ LONA Trading Assistant
→ opt-trading
→ retour Telegram
```

## 2_INITIAL_PROJECT_DOC

Ce dossier est le document transporteur initial du chantier. Il fige le plan parent V1 et reste la référence de reprise hors session.

## 3_INITIAL_NEED

Documenter intégralement l'utilisation de Botpress pour l'écosystème `opt-trading`, ouvrir une branche dédiée et produire un plan complet d'implémentation/exécution indépendant de la conversation.

## 4_MASTER_PROJECT_PLAN

Botpress n'est pas la source métier. Il devient le routeur conversationnel contrôlé : classification d'intention, safety gate, appels API, formatage réponse, journalisation d'événements.

## 5_GO_PLAN

- GO_CHILD_01 : figer intentions et workflows Botpress.
- GO_CHILD_02 : exposer OpenClaw Gateway local.
- GO_CHILD_03 : connecter Telegram Screener et routage image/message.
- GO_CHILD_04 : brancher student / Trading Labs / LONA.
- GO_CHILD_05 : journaliser dans opt-trading.
- GO_CHILD_06 : smoke end-to-end sans trade réel.

## 6_FINAL_TARGET

Un Botpress Operator V1 capable de recevoir une demande Telegram, classifier l'intention, appeler OpenClaw, déléguer vers les surfaces trading, retourner un verdict structuré et journaliser la trace.

## 7_CANONICAL_STATE

Chantier parent ouvert sur branche dédiée : `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01`.

## 12_INVARIANTS

- Pas de trade réel automatique en V1.
- Pas de push Git automatique depuis Botpress.
- Pas de modification production sans validation humaine.
- Pas de logique trading canonique dupliquée dans Botpress.
- `opt-trading` reste la source de vérité.

## 17_RESUME_POINT

Reprendre par `SESSION_REPRISE.txt`, puis lire `00_cadrage_parent.md`, `03_plan_implementation_execution.md` et `04_api_contract_openclaw_gateway.md`.

## RISKS

- À qualifier.
