---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_20_ACTIVE_GO_LIST
doc_type: chantier/go_list
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/GO_INDEX.md
---

# 20_ACTIVE_GO_LIST

Liste des GO actifs propres a cursor-ai au `2026-05-05`.

## GO actifs

### 1. `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_APPLICATION_ACTIVE_01`

- **Statut** : `ACTIVE_CONTINUITY`
- **PR** : #203 mergee
- **Note** : application webhook active, non fermee produit
- **Machine** : cursor-ai

### 2. `GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01`

- **Statut** : `APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED`
- **PR** : #202 mergee
- **Note** : Bundles application documentee, workflow documente, produit non ferme
- **Machine** : cursor-ai

### 3. `GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01`

- **Statut** : `CANDIDATE`
- **Note** : pack operateur Claude artifacts, prochain axe recommande
- **Machine** : cursor-ai

### 4. `GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01`

- **Statut** : `FUTURE` (non ouvert)
- **Note** : specification de gate avant admin-trading
- **Machine** : cursor-ai

### 5. `GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01`

- **Statut** : `FUTURE` (non ouvert)
- **Note** : fiche unique de reprise operateur cursor-ai
- **Machine** : cursor-ai

## GO fermes

| GO | Statut |
| --- | --- |
| TradingView MCP Observer parent (#200) | CLOSED (transport/docs) |
| Claude cowork parent live artifacts (#201) | MERGED |
| Bundles application operateur (#202) | MERGED |
| Machine map stale lines review (#204) | MERGED |

## Regle

- Aucun GO admin-trading n'est ouvert sans demande explicite.
- Les GO `FUTURE` ne doivent pas etre ouverts avant le verdict du present GO parent.
