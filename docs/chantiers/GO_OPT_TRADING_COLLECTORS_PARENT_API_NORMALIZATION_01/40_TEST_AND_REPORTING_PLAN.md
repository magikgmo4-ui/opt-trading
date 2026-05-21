---
doc_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01_TEST_AND_REPORTING_PLAN
doc_type: test_plan
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 40_TEST_AND_REPORTING_PLAN

## Objectif

Definir les tests et rapports necessaires pour prouver les donnees collectables, les gaps et la compatibilite Desk Pro read-only.

## Tests minimaux attendus

| Test | Objectif | Side effects |
|---|---|---|
| provider coverage unit | prouver collectable/missing metrics par provider | aucun |
| market_metrics schema | valider le contrat `market_metrics.v1` | aucun |
| derivatives mock -> market_metrics | prouver conversion depuis `DerivativesRow` | fichiers temporaires |
| Bitget fixture -> market_metrics | prouver couverture partielle explicite | aucun appel externe |
| Binance derivatives fixture -> market_metrics | prouver coverage OI/funding/volume/L/S | aucun appel externe |
| Desk Pro read-only smoke | prouver consommation sans mutation | aucun write externe |
| cache by-symbol smoke | prouver generation `by_symbol/<SYMBOL>.json` | fichiers temporaires |

## Rapport attendu

Fichier cible propose :

```text
data/collectors/reports/provider_metric_coverage_latest.json
```

Payload cible :

```json
{
  "generated_at": "2026-05-20T00:00:00Z",
  "contract_version": "v1",
  "providers": [
    {
      "module_id": "derivatives_collector",
      "provider_id": "bitget",
      "status": "partial",
      "collectable_metrics": ["open_interest", "funding_rate", "volume_futures"],
      "missing_metrics": ["long_short_ratio", "liquidations_long", "liquidations_short"],
      "test_status": "fixture_pass"
    }
  ],
  "gaps": [
    {
      "provider_id": "coinglass",
      "status": "not_proven_runtime_adapter",
      "action": "implement_or_remove_placeholder"
    }
  ]
}
```

## Critere PASS

Un provider peut passer meme si sa couverture est partielle, a condition que :

- la couverture soit explicite ;
- les metriques absentes soient `null` ;
- le rapport liste les gaps ;
- Desk Pro ne recoive pas un PASS silencieux ;
- aucune donnee manquante ne soit inventee.

## Critere BLOCKED

- provider mentionne sans adapter runtime prouve ;
- metrique manquante remplie par defaut numerique trompeur ;
- cache by-symbol sans timestamp ou provider coverage ;
- Desk Pro consomme sans warning de freshness/coverage ;
- test avec appel reseau externe non mocke dans CI.

## Commandes cibles futures

```bash
python -m pytest tests/collectors/test_market_metrics_contract.py -q
python -m pytest tests/desk_pro/test_market_metrics_readonly_consumer.py -q
python tools/collectors/build_provider_metric_coverage_report.py --fixtures
```

## Rapport humain attendu

Un rapport markdown doit etre produit dans le chantier child :

```text
docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01/10_PROVIDER_COVERAGE_REPORT.md
```

Il doit resumer :

- provider ;
- endpoint/source ;
- donnees collectables ;
- donnees manquantes ;
- risque ;
- statut test ;
- prochain patch recommande.
