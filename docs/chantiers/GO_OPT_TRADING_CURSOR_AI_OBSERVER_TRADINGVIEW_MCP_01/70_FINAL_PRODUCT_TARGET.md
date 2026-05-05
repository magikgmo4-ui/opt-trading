# 70_FINAL_PRODUCT_TARGET — TradingView Desktop Observer for opt-trading

## Nom produit

**TradingView Desktop Observer for opt-trading**

## Usage final

Permettre à opt-trading/OpenClaw de voir et auditer TradingView Desktop localement.

## Capacités finales

1. Lire le symbole courant.
2. Lire le timeframe courant.
3. Lire OHLC / quote.
4. Lire indicateurs visibles si disponibles.
5. Lire dessins/tables Pine si disponibles.
6. Capturer screenshot si disponible.
7. Lister les alertes.
8. Auditer statut des alertes.
9. Préparer une alerte test.
10. Exporter JSON/MD structuré.
11. Donner à OpenClaw une vue exploitable.
12. Garder admin-trading comme runtime webhook séparé.

## Non-objectifs

- Pas de trading autonome.
- Pas de remplacement webhook.
- Pas de dépendance à Medium ou à une session ChatGPT.
- Pas de port CDP exposé au LAN.
- Pas de mutation de production sans GO explicite.

## Définition finale de Done

- [ ] Documentation complète présente (tous les fichiers créés et complétés).
- [ ] Installation locale reproductible (tradingview-mcp hors repo).
- [ ] Smoke PASS (phase 1).
- [ ] Wrapper opt-trading PASS (phase 3).
- [ ] OpenClaw skill documenté (phase 4).
- [ ] Closeout PASS (90_CLOSEOUT.md).
- [ ] Reprise possible depuis docs/chantiers uniquement.

## Architecture cible

```
cursor-ai (Windows)
├── TradingView Desktop (:9222 localhost)
├── tradingview-mcp (C:\Users\ghost\.claude\tools\tradingview-mcp)
├── Claude Code (client MCP)
│
opt-trading repo
├── modules/tradingview_observer/  (wrapper lecteur)
│   ├── cmd.ps1
│   ├── menu.ps1
│   ├── sanity_check.ps1
│   └── output/
├── openclaw_skills/               (skill orchestrateur)
│
admin-trading (serveur distant)
├── webhook TradingView            (canonique, inchangé)
└── desk                           (interface utilisateur)
```
