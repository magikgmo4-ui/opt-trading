---
doc_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01_REGISTRY_FIELD_UPDATE
doc_type: schema
repo: opt-trading
go_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 20_REGISTRY_FIELD_UPDATE - Champs telegram_latency

## Champ table registry (V1)

Ajouter une colonne à la table `2_REGISTRY` (sans casser l’existant):

- `telegram_latency` (valeurs)
  - `UNMEASURED` (default)
  - `MEASURING`
  - `PASS`
  - `DEGRADED`
  - `BLOCKED`

## Champs par entrée (V1)

Ajouter dans chaque section `3.x`:

- `telegram_latency_status`
- `telegram_latency_p95_ms` (optionnel)
- `telegram_latency_ok_rate` (optionnel)
- `telegram_latency_evidence_ref` (optionnel: path/json id)
- `telegram_latency_last_measured_at` (optionnel)

## Source de vérité

Les valeurs proviennent du backtest offline (telemetry JSONL) et ne doivent jamais être “inventées” sans preuve.

## Ancrage umbrella

- `MASTER_TARGET` : standardiser la dimension `telegram_latency` dans le produit final total
- `Tableau Kanban du bundle` : reste la navigation principale
- `Produit final total voulu` : chaines separees mais liees entre webhook, Desk Pro, Telegram, Sheets, Perf et runtime
- `Prochain item Kanban exact` : `GO_SIGNAL_CHAIN_E2E_DRY_RUN_01`
- `Gaps encore ouverts` : seuils non fixes, evidence refs non renseignees par strategie, mise a jour registry encore read-only
