# TradingView Observer — OpenClaw Skill

Module permettant a OpenClaw de lire TradingView Desktop via le wrapper opt-trading read-only.

## Pre-requis

- Wrapper `modules/tradingview_observer/` operationnel (Phase 3-6)
- TradingView Desktop lance avec CDP sur `127.0.0.1:9222`
- Node.js v24+ disponible

## Utilisation

```powershell
# Sanity check rapide (7 checks)
.\run.ps1 sanity

# Snapshot complet (sanity + export 6 JSON)
.\run.ps1 snapshot

# Bridge packet V1 (dry-run, sans transfert)
.\run.ps1 bridge
```

## Flow de securite

```
OpenClaw → run.ps1 → cmd.ps1 → app/observer_runner.ps1 → TV CLI → CDP 9222
                            ↳ sanity_check.ps1
                            ↳ export_bridge_packet.ps1
```

- OpenClaw n'accede jamais directement a CDP ou tradingview-mcp
- Toute mutation est verrouillee
- Aucun transfert admin-trading
- Aucun output live committe

## Skill definition

Voir `skill.md` pour la definition OpenClaw complete.

## Exports

Tous les exports sont dans `..\tradingview_observer\output\`
