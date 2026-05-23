---
doc_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01_REPO_STATE_AND_GAPS
doc_type: state_gap_report
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 10_REPO_STATE_AND_GAPS

## Objet

Documenter l'etat reel des collectors API dans le repo et les gaps a combler avant ingestion Desk Pro / reutilisation multi-surface.

## Collectors etablis

| Surface | Etat | Role | Stockage courant | Verdict |
|---|---|---|---|---|
| `modules/derivatives_collector` | canonique | metrics derivatives | `data/derivatives` JSON/CSV + `.meta.json` + lifecycle compat | actif, partiellement converge |
| `modules/collector_coingecko` | valide | spot market snapshot | raw + normalized + lifecycle family | propre, `collectors_core` |
| `modules/collector_binance_spot` | valide | spot pair market snapshot | raw + normalized + lifecycle family | propre, `collectors_core` |
| `packages/collectors_core` | valide | runtime helpers | lifecycle/config/artifacts/http helpers | fondation partagee |
| `modules/derivatives_collector/app/bitget_adapter.py` | reel | Bitget USDT-M futures partial | via derivatives collector | present, couverture incomplete |

## Donnees collectables etablies

### derivatives_collector

Champs cibles exposes par la dataclass actuelle :

- `symbol`
- `exchange`
- `timestamp`
- `open_interest`
- `funding_rate`
- `long_short_ratio`
- `liquidations_long`
- `liquidations_short`
- `volume_futures`
- `error`

### Binance derivatives adapter

Couverture observee :

- `open_interest`
- `funding_rate`
- `volume_futures`
- `long_short_ratio`

Gap : liquidations non prouvees dans l'adapter lu.

### Bitget derivatives adapter

Couverture observee :

- `open_interest`
- `volume_futures`
- `funding_rate`

Gaps :

- `long_short_ratio` non prouve
- `liquidations_long` non prouve
- `liquidations_short` non prouve
- gestion d'erreur provider-specific minimaliste

### CoinGecko spot

Couverture : snapshot marche spot normalise, raw response + normalized output + lifecycle family.

### Binance spot

Couverture : exchange info + ticker 24h, raw response + normalized output + lifecycle family.

## Gaps majeurs

| Gap | Impact | Priorite |
|---|---|---|
| `market_metrics.v1` non materialise | Desk Pro ne peut pas consommer directement les metrics collectors | A |
| Bitget coverage incomplete | donnees partielles non visibles dans un rapport provider | A |
| Coinglass placeholder/non prouve | risque de supposer une source non implemente | A |
| cache `by_symbol` absent | reutilisation rapide par Desk Pro/Sheets/Telegram/Perf moins directe | A |
| Desk Pro consumer read-only absent | le contrat reste theorique | A |
| tests smoke provider coverage absents | regressions non bloquees | A |
| ingestion DB non implementee | `/shared/desk_pro/latest` reste consultation/prep seulement | B |

## Regle de rapport attendue

Chaque provider doit publier un rapport de couverture :

```json
{
  "provider_id": "bitget",
  "module_id": "derivatives_collector",
  "symbol": "BTCUSDT",
  "collectable_metrics": ["open_interest", "funding_rate", "volume_futures"],
  "missing_metrics": ["long_short_ratio", "liquidations_long", "liquidations_short"],
  "runtime_status": "partial",
  "notes": ["do not synthesize missing metrics"]
}
```

## Decision

Le prochain patch doit traiter les gaps comme de la couverture explicite, pas comme des donnees simulees. Une metrique absente doit rester `null` avec `provider_coverage`, `missing_metrics` et warning exploitable.
