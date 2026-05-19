# 00_START — GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_SHARED_PACKET_01

## Role

Phase 9 — Child 2 du parent machine cursor-ai. Prepare l'Option B : export du bridge packet V1 vers un dossier partage local, sans ingestion admin-trading automatique.

## References

| Champ | Valeur |
|-------|--------|
| Parent machine | `GO_OPT_TRADING_MACHINE_CURSOR_AI_PARENT_01` |
| Child precedent | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_POST_MERGE_REPRISE_01` (PASS) |
| Produit ferme | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01` |
| Decision Phase 5 | Option A (local manuel) → cette phase active Option B preparee |
| Phase | 9 — Shared packet Option B |

## Objectif

Ajouter un script d'export safe `export_shared_packet.ps1` qui depose le bridge packet V1 dans un dossier de staging local, sans jamais transferer automatiquement vers admin-trading ou SFTP.

## Statut

OPEN → PASS attendu apres execution.
