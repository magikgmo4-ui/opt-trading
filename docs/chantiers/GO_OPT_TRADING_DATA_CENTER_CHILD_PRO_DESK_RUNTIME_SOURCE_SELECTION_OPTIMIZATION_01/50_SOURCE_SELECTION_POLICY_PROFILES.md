---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_SOURCE_SELECTION_POLICY_PROFILES
doc_type: policy
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 50_SOURCE_SELECTION_POLICY_PROFILES

## Policy rule

```text
Data Center arbitre la source.
Data Center ne decide pas l'usage.
```

Plus precis :

```text
Data Center source selector chooses the best data candidate according to an explicit policy.
Consumers decide how to use that data.
```

## Policy profiles V1

| Policy | Consumer cible | Selection |
|---|---|---|
| `policy_deskpro_context` | DeskPro | meilleure source fraiche, fallback tolere avec warning |
| `policy_strategy_features` | Strategy | source stable, normalisee, pas OCR si API existe |
| `policy_perf_replay` | Perf / replay | historique reproductible, pas latest-only si replay |
| `policy_sheets_reporting` | Google Sheets | erreur si source reporting absente |
| `policy_telegram_context` | Telegram | contexte enrichi seulement si fresh, sinon alerte sans contexte |
| `policy_debug_all_candidates` | debug / audit | retourne toutes les candidates, aucune selection finale |

## Score vectoriel minimal

```text
source_reliability_score
freshness_score
schema_validation_score
completeness_score
cross_source_consistency_score
latency_score
historical_accuracy_score
permission_score
manual_override_score
```

## Selection trace minimale

Toute selection doit conserver :

```text
data_key
symbol_or_scope
policy
selected_source_id
selected_score
candidate_count
selection_reason
registry_checksum
source_candidates_checksum
selected_at
```

## Interdits

- Pas de selection sans policy.
- Pas de score final sans score vectoriel.
- Pas de suppression des candidates rejetees.
- Pas de selection trading dans Data Center.
