---
doc_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01_STORAGE_AND_INGESTION_PLAN
doc_type: storage_ingestion_plan
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 30_STORAGE_AND_INGESTION_PLAN

## Objectif

Normaliser le stockage des donnees collectors pour permettre :

1. lecture rapide par Desk Pro ;
2. reutilisation par Sheets, Telegram, Perf Engine, Strategy Registry, replay et paper ;
3. ingestion DB future sans changer le contrat producteur ;
4. audit et replay via raw/normalized/events/errors.

## Stockage cible

```text
data/collectors/
  derivatives/
    raw/
    normalized/
    latest.json
    manifest.json
    status.json
    events.jsonl
    errors.jsonl
    cache/
      by_symbol/
        BTCUSDT.json
        ETHUSDT.json

  spot/
    coingecko/
      raw/
      normalized/
      latest.json
      manifest.json
      status.json
      events.jsonl
      errors.jsonl
    binance_spot/
      raw/
      normalized/
      latest.json
      manifest.json
      status.json
      events.jsonl
      errors.jsonl

data/deskpro/inputs/market_metrics/
  latest.json
  by_symbol/
    BTCUSDT.json
    ETHUSDT.json
```

## Roles des couches

| Couche | Role | Ecrasee ? | Consommateur |
|---|---|---:|---|
| `raw/` | capture API brute | non | audit/replay/debug |
| `normalized/` | payload stable par run | non | tests/reporting |
| `latest.json` | pointeur dernier run valide | oui | Desk Pro / wrappers |
| `manifest.json` | inventaire artefacts | oui | decouverte |
| `status.json` | etat/fraicheur runtime | oui | health/readiness |
| `events.jsonl` | historique append-only | non | audit |
| `errors.jsonl` | erreurs append-only | non | debug |
| `cache/by_symbol/` | lecture rapide | oui par symbole | Desk Pro/Sheets/Telegram/Perf |

## Surface Desk Pro

Desk Pro doit consommer une surface read-only derivee :

```text
data/deskpro/inputs/market_metrics/latest.json
```

Cette surface peut pointer vers les fichiers collectors originaux via `refs`, mais elle doit rester stable pour le consumer.

## Politique ingestion future

L'ingestion DB future doit lire les memes contrats que Desk Pro :

- `market_metrics.v1`
- `latest.json`
- `by_symbol/<SYMBOL>.json`
- `manifest.json`
- `status.json`

Elle ne doit pas parser les fichiers legacy JSON/CSV directement sauf pour migration ou audit.

## Relation avec `/shared/desk_pro/latest/`

Le repo a deja un contrat source minimal pour Desk Pro / db-layer :

```text
/shared/desk_pro/latest/
  run_summary.json
  portfolio_engine.json
  journal_engine.json
  perf_engine.json
```

Ce chantier ne remplace pas cette surface. Il prepare une nouvelle famille d'inputs read-only que Desk Pro pourra ensuite exporter ou resumer dans ses artefacts `/shared` si necessaire.

## Regle de compatibilite

- Les exports legacy derivatives JSON/CSV restent valides.
- Le stockage normalise ajoute une couche de decouverte, cache et contrat.
- Les consumers doivent preferer `latest` / `by_symbol` aux fichiers timestampes.
- Les fichiers timestampes restent la verite de replay et audit.

## Contraintes de non-elargissement

- aucune action broker ;
- aucune notification externe ;
- aucune ecriture Sheets ;
- aucune ecriture DB directe ;
- aucune suppression de captures raw.
