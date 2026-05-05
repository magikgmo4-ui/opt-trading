---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_10_CANONICAL_STATE
doc_type: chantier/canonical_state
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 10_CURSOR_AI_CANONICAL_STATE

## Etat general

Cursor-ai est la machine de preparation, documentation, packaging et gate avant toute application runtime sur admin-trading.

La map cursor-ai est clean en 6 sous-sections :

1. **TradingView MCP Observer — CLOSED (transport/docs)**
2. **alert_webhook — ACTIVE_CONTINUITY**
3. **Bundles — APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED**
4. **Live artifacts / Claude cowork — MERGED**
5. **DOC_OPS — HISTORICAL (branches supprimees en cleanup)**
6. **DOC_OPS — BLOCKED**

## PR mergees

| PR | Objet |
| --- | --- |
| PR #200 | TradingView MCP parent |
| PR #201 | Claude cowork / live artifacts / IDE bundle |
| PR #202 | Bundles application operateur |
| PR #203 | alert_webhook application |
| PR #204 | Machine map stale lines review (derniere mergée) |

## Parent TradingView MCP

- Ferme comme `transport/docs`.
- Branche de closeout mergee.
- Aucune reprise prevue sans demande explicite.

## Admin-trading

- Non ouvert.
- Aucune branche admin-trading creee par cursor-ai.
- Gate explicite maintenue.

## Runtime

- Aucun runtime cursor-ai ouvert ou modifie.
- Aucune alerte reelle declenchee.
- Serveur webhook non touche.
