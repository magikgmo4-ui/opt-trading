---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01_PRODUCER_CONTRACT_SPEC
doc_type: data_contract_spec
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_PRODUCER_CONTRACT_SPEC — Format canonique d'un contrat producer Data Center

## Objet

Définir ce qu'est un contrat producer dans le contexte du Data Center `PF_DATA_CENTER`.

Un contrat producer est une déclaration qui permet au Data Center de savoir **qui écrit quoi, où, dans quel format, avec quelle couverture**.

## Contrat producer — champs canoniques

```yaml
# Identité
producer_id: <string unique — ex: derivatives_collector__bitget, binance_spot>
family: derivatives | spot | events | vision | signals | other
schema_version: v1       # version du contrat lui-même
contract_class: <string> # nom du format payload — ex: market_metrics.v1, pair_market_snapshot.v1

# Stockage Data Center
output_path_root: data/data_center/<family>/<producer_id>/
write_mode: atomic       # atomic = écriture atomique via tempfile.replace ; append = jsonl

# Temporalité
latency_class: oneshot | scheduled | realtime
run_trigger: manual | cron | event_driven

# Couverture metrics (si applicable)
collectable_metrics: []  # métriques effectivement collectées et non nulles
missing_metrics: []      # métriques absentes ou toujours nulles
coverage_status: full | partial | not_proven_runtime_adapter | spot_only

# Méta
validated_at: <YYYY-MM-DD>  # date de dernière validation par test smoke ou CI
notes: ""
```

## Invariants

1. `producer_id` est unique dans le registre.
2. `family` détermine le sous-répertoire dans `data/data_center/<family>/`.
3. `contract_class` doit correspondre à un schéma documenté (ex: `market_metrics.v1` dans `20_MARKET_METRICS_V1_CONTRACT.md`).
4. `coverage_status: not_proven_runtime_adapter` signifie que le producer écrit mais que sa source externe n'est pas prouvée en runtime (ex: Coinglass).
5. Un producer sans `validated_at` est déclaré mais non testé.
6. Un producer ne peut pas écrire en dehors de `data/data_center/<family>/<producer_id>/`.

## Layout fichiers attendu par producer

Chaque producer écrit dans son répertoire selon le pattern :

```text
data/data_center/<family>/<producer_id>/
  raw/                                  <- captures brutes horodatées (non écrasées)
  normalized/                           <- payloads normalisés horodatés (non écrasés)
  latest.json                           <- dernier payload valide (atomic overwrite)
  manifest.json                         <- inventaire des artefacts du dernier run
  status.json                           <- état runtime (fresh/stale/error + ts)
  events.jsonl                          <- log append-only des runs réussis
  errors.jsonl                          <- log append-only des erreurs
  cache/
    by_symbol/<SYMBOL>.json             <- accès rapide par symbole (si applicable)
```

## Registre des producers

Le Data Center maintient un registre global des producers actifs à :

```text
data/data_center/_registry/producers.json
```

Format :

```json
{
  "registry_version": "v1",
  "updated_at": "<ISO timestamp>",
  "producers": [
    {
      "producer_id": "<string>",
      "family": "<string>",
      "contract_class": "<string>",
      "schema_version": "v1",
      "output_path_root": "data/data_center/<family>/<producer_id>/",
      "coverage_status": "<string>",
      "validated_at": "<YYYY-MM-DD>",
      "last_write": "<ISO timestamp | null>"
    }
  ]
}
```

## Relation avec collectors_core

Les producers basés sur `collectors_core` héritent du layout `raw/`, `normalized/`, `latest.json`, `manifest.json`, `status.json`, `events.jsonl`, `errors.jsonl` nativement.

Pour ces producers, l'adaptation au Data Center consiste à :
1. Déclarer leur contrat dans le registre `producers.json`.
2. Écrire dans `data/data_center/<family>/<producer_id>/` au lieu de (ou en plus de) `data/collectors/<family>/`.

## Anti-patterns

| Interdit | Raison |
|---|---|
| Producer sans `producer_id` déclaré | Pas de traçabilité ni de registre |
| Producer écrivant en dehors de son `output_path_root` | Viole le contrat d'isolation |
| Metric toujours null déclarée dans `collectable_metrics` | Fausse la couverture |
| `coverage_status: full` sans `validated_at` récent | Non prouvé |
| Simulation ou interpolation de métriques manquantes | Interdit sans flag explicite |
