# TradingView Observer — OpenClaw Skill

Module permettant a OpenClaw de lire TradingView Desktop via le wrapper opt-trading read-only.

## Pre-requis

- Wrapper `modules/tradingview_observer/` operationnel (Phase 3)
- TradingView Desktop lance avec CDP sur `127.0.0.1:9222`
- Node.js v24+ disponible

## Utilisation

```powershell
# Sanity check rapide
.\run.ps1 sanity

# Snapshot complet (export JSON)
.\run.ps1 snapshot

# Les exports sont dans ..\tradingview_observer\output\
```

## Skill definition

Voir `skill.md` pour la definition OpenClaw complete.
