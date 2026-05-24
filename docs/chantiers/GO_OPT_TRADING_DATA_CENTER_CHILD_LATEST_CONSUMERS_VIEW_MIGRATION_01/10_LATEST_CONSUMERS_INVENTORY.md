---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01_LATEST_CONSUMERS_INVENTORY
doc_type: inventory
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_LATEST_CONSUMERS_INVENTORY

## Périmètre

Consumers `market_metrics.v1` avec `access_pattern: latest_only` dans `modules/data_center/registry/consumers.json`.

## Inventaire (au 2026-05-23)

### `desk_pro__market_metrics`

```json
{
  "consumer_id": "desk_pro__market_metrics",
  "contract_class": "market_metrics.v1",
  "read_path": "data/data_center/views/market_metrics/latest.json",
  "access_pattern": "latest_only",
  "implementation_status": "implemented",
  "migration_needed": false,
  "read_path_current": null
}
```

**Reader réel** : `modules/desk_pro/service/market_metrics_reader.py`

Logique : `DC_MARKET_METRICS_VIEW` (primary) → `MARKET_METRICS_LEGACY` (fallback) → `[]`

**Migration** : COMPLÈTE (PR #753)

---

### `telegram_screener__signal_context`

```json
{
  "consumer_id": "telegram_screener__signal_context",
  "contract_class": "market_metrics.v1",
  "read_path": "data/data_center/views/market_metrics/latest.json",
  "access_pattern": "latest_only",
  "implementation_status": "not_started",
  "migration_needed": false,
  "read_path_current": null
}
```

**Reader réel** : AUCUN — aucun fichier Python dans `modules/` ne lit cette donnée.

**Recherche effectuée** :
```bash
find modules/ -name "*.py" | xargs grep -l "telegram_screener\|signal_context"
# → modules/data_center/tests/test_contract_tests.py uniquement
```

**Statut** : `not_started` est correct. Ne pas créer de reader fantôme.

**Prochaine étape** : quand `PF_TELEGRAM_SCREENER` sera implémenté, son reader devra lire `data/data_center/views/market_metrics/latest.json` en primary.

---

### `google_sheets__market_reporting`

```json
{
  "consumer_id": "google_sheets__market_reporting",
  "contract_class": "market_metrics.v1",
  "read_path": "data/data_center/views/market_metrics/latest.json",
  "access_pattern": "latest_only",
  "implementation_status": "not_started",
  "migration_needed": false,
  "read_path_current": null
}
```

**Reader réel** : AUCUN — aucun fichier Python dans `modules/` ne lit cette donnée.

**Recherche effectuée** :
```bash
find modules/ -name "*.py" | xargs grep -l "google_sheets\|market_reporting"
# → modules/data_center/tests/test_contract_tests.py uniquement
```

**Statut** : `not_started` est correct. Ne pas créer de reader fantôme. `fallback: error` déjà positionné (consumer critique).

**Prochaine étape** : quand `PF_GOOGLE_SHEETS_CONSUMER` sera implémenté, son reader devra lire `data/data_center/views/market_metrics/latest.json` en primary et lever une exception si absent (`fallback: error`).

---

## Récapitulatif

| Consumer | read_path correct | Reader réel | À migrer | Statut |
|---|---|---|---|---|
| `desk_pro__market_metrics` | Oui | Oui | — migré | DONE |
| `telegram_screener__signal_context` | Oui | Non | — rien à migrer | not_started |
| `google_sheets__market_reporting` | Oui | Non | — rien à migrer | not_started |

## Autres consumers `market_metrics.v1` hors périmètre `latest_only`

| Consumer | access_pattern | Note |
|---|---|---|
| `strategy_framework__market_context` | `by_symbol` | `views/market_metrics/by_symbol/` — GO futur |
| `perf_engine__replay_context` | `full_history` | `normalized/` — vue historique, GO futur |
