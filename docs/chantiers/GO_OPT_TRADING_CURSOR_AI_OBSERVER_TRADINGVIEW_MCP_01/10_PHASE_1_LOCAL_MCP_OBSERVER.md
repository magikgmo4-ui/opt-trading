# 10_PHASE_1 — Local MCP Observer

## Objectif

Installer tradingview-mcp hors repo opt-trading sur cursor-ai et valider que Claude Code peut communiquer avec TradingView Desktop.

## Setup cible

- TradingView Desktop lancé avec `--remote-debugging-port=9222`
- Port : `127.0.0.1:9222` uniquement
- tradingview-mcp installé dans : `C:\Users\ghost\.claude\tools\tradingview-mcp`
- Claude Code configuré comme client MCP

## Smokes obligatoires

1. `http://127.0.0.1:9222/json/version` — vérifier que le port CDP répond
2. `chart_get_state` — lire le symbole et timeframe courant
3. `quote_get` — lire OHLC courant
4. `screenshot` — capture d'écran si disponible
5. `data_get_study_values` — lire valeurs d'indicateurs si disponible

## Livrables

- Ce fichier complété avec verdict
- Preuve des commandes exécutées
- Statut : PASS / PARTIAL / FAIL

## Critère PASS

TradingView Desktop est lisible depuis Claude Code via MCP sans exposer de port réseau.

## Résultat

**Statut** : [PASS / PARTIAL / FAIL]

**Détail** :
