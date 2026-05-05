# 10_PHASE_1 — Local MCP Observer

## Objectif

Installer tradingview-mcp hors repo opt-trading sur cursor-ai et valider que Claude Code peut communiquer avec TradingView Desktop.

## Contexte exécution

- **Date** : 2026-05-04
- **Machine** : cursor-ai (Windows)
- **Branche** : `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01`

## Environnement

| Outil | Version / Chemin |
|-------|-----------------|
| OS | Windows (win32) |
| Git | 2.53.0.windows.2 |
| Node.js | v24.14.0 |
| npm | 11.9.0 |
| Claude Code CLI | `C:\Users\ghost\.local\bin\claude.exe` |
| tradingview-mcp | `C:\Users\ghost\.claude\tools\tradingview-mcp` (commit 4795784, branch main) |
| TradingView Desktop | **NON INSTALLÉ** sur cursor-ai |

## Setup cible

- TradingView Desktop lancé avec `--remote-debugging-port=9222`
- Port : `127.0.0.1:9222` uniquement
- tradingview-mcp installé dans : `C:\Users\ghost\.claude\tools\tradingview-mcp`
- Claude Code configuré comme client MCP

## Smokes exécutés

### 1. http://127.0.0.1:9222/json/version — FAIL

Port 9222 non accessible. Aucune connexion (TradingView Desktop n'est pas installé).

```
Port 9222 not reachable: No connection could be made because
the target machine actively refused it. (127.0.0.1:9222)
```

### 2. chart_get_state — BLOCKED (TV absent)

### 3. quote_get — BLOCKED (TV absent)

### 4. screenshot — BLOCKED (TV absent)

### 5. data_get_study_values — BLOCKED (TV absent)

### 6. MCP server start — PASS

Le serveur MCP démarre correctement et affiche le message d'avertissement standard :

```
⚠  tradingview-mcp  |  Unofficial tool. Not affiliated with TradingView Inc. or Anthropic.
   Ensure your usage complies with TradingView's Terms of Use.
```

Le serveur attend les messages MCP sur stdin/stdout et est fonctionnel comme processus.

## Installation tradingview-mcp

- Cloné depuis `https://github.com/tradesdontlie/tradingview-mcp.git`
- 94 packages npm installés
- 68 outils MCP disponibles dans le serveur (cf CLAUDE.md)
- Script de lancement Windows : `scripts/launch_tv_debug.bat`
- Emplacements vérifiés par le script : `%LOCALAPPDATA%\TradingView`, `%PROGRAMFILES%\TradingView`, `WindowsApps`

## TradingView Desktop — Recherche

Emplacements vérifiés (tous vides) :
- `C:\Users\ghost\AppData\Local\TradingView\`
- `C:\Program Files\TradingView\`
- `C:\Program Files (x86)\TradingView\`
- `C:\Program Files\WindowsApps\TradingView*\`
- `HKCU/HKLM App Paths`
- `C:\Users\ghost\AppData\Local\Programs\`

**TradingView Desktop n'est pas installé sur cursor-ai.**

## Configuration MCP

Fichier créé : `C:\Users\ghost\.claude\.mcp.json`

```json
{
  "mcpServers": {
    "tradingview-desktop": {
      "command": "node",
      "args": ["C:\\Users\\ghost\\.claude\\tools\\tradingview-mcp\\src\\server.js"]
    }
  }
}
```

Aucun fichier existant n'a été écrasé (le fichier n'existait pas avant).

## Résultat

**Statut** : PARTIAL

| Check | Statut |
|-------|--------|
| tradingview-mcp installé | PASS |
| npm install OK | PASS |
| MCP server démarre | PASS |
| MCP config créée | PASS |
| Claude Code CLI disponible | PASS |
| TradingView Desktop installé | **FAIL** |
| Port 9222 accessible | **FAIL** |
| chart_get_state | BLOCKED |
| quote_get | BLOCKED |
| screenshot | BLOCKED |
| data_get_study_values | BLOCKED |

## Causes du PARTIAL

- TradingView Desktop n'est pas installé sur la machine cursor-ai.
- Tous les outils MCP sont installés et prêts côté serveur, mais le endpoint CDP (127.0.0.1:9222) n'existe pas.
- Le blocage est purement logiciel (absence du binaire TradingView.exe).

## Actions requises pour débloquer

1. Installer TradingView Desktop sur cursor-ai depuis https://www.tradingview.com/desktop/
2. Lancer TradingView Desktop avec `--remote-debugging-port=9222`
3. Vérifier `http://127.0.0.1:9222/json/version`
4. Relancer Claude Code pour charger le serveur MCP
5. Exécuter `tv_health_check` ou `chart_get_state`

## Prochain GO recommandé

Installer TradingView Desktop sur cursor-ai, puis relancer le smoke Phase 1.
Le chantier documentaire et l'installation MCP sont prêts. Seul le runtime TradingView manque.
