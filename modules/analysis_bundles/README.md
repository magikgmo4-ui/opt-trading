# analysis_bundles

Producteur de bundles d'analyse multi-source. Chaque bundle agrège des inputs
hétérogènes (market_metrics, Coinglass OCR, Telegram signals) en un contrat JSON
canonique.

## Flow

```
market_metrics.latest.json ──┐
coinglass_latest.json ───────┤──▶ btc_core_producer.py  ──▶ bundle.btc_core.v1
telegram_signals/*.json ─────┘

market_metrics.latest.json ──▶ macro_producer.py       ──▶ bundle.macro.v1
                                    (mode dégradé: DXY + Gold)
```

## Commandes

```bash
# CLI
bash modules/analysis_bundles/scripts/cmd.sh sanity
bash modules/analysis_bundles/scripts/cmd.sh test
bash modules/analysis_bundles/scripts/cmd.sh btc
bash modules/analysis_bundles/scripts/cmd.sh macro
bash modules/analysis_bundles/scripts/cmd.sh validate <file.json>

# Menu interactif
bash modules/analysis_bundles/scripts/menu.sh

# Python
python -m modules.analysis_bundles.app
```

## Env vars

_Aucune requise._ Les producers lisent les fichiers data existants
(data/data_center/, data/deskpro/, data/telegram_screener/).
Si les fichiers sont absents → le bundle sort en mode STALE ou UNKNOWN
(ne lève jamais d'exception).

## Invariants

- Chaque bundle a un `contract` préfixé `bundle.`
- `freshness_state = FRESH` si toutes les sources < cadence/2
- `freshness_state = STALE` si au moins une source > cadence ou absente
- `missing_inputs` n'est jamais vide si `freshness_state = STALE`
- `confidence = LOW` si au moins une source STALE
- Aucune écriture disque — lecture seule
- Pas de crash si fichier absent → MISSING dans les inputs

## Bundles

| Bundle | Contract | Status |
|---|---|---|
| BTC Core | `bundle.btc_core.v1` | ESTABLISHED |
| Macro | `bundle.macro.v1` | ESTABLISHED (dégradé) |
| Energy/Oil | `bundle.energy_oil.v1` | HYPOTHESIS |

## Tests

```bash
python3 -m pytest tests/test_bundle_contracts.py -v
```

32 tests couvrant: validation, schema, producers, round-trip, enums.
