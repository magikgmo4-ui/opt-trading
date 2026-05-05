# 01_INITIAL_PROJECT_DOC — GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01

## 1_MASTER_TARGET

Créer une capacité durable TradingView Desktop Observer pour opt-trading, pilotable par Claude Code puis OpenClaw, capable de lire le graphique, les indicateurs visibles, les alertes, et produire des sorties structurées JSON/MD, sans remplacer le webhook TradingView admin-trading.

## 2_INITIAL_PROJECT_DOC

Ce document est la référence initiale figée du chantier.
Il décrit le plan complet de la phase 1 au produit final.
Il ne doit être modifié que si le besoin projet change explicitement.

## 3_INITIAL_NEED

Le besoin initial est de ne plus dépendre d'une vérification manuelle fragile dans TradingView Desktop.
Le système doit pouvoir :
- lire l'état du graphique ;
- lire les symboles/timeframes ;
- lire les valeurs d'indicateurs visibles ;
- lister les alertes ;
- préparer ou auditer des alertes ;
- exporter une preuve structurée ;
- être orchestrable par OpenClaw.

## 4_MASTER_PROJECT_PLAN

- **Phase 1** — MCP local observer sur cursor-ai (smoke et validation MCP)
- **Phase 2** — inventaire et contrôle des alertes TradingView
- **Phase 3** — wrapper opt-trading en lecture seule (modules/tradingview_observer)
- **Phase 4** — intégration OpenClaw comme skill contrôlé
- **Phase 5** — pont optionnel vers admin-trading / desk
- **Phase 6** — hardening produit (logs, timeouts, détection, verrous)
- **Phase 7** — produit final exploitable

## 12_INVARIANTS

- TradingView webhook admin-trading reste canonique.
- tradingview-mcp est observer/configurateur, pas runtime principal.
- Port 9222 local seulement (`127.0.0.1`).
- Aucun trade réel.
- Pas de mutation runtime sans validation.
- Tout résultat doit produire une trace (export JSON/MD).
- Secrets, .env, tokens jamais commités.
