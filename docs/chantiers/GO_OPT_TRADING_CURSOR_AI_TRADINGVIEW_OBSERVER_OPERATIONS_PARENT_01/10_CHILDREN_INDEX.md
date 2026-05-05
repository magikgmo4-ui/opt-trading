# 10_CHILDREN_INDEX — Children cursor-ai

## Liste des GO children

| # | GO ID | Nom | Statut | Phase |
|---|-------|-----|--------|-------|
| 1 | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_POST_MERGE_REPRISE_01` | Reprise post-merge | **PASS** | 8 |
| 2 | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_SHARED_PACKET_01` | Shared packet Option B | **PASS** | 9 |
| 3 | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_TEMPLATE_01` | Alert webhook template | PENDING | 10 |

## Child 2 — Shared packet Option B — PASS

- Branche : `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_SHARED_PACKET_01`
- Script `export_shared_packet.ps1` cree
- Staging local `_shared_packets/` ignore par git
- Dry-run + export reel PASS
- Aucun transfert admin-trading automatise
- Option B.2 candidat documente (WinSCP manuel futur)

## NEXT_GO immediat

**Phase 10** — `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_TEMPLATE_01`

## NEXT_GO_CANDIDATE (admin-trading)

Parent ADN separe, pas un child de ce parent cursor-ai :

`GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_OBSERVER_PACKET_PARENT_01`

Child unique :

`GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_OBSERVER_PACKET_INGEST_REVIEW_01`

Note : ce parent admin-trading ne doit pas etre ouvert avant que le shared packet (Option B) soit stable ou qu'un besoin admin-trading soit prouve.
