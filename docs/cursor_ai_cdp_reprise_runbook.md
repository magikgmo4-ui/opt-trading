# cursor-ai — Reprise CDP TradingView

Runbook de reprise après logoff/logon sur cursor-ai pour rétablir CDP (port 9222)
et valider le pipeline TVOrchestratorAgent → tradingview-mcp → TradingView Desktop.

## Contexte

TradingView Desktop (MSIX) nécessite `--remote-debugging-port=9222` au démarrage
pour exposer le CDP. La variable `ELECTRON_EXTRA_LAUNCH_ARGS` doit être dans le
token utilisateur Windows, pas seulement dans le registre. Un logoff/logon recharge
le token → la variable est active → le VBS fonctionne.

Variable persistante (déjà en place) :
```
HKCU\Environment\ELECTRON_EXTRA_LAUNCH_ARGS = --remote-debugging-port=9222
```

---

## Étapes post-logon

### 1. Lancer TradingView avec CDP

Double-clique `TradingView_CDP.vbs` sur le bureau.

> Si TV était déjà ouvert avant le VBS : fermer TV, relancer le VBS.

Vérification :
```powershell
(Test-NetConnection localhost -Port 9222 -WarningAction SilentlyContinue).TcpTestSucceeded
# → True
```

### 2. Vérifier tradingview-mcp

```powershell
node C:\Users\ghost\.claude\tools\tradingview-mcp\src\cli\index.js status
# → { success: true, symbol: "...", price: ... }
```

### 3. Vérifier TVOrchestratorAgent

```powershell
schtasks /query /tn TVOrchestratorAgent /fo list | Select-String "État"
# → En cours d'exécution
```

Si arrêté :
```powershell
Stop-ScheduledTask  -TaskName TVOrchestratorAgent
Start-ScheduledTask -TaskName TVOrchestratorAgent
```

### 4. Pull sot/mainline (sans quitter la branche YouTube)

```powershell
cd C:\Users\ghost\opt-trading
git fetch origin
git branch -f sot/mainline origin/sot/mainline
git branch --show-current
# → go/GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
```

### 5. Test E2E snapshot depuis Linux

```bash
# Sur db-layer (Linux)
python3 modules/tradingview_orchestrator/app/tv_runner.py \
  modules/tradingview_orchestrator/jobs/examples/tv_job_snapshot.json
# → status: done, quote + alertes présentes
```

---

## Recréer l'alerte SpaceX Wire (si stoppée)

L'alerte `#4917725195` peut s'arrêter après une migration tunnel ou un redémarrage TV.
Job packet : `modules/tradingview_orchestrator/jobs/spacex_wire_alert.json`

```bash
# Sur db-layer — CDP doit être UP sur cursor-ai
python3 modules/tradingview_orchestrator/app/tv_runner.py \
  modules/tradingview_orchestrator/jobs/spacex_wire_alert.json --gate-approved
```

Vérification :
```bash
grep SPACEX_WIRE state/events.jsonl | tail -1
```

---

## Pourquoi le VBS ne passe pas via SSH

`explorer.exe shell:AppsFolder\...` via SSH crée un process dans la session
non-interactive (Session 0), pas sur le bureau. TradingView ne s'ouvre pas.
Le lancement doit toujours être fait depuis la session desktop interactive.

---

## État des machines au 2026-06-12

| Machine | Branch | HEAD |
|---|---|---|
| Linux (`db-layer`) | `sot/mainline` | `08537c73` |
| cursor-ai | `go/GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01` | `db79b16a` |

Runtime Linux : 9/9 tmux sessions UP — `all_ok=true` (LocalCMS `/runtime/tmux`).

---

## Référence — variables persistantes cursor-ai

| Variable | Valeur | Scope |
|---|---|---|
| `ELECTRON_EXTRA_LAUNCH_ARGS` | `--remote-debugging-port=9222` | User (HKCU) |

Ne pas supprimer. Requis pour tout démarrage de TradingView Desktop avec CDP.
