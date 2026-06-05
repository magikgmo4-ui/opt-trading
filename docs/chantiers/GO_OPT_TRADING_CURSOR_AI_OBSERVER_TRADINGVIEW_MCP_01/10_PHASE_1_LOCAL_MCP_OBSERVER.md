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
| tradingview-mcp | `C:\Users\ghost\.claude\tools\tradingview-mcp` (commit 8dc9dc2, main + PR #76 merged) |
| TradingView Desktop | MSIX v3.1.0.7818, Electron 38.2.2, Chrome 140.0.7339.133 |
| MCP config | `C:\Users\ghost\.claude\.mcp.json` |

## TradingView Desktop — Installation

- **Méthode** : MSIX téléchargé depuis `https://tvd-packages.tradingview.com/stable/latest/win32/TradingView.msix`
- **Installation** : `Add-AppxPackage` Powershell
- **Package** : `TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj`
- **InstallLocation** : `C:\Program Files\WindowsApps\TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj`
- **PackageFamilyName** : `TradingView.Desktop_n534cwy3pjxzj`
- **AUMID** : `TradingView.Desktop_n534cwy3pjxzj!TradingView.Desktop`

## PR #76 — MSIX CDP fix

Le repo `tradingview-mcp` upstream (main) ne supportait pas le lancement MSIX.
PR #76 (`unknowntrader7`, commit `8dc9dc2`) ajoute :
- `scripts/launch_msix.ps1` — COM activation via `IApplicationActivationManager`
- `src/core/health.js` — détection et lancement MSIX automatique
- La PR a été mergée localement (fast-forward) dans notre clone.

Sans cette PR, `tv launch` échoue silencieusement sur MSIX (le .exe ne peut pas recevoir d'arguments en ligne de commande).

## Smokes exécutés

### 1. http://127.0.0.1:9222/json/version — PASS

```json
{
  "Browser": "Chrome/140.0.7339.133",
  "Protocol-Version": "1.3",
  "V8-Version": "14.0.365.4",
  "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/browser/6c4c31d1-..."
}
```

### 2. tv launch (MSIX) — PASS

```json
{
  "success": true,
  "platform": "win32",
  "launch_method": "msix",
  "binary": "TradingView.Desktop_n534cwy3pjxzj!TradingView.Desktop",
  "pid": 211360,
  "cdp_port": 9222,
  "cdp_url": "http://localhost:9222",
  "browser": "Chrome/140.0.7339.133",
  "user_agent": "... TradingView/3.1.0 ... Electron/38.2.2 ..."
}
```

### 3. tv status (health check) — PASS

```json
{
  "success": true,
  "cdp_connected": true,
  "target_url": "https://fr.tradingview.com/chart/",
  "chart_symbol": "TVC:CAC40",
  "chart_resolution": "D",
  "chart_type": 1,
  "api_available": true
}
```

### 4. tv state (chart_get_state) — PASS

```json
{
  "success": true,
  "symbol": "TVC:CAC40",
  "resolution": "D",
  "chartType": 1,
  "studies": []
}
```

### 5. tv quote (quote_get) — PASS

```json
{
  "success": true,
  "symbol": "TVC:CAC40",
  "open": 8122.1,
  "high": 8122.1,
  "low": 7962.76,
  "close": 7976.13,
  "last": 7976.13,
  "description": "CAC 40",
  "exchange": "TVC",
  "type": "index"
}
```

### 6. tv alert list (alert_list) — PASS

```json
{
  "success": true,
  "alert_count": 0,
  "alerts": []
}
```

### 7. tv values (data_get_study_values) — PASS (no studies loaded, expected)

```json
{
  "success": true,
  "study_count": 0,
  "studies": []
}
```

## Résultat

**Statut** : PASS

| Check | Statut |
|-------|--------|
| tradingview-mcp installé | PASS |
| PR #76 MSIX fix appliqué | PASS |
| MCP server démarre | PASS |
| MCP config créée | PASS |
| Claude Code CLI disponible | PASS |
| TradingView Desktop installé | PASS |
| Port 9222 accessible | PASS |
| tv launch (MSIX COM) | PASS |
| tv status / health check | PASS |
| tv state / chart_get_state | PASS |
| tv quote / quote_get | PASS |
| tv alert list / alert_list | PASS |
| tv values / data_get_study_values | PASS |

## Notes

- TradingView Desktop sur Windows est **exclusivement MSIX** (même depuis tradingview.com/desktop/).
- Le lancement CDP nécessite la PR #76 (COM `IApplicationActivationManager`) — le `spawn(exe, [--remote-debugging-port])` natif échoue sur MSIX.
- La PR #76 a été mergée localement dans notre clone `tradingview-mcp`. Si le repo upstream est mis à jour (merge de la PR), il faudra rebase.
- Aucune alerte de production présente (0 alertes). Sécurisé pour les phases suivantes.

## Prochain GO

Phase 2 — Alertes TradingView : inventaire et contrôle
→ `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERTS_INVENTORY_01`

## RISKS

- À qualifier.
