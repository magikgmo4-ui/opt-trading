---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_APPLY_OUTCOMES_PIPELINE_INTEGRATION_01
doc_type: contract
---

# Contrat pipeline intégré

## `batch_run(args) → int`

```
args[0]: csv_path (optionnel, défaut: SAMPLE_MARKET_CSV)
args[1]: session_id filter (optionnel)
args[2]: start_date filter (optionnel, YYYY-MM-DD)
args[3]: end_date filter (optionnel, YYYY-MM-DD)
```

Itère toutes les sessions activées × toutes les dates disponibles dans le CSV. Appelle `process_market_run` pour chaque combinaison. Sortie JSON : `{runs_done, csv}`.

## `run_with_outcomes(args) → int`

```
args[0]: csv_path (optionnel, défaut: SAMPLE_MARKET_CSV)
args[1..]: transmis à batch_run (session_id, start_date, end_date)
```

Séquence atomique :
1. Efface FEATURES_JSONL, EVENTS_JSONL, TRADES_JSONL
2. Appelle `batch_run`
3. Appelle `apply_outcomes` avec le même csv_path
4. Appelle `batch_report` (sans filtre)

Sortie : 3 blocs JSON consécutifs (batch_run, apply_outcomes, batch_report).

## Garantie d'idempotence

Chaque appel à `run_with_outcomes` efface les trades précédents et repart de zéro. Résultat déterministe sur le même CSV.

## Compatibilité backward

`apply-outcomes` et `batch-report` restent des commandes indépendantes. `batch_run` peut être utilisé seul pour générer des trades sans résolution.
