# 40_PHASE_4 — Integration OpenClaw Skill

## Objectif

Faire d'OpenClaw l'orchestrateur du wrapper opt-trading, sans acces libre au port 9222 ni au CLI tradingview-mcp.

## Structure creee

```
modules/tradingview_observer_openclaw/
  README.md   — documentation operateur
  skill.md    — definition du skill OpenClaw (commandes autorisees/interdites)
  run.ps1     — runner safe (appelle UNIQUEMENT le wrapper)
```

## Role d'OpenClaw

- Lancer les commandes validees du wrapper opt-trading.
- Lire les exports JSON produits par le wrapper.
- Resumer l'etat graphique (symbole, timeframe, indicateurs).
- Proposer des alertes (configuration assistee).
- Demander validation humaine avant toute modification.

## OpenClaw ne doit pas

- Acceder directement au port 9222 (CDP).
- Appeler tradingview-mcp directement.
- Creer / supprimer / modifier des alertes.
- Trader.
- Contourner le wrapper opt-trading.
- Modifier admin-trading.

## Skill definition (skill.md)

| Section | Contenu |
|---------|---------|
| ROLE | Lecteur TradingView Desktop via wrapper read-only |
| ENTRYPOINT | `modules/tradingview_observer_openclaw/run.ps1` |
| ALLOWED | `sanity`, `snapshot`, lecture des JSON output |
| FORBIDDEN | CDP direct, tradingview-mcp direct, alert_create, alert_delete, trade, admin-trading |
| FLOW | sanity -> snapshot -> read latest_report.json -> summarize |
| FAILURE | Retourner PARTIAL avec erreur, ne jamais reparer en mutatant |

## Test live (2026-05-05)

### run.ps1 sanity

```
=== TradingView Observer Sanity Check ===
[PASS] Node.js
[PASS] tradingview-mcp CLI
[PASS] CDP port 9222
[PASS] tv status
[PASS] tv state
[PASS] tv quote
[PASS] tv alert list
=== 7 PASS / 0 FAIL ===
```

### run.ps1 snapshot

```
[MODE] READ-ONLY

[1/6] CDP check...     OK: Chrome/140.0.7339.133
[2/6] tv status...     OK: BITGET:BTCUSDT.P 480
[3/6] tv quote...      OK: BITGET:BTCUSDT.P close=80632.8
[4/6] tv state...      OK: BITGET:BTCUSDT.P studies=7
[5/6] tv alert list... OK: 10 alerts
[6/6] tv values...     OK: 3 studies

=== Exports ===
  latest_alert_inventory.json (35.7 KB)
  latest_quote.json (0.4 KB)
  latest_report.json (51.7 KB)
  latest_state.json (1.2 KB)
  latest_status.json (0.5 KB)
  latest_values.json (1.1 KB)

Snapshot complete.
Read ...\output\latest_report.json for full analysis.
```

## Architecture securite

```
OpenClaw
  |
  |-- run.ps1 sanity/snapshot  (SEUL point d'entree autorise)
  |     |
  |     +---> modules/tradingview_observer/cmd.ps1
  |               |
  |               +---> sanity_check.ps1
  |               +---> app/observer_runner.ps1
  |                       |
  |                       +---> node .../src/cli/index.js (MCP CLI)
  |                               |
  |                               +---> 127.0.0.1:9222 (CDP)
  |
  +---> lecture output/latest_report.json

  X  Pas d'acces direct a 9222
  X  Pas d'acces direct a tradingview-mcp
  X  Pas de mutation TradingView
```

## Critere PASS

OpenClaw peut demander un etat TradingView et recevoir une sortie structuree sans mutation dangereuse. **Atteint.**

## Resultat

**Statut** : PASS

## RISKS

- À qualifier.
