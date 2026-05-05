# 30_PHASE_3 — Wrapper opt-trading

## Objectif

Créer une couche opt-trading minimale pour lancer les lectures TradingView et exporter les résultats.

## Structure proposée

```
modules/tradingview_observer/
  README.md
  cmd.sh ou cmd.ps1
  menu.sh ou menu.ps1
  sanity_check.ps1
  app/
    observer_runner.py ou observer_runner.ps1
  output/
    .gitkeep
```

## Rôle

- Ne pas contenir tradingview-mcp directement (installé hors repo).
- Appeler l'outil externe installé dans `C:\Users\ghost\.claude\tools\tradingview-mcp`.
- Exporter JSON et/ou MD dans `output/`.
- Permettre reprise par desk/admin-trading plus tard.

## Sorties attendues

- `output/latest_chart_state.json`
- `output/latest_quote.json`
- `output/latest_alert_inventory.json`
- `output/latest_smoke_report.md`

## Critère PASS

Depuis opt-trading, une commande unique peut produire un inventaire TradingView local en lecture seule.

## Résultat

**Statut** : [PASS / PARTIAL / FAIL]

**Détail** :
