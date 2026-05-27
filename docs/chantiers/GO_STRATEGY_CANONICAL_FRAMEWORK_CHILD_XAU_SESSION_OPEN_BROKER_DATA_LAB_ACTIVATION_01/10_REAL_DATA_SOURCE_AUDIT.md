---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01_AUDIT
doc_type: audit
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01
---

# 10 — Audit des sources de données réelles disponibles

## Situation post-PR #865

| Source | État | Notes |
|---|---|---|
| `sample_xauusd_m1.csv` | Committée — 12 lignes, 2 dates | Synthétique non diversifiée |
| `state/trading_lab_v1/` | Gitignorée (`state/`) | Runtime state, ne pas committer |
| Export Dukascopy | Non disponible — hors scope | Validé nécessaire pour `MEASURED` |
| Export MT4/MT5 | Non disponible dans ce repo | Possible via broker |
| Export TradingView | Non disponible | Alertes TV via webhook, pas OHLCV |

## Lacunes du sample existant

- 12 lignes M1 total, 2 dates (2026-04-03, 2026-04-04)
- Produit uniquement `xau_open_sweep_fvg` sur les 4 variants possibles
- Pas representatif: sweep+FVG dans les 2 sessions, pas de session sans signal
- Prix arrondis (3200, 3201...) — non réalistes pour XAUUSD M1

## Décision: ajout d'un sample réaliste

`modules/trading_lab_v1/data/sample_xauusd_m1_real_like.csv`

Caractéristiques:
- 60 lignes M1, 10 sessions, 5 semaines (2026-04-07 au 2026-04-14)
- 2 sessions/jour (gold_open_18h + midnight_00h)
- 4/4 variants couverts: sweep_fvg, no_sweep_fvg, sweep_no_fvg, no_sweep_no_fvg
- Directions diversifiées: 5 bullish + 5 bearish
- Prix réalistes ~3250-3275 avec progression graduelle
- Volumes réalistes 90-150

## Règles de placement des données broker réelles

Pour des exports broker réels XAUUSD M1 (non inclus dans ce repo):

```
# Placer dans (gitignorée automatiquement):
state/trading_lab_v1/inputs/xauusd_m1_<broker>_<daterange>.csv

# OU dans le répertoire data (committée — seulement si anonymisée):
modules/trading_lab_v1/data/sample_xauusd_m1_<description>.csv
```

Les fichiers dans `state/` sont gitignorés via `.gitignore` (`state/`). Ne jamais committer de données contenant des prix live sensibles ou des métadonnées broker.

## État .gitignore

`state/` est gitignorée globalement → tous les fichiers `state/trading_lab_v1/*.jsonl` sont exclus du commit automatiquement.

Aucun changement .gitignore nécessaire.
