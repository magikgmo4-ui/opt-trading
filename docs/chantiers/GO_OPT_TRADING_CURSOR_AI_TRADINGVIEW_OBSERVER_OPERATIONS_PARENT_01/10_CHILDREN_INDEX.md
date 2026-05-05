# 10_CHILDREN_INDEX — Children cursor-ai

## Liste des GO children

| # | GO ID | Nom | Statut | Phase |
|---|-------|-----|--------|-------|
| 1 | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_POST_MERGE_REPRISE_01` | Reprise post-merge | **PASS** | 8 |
| 2 | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_SHARED_PACKET_01` | Shared packet Option B | PENDING | 9 |
| 3 | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_TEMPLATE_01` | Alert webhook template | PENDING | 10 |

## Child 1 — Reprise post-merge — PASS

- Branche : `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_POST_MERGE_REPRISE_01`
- Source de verite confirmee : `sot/mainline`
- Modules produits presents
- Commandes operateur documentees
- Smoke leger : PASS (CDP ouvert, sanity 9/9, snapshot 5/5, OC 9/9)
- Aucun output live committe

## NEXT_GO immediat

**Phase 9** — `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_SHARED_PACKET_01`

## NEXT_GO_CANDIDATE (admin-trading)

Parent ADN separe, pas un child de ce parent cursor-ai :

`GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_OBSERVER_PACKET_PARENT_01`

Child unique :

`GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_OBSERVER_PACKET_INGEST_REVIEW_01`

Note : ce parent admin-trading ne doit pas etre ouvert avant que le shared packet (Option B) soit stable ou qu'un besoin admin-trading soit prouve.
