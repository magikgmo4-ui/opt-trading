---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_30_PARENT_PRODUCT_MAP
doc_type: chantier/parent_product_map
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 30_PARENT_AND_PRODUCT_MAP

Table des parents, GO, statuts et produits finaux prevus pour cursor-ai.

| Parent | GO | Statut | Produit final prevu | Etat |
| --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01` | (ce GO) | DOC_ONLY | Plan operateur parent consolide | Actif |
| TradingView MCP parent | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01` | MERGED | Observateur docs | CLOSED (transport/docs) |
| alert_webhook parent | `GO_OPT_TRADING_CURSOR_AI_..._ALERT_WEBHOOK_APPLICATION_ACTIVE_01` | ACTIVE_CONTINUITY | Application webhook | Application non fermee |
| Bundles doc parent | `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | MERGED | Documentation Bundles | MERGED |
| Bundles application | `GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01` | DOCUMENTED | Workflow Bundles | Produit non ferme |
| Claude cowork parent | `GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | MERGED | Live artifacts IDE bundle | MERGED |
| Claude artifacts (candidat) | `GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01` | CANDIDATE | Pack operateur Claude artifacts | Non ouvert |
| alert_webhook gate | `GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01` | FUTURE | Spec gate admin-trading | Non ouvert |
| Reprise operateur | `GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01` | FUTURE | Fiche reprise cursor-ai | Non ouvert |

## Produits finaux prevus

1. **Plan operateur parent** — `PARENT_OPERATIONAL_PLAN_01`
2. **Pack operateur Claude artifacts** — `CLAUDE_ARTIFACTS_OPERATOR_PACK_01`
3. **Bundles produit final** — `BUNDLES_APPLICATION_ACTIVE_01` (reprise)
4. **Spec gate admin-trading** — `ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01`
5. **Fiche reprise operateur** — `OPERATOR_REPRISE_PACKET_01`
