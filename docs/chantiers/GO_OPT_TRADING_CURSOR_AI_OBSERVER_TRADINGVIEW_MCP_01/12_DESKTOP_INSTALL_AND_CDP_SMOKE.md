# 12_DESKTOP_INSTALL_AND_CDP_SMOKE — Log détaillé

## 13_ESTABLISHED

- TradingView Desktop installé : MSIX v3.1.0.7818 (Electron 38.2.2, Chrome 140)
- Méthode d'installation : téléchargement direct MSIX → `Add-AppxPackage`
- Package : `TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj`
- AUMID : `TradingView.Desktop_n534cwy3pjxzj!TradingView.Desktop`
- Port 9222 ouvert et fonctionnel
- CDP répond : Chrome/140, Protocol 1.3, WebSocket debugger URL présente
- MCP connecté : cdp_connected=true, chart_symbol=TVC:CAC40, api_available=true
- PR #76 mergée localement dans tradingview-mcp (commit 8dc9dc2)

## 14_HYPOTHESIS

- **Confirmée** : MSIX bloque `spawn(exe, [--remote-debugging-port])` natif → nécessite COM `IApplicationActivationManager`
- **Confirmée** : PR #76 débloque le lancement CDP sur MSIX via `tv launch`
- **Confirmée** : Aucun script externe (.bat, .vbs) requis — `tv launch` CLI fonctionne directement
- **Vérifiée** : La version MSIX de TradingView Desktop supporte CDP si lancée via le COM API

## 15_REMAINING_GAP

Aucun gap bloquant. La Phase 1 est PASS.

Points à surveiller pour les phases suivantes :
- `tv_launch` est un outil MCP, pas une commande CLI (`tv launch` est le CLI)
- La MCP config (`~/.claude/.mcp.json`) pointe vers `src/server.js` — à vérifier que Claude Code charge bien le serveur après `tv launch`
- tradingview-mcp doit être à jour avec PR #76. Si le repo upstream est recloné, il faudra remerger.

## 16_TODO

- Phase 2 : inventaire et contrôle des alertes TradingView
- Vérifier la config MCP Claude Code complète (chargement automatique du serveur)
- Tester `tv screenshot` pour capture visuelle

## VERDICT

**PASS**

## RISKS

- À qualifier.
