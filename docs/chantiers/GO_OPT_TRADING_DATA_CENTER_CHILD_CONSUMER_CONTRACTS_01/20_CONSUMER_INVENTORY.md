---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01_CONSUMER_INVENTORY
doc_type: consumer_inventory
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_CONSUMER_INVENTORY — Contrats consumers Data Center

## Objet

Inventaire des consumers connus avec leur contrat Data Center formalisé.

---

## C1 — `desk_pro__market_metrics`

```yaml
consumer_id: desk_pro__market_metrics
surface: PF_DESK_PRO
contract_class: market_metrics.v1
read_path: data/data_center/derivatives/derivatives_collector__bitget/latest.json
access_pattern: latest_only
read_mode: pull
latency_tolerance: oneshot
freshness_min: stale_ok
fallback: silent_empty
implementation_status: implemented
read_path_current: data/deskpro/inputs/market_metrics/latest.json
migration_needed: true
validated_at: 2026-05-23
notes: >
  Implémenté dans modules/desk_pro/service/market_metrics_reader.py.
  Lit actuellement depuis data/deskpro/inputs/market_metrics/latest.json
  (path alimenté par market_metrics_writer.py, pas directement depuis data/data_center/).
  Migration : changer la constante MARKET_METRICS_LATEST dans market_metrics_reader.py.
  Le fallback silent_empty est éprouvé : retourne [] si fichier absent ou malformé.
```

### Note de migration

Le path actuel `data/deskpro/inputs/market_metrics/latest.json` est une vue de transit.

Dans la cible Data Center :
- le producer `derivatives_collector__bitget` écrit dans `data/data_center/derivatives/derivatives_collector__bitget/latest.json` ;
- le consumer Desk Pro lit depuis ce path Data Center directement ;
- le path de transit `data/deskpro/inputs/market_metrics/` peut être maintenu en parallèle ou déprécié dans un child GO dédié.

---

## C2 — `desk_pro__spot_snapshot`

```yaml
consumer_id: desk_pro__spot_snapshot
surface: PF_DESK_PRO
contract_class: pair_market_snapshot.v1
read_path: data/data_center/spot/collector_binance_spot/latest.json
access_pattern: latest_only
read_mode: pull
latency_tolerance: oneshot
freshness_min: stale_ok
fallback: silent_empty
implementation_status: not_started
read_path_current: null
migration_needed: false
validated_at: null
notes: >
  Consumer futur. Desk Pro ne lit pas encore de snapshot spot.
  Ce contrat prévoit la lecture du pair_market_snapshot.v1 une fois le producer
  collector_binance_spot adapté vers data/data_center/.
```

---

## C3 — `strategy_framework__market_context`

```yaml
consumer_id: strategy_framework__market_context
surface: PF_STRATEGY_FRAMEWORK_REGISTRY
contract_class: market_metrics.v1
read_path: data/data_center/derivatives/derivatives_collector__bitget/cache/by_symbol/<SYMBOL>.json
access_pattern: by_symbol
read_mode: pull
latency_tolerance: batch
freshness_min: stale_ok
fallback: stale_ok
implementation_status: not_started
read_path_current: null
migration_needed: false
validated_at: null
notes: >
  Consumer futur pour enrichissement des évaluations stratégie.
  Accès par symbole pour contexte OI / funding lors de l'évaluation d'une stratégie.
  Pour le backtesting, accès full_history depuis normalized/ sera nécessaire
  (contrat étendu à ajouter dans consumer_id strategy_framework__backtest_context).
```

---

## C4 — `perf_engine__replay_context`

```yaml
consumer_id: perf_engine__replay_context
surface: PF_PERF_ENGINE_TRADING_LAB
contract_class: market_metrics.v1
read_path: data/data_center/derivatives/derivatives_collector__bitget/normalized/
access_pattern: full_history
read_mode: pull
latency_tolerance: batch
freshness_min: any
fallback: error
implementation_status: not_started
read_path_current: null
migration_needed: false
validated_at: null
notes: >
  Consumer futur pour replay et labelling en Trading Lab.
  Accès full_history (normalized/) nécessaire pour reconstruire le contexte market
  au moment de chaque trade passé.
  fallback: error car un replay incomplet sans contexte marché produit un résultat faux.
```

---

## C5 — `telegram_screener__signal_context`

```yaml
consumer_id: telegram_screener__signal_context
surface: PF_TELEGRAM_SCREENER
contract_class: market_metrics.v1
read_path: data/data_center/derivatives/derivatives_collector__bitget/latest.json
access_pattern: latest_only
read_mode: pull
latency_tolerance: near-realtime
freshness_min: fresh_only
fallback: silent_empty
implementation_status: not_started
read_path_current: null
migration_needed: false
validated_at: null
notes: >
  Consumer futur pour enrichissement des alertes Telegram avec contexte OI/funding.
  freshness_min: fresh_only — une alerte enrichie avec des données stale est trompeuse.
  Si stale : envoyer l'alerte sans contexte plutôt qu'avec un contexte périmé.
```

---

## C6 — `google_sheets__market_reporting`

```yaml
consumer_id: google_sheets__market_reporting
surface: PF_GOOGLE_SHEETS_CONSUMER
contract_class: market_metrics.v1
read_path: data/data_center/derivatives/derivatives_collector__bitget/latest.json
access_pattern: latest_only
read_mode: pull
latency_tolerance: batch
freshness_min: stale_ok
fallback: error
implementation_status: not_started
read_path_current: null
migration_needed: false
validated_at: null
notes: >
  Consumer futur pour reporting journalier dans Google Sheets.
  fallback: error — un export Sheets silencieux masquerait une panne du producer.
  L'opérateur doit savoir si les données market n'ont pas été exportées.
```

---

## C7 — `localcms__data_center_health`

```yaml
consumer_id: localcms__data_center_health
surface: PF_LOCALCMS_COCKPIT
contract_class: null
read_path: data/data_center/_registry/producers.json
             | data/data_center/<family>/<producer_id>/status.json
access_pattern: status_only
read_mode: pull
latency_tolerance: near-realtime
freshness_min: any
fallback: silent_empty
implementation_status: not_started
read_path_current: null
migration_needed: false
validated_at: null
notes: >
  Consumer futur pour visibilité ops dans LocalCMS.
  Ne lit pas les payloads — lit uniquement status.json et producers.json pour
  afficher l'état de santé du Data Center (derniers runs, producers actifs, fraîcheur).
  contract_class: null car ce consumer ne lit pas un payload normalisé mais des méta-fichiers.
```

---

## Registre `consumers.json` — état à la livraison de ce child

```json
{
  "registry_version": "v1",
  "updated_at": "2026-05-23T00:00:00Z",
  "consumers": [
    {
      "consumer_id": "desk_pro__market_metrics",
      "surface": "PF_DESK_PRO",
      "contract_class": "market_metrics.v1",
      "read_path": "data/data_center/derivatives/derivatives_collector__bitget/latest.json",
      "access_pattern": "latest_only",
      "fallback": "silent_empty",
      "implementation_status": "implemented",
      "migration_needed": true,
      "validated_at": "2026-05-23"
    },
    {
      "consumer_id": "desk_pro__spot_snapshot",
      "surface": "PF_DESK_PRO",
      "contract_class": "pair_market_snapshot.v1",
      "read_path": "data/data_center/spot/collector_binance_spot/latest.json",
      "access_pattern": "latest_only",
      "fallback": "silent_empty",
      "implementation_status": "not_started",
      "migration_needed": false,
      "validated_at": null
    },
    {
      "consumer_id": "strategy_framework__market_context",
      "surface": "PF_STRATEGY_FRAMEWORK_REGISTRY",
      "contract_class": "market_metrics.v1",
      "read_path": "data/data_center/derivatives/derivatives_collector__bitget/cache/by_symbol/",
      "access_pattern": "by_symbol",
      "fallback": "stale_ok",
      "implementation_status": "not_started",
      "migration_needed": false,
      "validated_at": null
    },
    {
      "consumer_id": "perf_engine__replay_context",
      "surface": "PF_PERF_ENGINE_TRADING_LAB",
      "contract_class": "market_metrics.v1",
      "read_path": "data/data_center/derivatives/derivatives_collector__bitget/normalized/",
      "access_pattern": "full_history",
      "fallback": "error",
      "implementation_status": "not_started",
      "migration_needed": false,
      "validated_at": null
    },
    {
      "consumer_id": "telegram_screener__signal_context",
      "surface": "PF_TELEGRAM_SCREENER",
      "contract_class": "market_metrics.v1",
      "read_path": "data/data_center/derivatives/derivatives_collector__bitget/latest.json",
      "access_pattern": "latest_only",
      "fallback": "silent_empty",
      "implementation_status": "not_started",
      "migration_needed": false,
      "validated_at": null
    },
    {
      "consumer_id": "google_sheets__market_reporting",
      "surface": "PF_GOOGLE_SHEETS_CONSUMER",
      "contract_class": "market_metrics.v1",
      "read_path": "data/data_center/derivatives/derivatives_collector__bitget/latest.json",
      "access_pattern": "latest_only",
      "fallback": "error",
      "implementation_status": "not_started",
      "migration_needed": false,
      "validated_at": null
    },
    {
      "consumer_id": "localcms__data_center_health",
      "surface": "PF_LOCALCMS_COCKPIT",
      "contract_class": null,
      "read_path": "data/data_center/_registry/producers.json",
      "access_pattern": "status_only",
      "fallback": "silent_empty",
      "implementation_status": "not_started",
      "migration_needed": false,
      "validated_at": null
    }
  ]
}
```

---

## BUNDLE_TARGET atteint

- [x] `10_CONSUMER_CONTRACT_SPEC.md` livré
- [x] `20_CONSUMER_INVENTORY.md` livré — 7 consumers formalisés (C1–C7)
- [x] Migration Desk Pro documentée (`migration_needed: true`, path courant noté)
- [x] Registre `consumers.json` spécifié
- [x] Fallback et latence définis pour chaque consumer

Prochain child : `GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01`.
