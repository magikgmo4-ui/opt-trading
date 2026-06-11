# GO_OPT_TRADING_DATA_CENTER_CHILD_CANONICAL_VALUE_PUBLISHER_01

## Inventaire Desk Pro — Data Center

### Sources inventoriées (6 dans `data_center_router.py`)

| Source | Contract | Status DC | Provenance | Fichiers | Gap |
|---|---|---|---|---|---|
| `vision_analysis` | `vision_analysis.v1` | ESTABLISHED | PROVEN | 24 symboles × multi-TF | OK |
| `coinglass_ocr` | `vision_context.coinglass.v1` | ESTABLISHED | PROVEN | `deskpro/inputs/vision_context/coinglass/latest.json` | OK |
| `market_metrics` | `market_metrics.v1` | HYPOTHESIS | MISSING | `data_center/views/market_metrics/latest.json` absent | **Pas de producer actif** |
| `telegram_screener` | `telegram_signal.v1` | HYPOTHESIS | PROVEN | 44 canaux, 853 signaux | OK (depuis notre PR) |
| `telegram_collector` | (none) | HYPOTHESIS | PROVEN | `collector_telegram/outputs/` | Pas de contrat DC |
| `runtime_health` | (none) | ESTABLISHED | PROVEN | `runtime_health/ledger/events.jsonl` | Pas de contrat DC |

### Sources candidates non inventoriées

| Source | Données dispo | Fichier | Gap |
|---|---|---|---|
| `derivatives` | OI, funding rate, liquidations | `data/derivatives/latest.json` | Pas dans DC |
| `desk_snapshot` | Market snapshots | `data/desk_runs/` | Pas dans DC |
| `probability` | Scores de probabilité | `data/probability/` | Pas dans DC |
| `ranker` | Ranking decisions | `data/ranker/` | Pas dans DC |
| `portfolio` | Portfolio state | `data/portfolio/` | Pas dans DC |
| `risk` | Risk config | `data/risk/` | Pas dans DC |
| `position` | Position engine | `data/position/` | Pas dans DC |
| `execution` | Execution engine | `data/execution/` | Pas dans DC |
| `decision` | Decision engine | `data/decision/` | Pas dans DC |
| `liquidation` | Liquidation events | `data/liquidation/` | Pas dans DC |

### Desk Pro inputs (attendus par dry_run)

| Input | Status | Fichier | Gap |
|---|---|---|---|
| `signal_event` | PROVEN | `state/events.jsonl` | V0 format, pas V1 dans DC |
| `visual_context` | PROVEN | `deskpro/inputs/vision_context/coinglass/latest.json` | OK |
| `desk_snapshot` | HYPOTHESIS | `desk_runs/` | Pas consolidé dans DC |
| `market_metrics` | MISSING | Introuvable | **Pas de producer** |
| `vision_analysis` | PROVEN | `deskpro/inputs/vision_analysis/latest.json` | OK |
| `telegram_claim` | PROVEN | `deskpro/inputs/telegram_claim/latest.json` | OK (single claim) |

### Checklist gaps prioritaires

- [ ] **P0 — `canonical_value_publisher`** : brancher source_selector → vraies valeurs → views DC
- [ ] **P1 — `market_metrics` producer** : créer un producer qui publie `market_metrics.v1` dans DC
- [ ] **P2 — `desk_snapshot` → DC** : router les snapshots dans `data_center/views/desk_snapshot/`
- [ ] **P2 — `derivatives` → DC** : contrat `derivatives.v1` dans DC
- [ ] **P3 — `telegram_collector` → contrat DC** : contrat `telegram_raw.v1`
- [ ] **P3 — `runtime_health` → contrat DC** : contrat `runtime_health.v1`
