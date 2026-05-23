---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
topic_keys:
  - opt-trading
  - collectors
  - coinglass
  - vision
  - headless
  - liquidations
links:
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/20_ACCEPTANCE_REPORT.md
  - docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01.md
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer officiellement la voie Coinglass → bot vision headless → signal/context, sans rouvrir le parent collectors accepté ni implémenter d'adapter API Coinglass runtime.

## 2_PARENT_CONTEXT

Le parent `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01` est **ACCEPTED** (PR #707, 2026-05-23). Il a fermé Coinglass comme `NOT_PROVEN_RUNTIME_ADAPTER` pour la raison suivante : service payant, aucun adapter API runtime viable sans clé.

Ce child de continuité ne remet pas en cause ce verdict. Il documente la **voie alternative officielle** : un bot vision headless externe capture l'interface Coinglass et produit un contrat `vision_context.coinglass.v1` indépendant du collector API.

## 3_DISTINCTION CRITIQUE

| Dimension | collectors API (`market_metrics.v1`) | bot vision headless (`vision_context.coinglass.v1`) |
|---|---|---|
| Source | Endpoint API JSON | Screenshot OCR/vision |
| Authenticité | Donnée structurée | Extraction visuelle |
| Confiance | Haute si PROVEN | Dépend du confidence score |
| Limite | Coinglass = payant | Fragilité visuelle / layout changes |
| Usage Desk Pro | `market_metrics.v1` input | `vision_context` input séparé |

Ces deux contrats ne se mélangent pas et ne se remplacent pas.

## 4_SCOPE

### Autorisé

- Docs uniquement : contrat, schéma, data flow, plan de validation
- Définir `vision_context.coinglass.v1` comme contrat de sortie du bot
- Définir les chemins de stockage
- Définir les patches futurs (schema → parser mock → Desk Pro consumer → runtime gated)

### Interdit

- Adapter Coinglass API runtime
- Contournement du service payant
- Simulation de liquidations/funding/LSR sans preuve visuelle réelle
- DB write, Sheets, Telegram
- Index globaux modifiés
- Mélanger `market_metrics.v1` et `vision_context.coinglass.v1`

## 5_DELIVERABLES

| Fichier | Rôle |
|---|---|
| `10_DECISION_CONTEXT.md` | Contexte de la décision — pourquoi bot vision vs adapter API |
| `20_BOT_VISION_HEADLESS_CONTRACT.md` | Contrat `vision_context.coinglass.v1` |
| `30_DATA_FLOW_AND_STORAGE_PLAN.md` | Chemins de stockage + flux de données |
| `40_VALIDATION_AND_EVIDENCE_PLAN.md` | Plan de tests + critères de confiance |
| `50_NEXT_PATCHES.md` | Roadmap patches A1→B2 |
| `90_REPRISE_POINT.md` | Point de reprise |
| `BRANCH_STATE.md` | Etat de la branche |
