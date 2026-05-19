# 11_PHASE_1_SMOKE_LOG — Log technique

## Commandes exécutées et résultats

### Git

```powershell
git fetch origin
git checkout go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01
git pull --rebase origin go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01
```

Résultat : branch up to date, clean.

### Outils

```powershell
git --version    # 2.53.0.windows.2
node --version   # v24.14.0
npm --version    # 11.9.0
```

### Installation tradingview-mcp

```powershell
New-Item -ItemType Directory -Force C:\Users\ghost\.claude\tools
cd C:\Users\ghost\.claude\tools
git clone https://github.com/tradesdontlie/tradingview-mcp.git
cd tradingview-mcp
npm install
```

Résultat : 94 packages, commit 4795784 (main), npm 11.9.0.

### Recherche TradingView Desktop

```powershell
# Aucun résultat dans :
Get-ChildItem "$env:LOCALAPPDATA\TradingView"            # vide
Get-ChildItem "C:\Program Files\TradingView"              # vide
Get-ChildItem "${env:ProgramFiles(x86)}\TradingView"       # vide
Get-ChildItem "C:\Program Files\WindowsApps\TradingView*" # vide
registry "App Paths\TradingView.exe"                      # absent
```

### Test port 9222

```powershell
Invoke-WebRequest http://127.0.0.1:9222/json/version -TimeoutSec 3
```

Résultat : connexion refusée (aucun processus sur ce port).

### Test MCP server start

```powershell
node src/server.js  # démarré puis killé après 5s
```

Résultat : démarrage OK, avertissement standard affiché. Serveur fonctionnel.

### Configuration MCP

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

## Verdict final

**PARTIAL** — L'infrastructure MCP est installée et fonctionnelle. Le serveur tradingview-mcp démarre. Seul le runtime TradingView Desktop manque sur cursor-ai pour activer les smokes CDP.

Prochaine étape : installer TradingView Desktop → relancer smoke Phase 1 → passer à la Phase 2.
