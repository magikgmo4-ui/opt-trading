# Acceptance Report — GO_OPT_TRADING_TRADINGVIEW_ORCHESTRATOR_01

**Date** : 2026-06-12  
**Verdict** : PASS — E2E validé, pipeline en production

---

## Objectif atteint

Construire un système durable et orchestrable permettant de piloter TradingView
(alertes, charts, indicateurs, Pine Script, layouts) via prompt/commande avec gate
humain, sans jamais toucher TradingView manuellement.

---

## Contexte — problème initial

TradingView Desktop est une **app MSIX** sur Windows (cursor-ai, 192.168.0.177).
Plusieurs contraintes techniques ont dû être résolues pour rendre l'accès CDP possible
depuis Linux (admin-trading) :

| Contrainte | Symptôme | Solution |
|---|---|---|
| MSIX AppContainer loopback isolation | HTTP vers port 9222 hang infini, TCP OK | `CheckNetIsolation.exe LoopbackExempt -a -n="TradingView.Desktop_n534cwy3pjxzj"` |
| Lancement MSIX avec args | Start Menu ne passe pas `--remote-debugging-port` | `TradingView_CDP.vbs` (bureau ghost) via `IApplicationActivationManager` |
| Session Windows isolation | SSH = session 0, TradingView = session 1 | Agent Task Scheduler OnLogon (session 1) |
| SCP Windows paths | `C:\path` → "No such file" | Conversion `/C:/path` côté Linux |
| UTF-8 BOM PowerShell | JSON parse échoue — `\xef\xbb\xbf` en tête | `encoding="utf-8-sig"` Python |
| PS5.1 compat | `??` opérateur PS7 only, em dash non-ASCII | `Coalesce()` helper, sed fix |
| `@Args` vs `@CmdArgs` | Sous-commandes multi-mots (alert list) ne passent qu'un arg | `[Parameter(ValueFromRemainingArguments=$true)]` |
| CDP HTTP via SSH | `Invoke-WebRequest` hang dans contexte SSH | `Test-NetConnection` TCP probe uniquement |
| Poll timeout | SSH+PS `Test-Path` ~10s/tentative → 120s épuisé | Polling SCP direct (0.3s/tentative) |

---

## Architecture livrée

```
[admin-trading Linux]
  tv_runner.py
  ├── charge job packet tv_job_v1 (JSON)
  ├── gate check (mutation → --gate-approved requis)
  ├── inject secrets si nécessaire (ex: TV_WEBHOOK_KEY pour alert.rotate)
  ├── SCP → cursor-ai /C:/Users/ghost/opt-trading/.../jobs/pending/<id>.json
  └── poll SCP jobs/done/<id>.result.json (2s interval, 120s timeout)

[cursor-ai Windows — Task Scheduler TVOrchestratorAgent, session 1]
  tv_agent.ps1
  ├── poll jobs/pending/ toutes les 2s
  ├── CheckCdp via Test-NetConnection TCP port 9222
  ├── ExecJob → node $TV_CLI @CmdArgs (tradingview-mcp CLI)
  └── résultat → jobs/done/<id>.result.json

[TradingView Desktop]
  CDP:9222 (--remote-debugging-port=9222)
  ├── status / quote / state / values / alerts
  ├── alert create/delete/rotate_webhook_key
  ├── indicator add/remove/set
  ├── symbol.set / timeframe.set
  ├── pine.set / pine.save
  └── layout.switch / screenshot
```

---

## Fichiers produits

| Fichier | Rôle |
|---|---|
| `modules/tradingview_observer/agent/tv_agent.ps1` | Agent Windows — poll + exec CLI |
| `modules/tradingview_observer/agent/install_agent.ps1` | Setup Task Scheduler TVOrchestratorAgent |
| `modules/tradingview_orchestrator/app/tv_runner.py` | Runner Linux — dispatch + poll |
| `modules/tradingview_orchestrator/scripts/cmd.sh` | CLI entry point |
| `modules/tradingview_orchestrator/scripts/sanity_check.sh` | Validation installation |
| `schemas/tv_job_v1.json` | JSON Schema du job packet |
| `scripts/ai/workers/runner_tv.py` | Adapter dispatcher → tv_runner |
| `scripts/ai/workers/tasks.index.json` | +TV_SNAPSHOT (A2), +TV_WRITE_GATED (A0) |
| `scripts/ai/workers/openclaw_strict_worker_dispatcher.py` | Routing TV_* → runner_tv |
| `modules/tradingview_orchestrator/jobs/examples/` | 4 job packets d'exemple |
| `C:\Users\ghost\Desktop\TradingView_CDP.vbs` | Lanceur CDP (bureau cursor-ai) |

---

## Résultat E2E validé

```
snapshot OANDA:XAUUSD — 2026-06-12
  status:  CDP=True  api_available=True
  quote:   open=4219.55  close=4211.165
  state:   OANDA:XAUUSD  TF=240  studies=6
  alerts:  11 alertes lues
  values:  2 études
```

---

## Procédure startup (obligatoire avant chaque session orchestrée)

1. Double-cliquer `C:\Users\ghost\Desktop\TradingView_CDP.vbs` sur cursor-ai
2. TradingView s'ouvre avec CDP sur port 9222
3. Vérifier : `ssh cursor-ai "cmd /c netstat -ano | findstr :9222"`
4. L'agent TVOrchestratorAgent démarre automatiquement au logon de ghost

**Note** : TradingView ouvert via Start Menu n'a PAS le CDP — toujours utiliser le VBS.

---

## Commandes opérationnelles

```bash
# Snapshot complet (lecture, pas de gate)
source .env && python3 modules/tradingview_orchestrator/app/tv_runner.py \
  modules/tradingview_orchestrator/jobs/examples/tv_job_snapshot.json

# Créer une alerte (gate requis)
python3 modules/tradingview_orchestrator/app/tv_runner.py \
  modules/tradingview_orchestrator/jobs/examples/tv_job_alert_create.json \
  --gate-approved

# Dry-run (voir ce qui serait exécuté)
python3 ... --dry-run

# Via cmd.sh
modules/tradingview_orchestrator/scripts/cmd.sh snapshot
```

---

## Intégration OpenClaw / dispatcher

```
TV_SNAPSHOT   → A2 autonomy, read-only, runner_tv.py
TV_WRITE_GATED → A0, requires --gate-approved, 11 mutation types
```

Les job types `snapshot`, `alert.list`, `screenshot` ne nécessitent pas de gate.
Toutes les mutations (alert.create, indicator.set, pine.set, etc.) bloquent sans
`--gate-approved`.

---

## État des credentials P1 (GO_SECURITY_P1_UNKNOWN_VERIFY_ROTATE_01)

| Credential | Verdict | Action |
|---|---|---|
| `TV_WEBHOOK_KEY` | STALE | ROTATED 2026-06-12 — `.env` mis à jour |
| `OPS_ADMIN_KEY` | STALE | ROTATED 2026-06-12 — `.env` mis à jour |
| `TELEGRAM_BOT_TOKEN` | KEEP | Vérifié BotFather 2026-06-12 — dans TTL |

Note : les 11 alertes TradingView existantes sont des alertes prix (texte brut),
pas des alertes webhook. TV_WEBHOOK_KEY ne nécessite pas de propagation côté TV.

---

## Prochaine étape

`GO_TV_WEBHOOK_ALERTS_WIRE_01` — câbler des alertes TradingView en format webhook
(payload JSON avec `key=TV_WEBHOOK_KEY`) vers `webhook_server.py`, en utilisant
l'orchestrateur pour créer/gérer ces alertes via commande.
