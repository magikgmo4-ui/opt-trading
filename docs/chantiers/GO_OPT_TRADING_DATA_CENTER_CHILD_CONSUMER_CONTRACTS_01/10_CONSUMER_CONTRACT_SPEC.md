---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01_CONSUMER_CONTRACT_SPEC
doc_type: data_contract_spec
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_CONSUMER_CONTRACT_SPEC — Format canonique d'un contrat consumer Data Center

## Objet

Définir ce qu'est un contrat consumer dans le contexte du Data Center `PF_DATA_CENTER`.

Un contrat consumer est une déclaration qui permet au Data Center de savoir **qui lit quoi, depuis quel path, avec quelle tolérance de fraîcheur et quel comportement en cas d'absence ou d'erreur**.

## Contrat consumer — champs canoniques

```yaml
# Identité
consumer_id: <string unique — ex: desk_pro__market_metrics, perf_engine__replay>
surface: <PF_* — surface consommatrice>
contract_class: <string — doit correspondre à un contract_class producer connu>

# Lecture
read_path: data/data_center/<family>/<producer_id>/latest.json
             | data/data_center/<family>/<producer_id>/cache/by_symbol/<SYMBOL>.json
             | data/data_center/<family>/<producer_id>/normalized/
             | data/data_center/<family>/<producer_id>/status.json
access_pattern: latest_only | by_symbol | status_only | full_history | manifest_only
read_mode: pull   # toujours pull (pas de push depuis le Data Center)

# Tolérance
latency_tolerance: oneshot | near-realtime | batch
freshness_min: fresh_only | stale_ok | any
fallback: silent_empty | stale_ok | error | block

# État implémentation
implementation_status: implemented | planned | not_started
read_path_current: <path actuel si différent du path Data Center cible | null>
migration_needed: true | false
validated_at: <YYYY-MM-DD | null>
notes: ""
```

## Valeurs de fallback

| Valeur | Comportement si données absentes ou erreur |
|---|---|
| `silent_empty` | Retourne une liste/dict vide. Ne lève pas d'exception. Usage : UI, cockpit, contexte optionnel. |
| `stale_ok` | Retourne les dernières données connues même si stale. Usage : lecture de contexte enrichi non bloquant. |
| `error` | Lève une exception ou log une erreur explicite. Usage : reporting, export, pipeline obligatoire. |
| `block` | Bloque l'opération jusqu'à disponibilité. Usage : pipeline synchrone critique (rare). |

## Access patterns

| Pattern | Description | Fichier(s) lus |
|---|---|---|
| `latest_only` | Dernière capture valide, un seul payload | `latest.json` |
| `by_symbol` | Accès rapide par symbole cible | `cache/by_symbol/<SYMBOL>.json` |
| `status_only` | Vérification fraîcheur / health sans lire le payload | `status.json` |
| `full_history` | Accès à tous les payloads horodatés (replay, backtest) | `normalized/` |
| `manifest_only` | Inventaire des artefacts disponibles | `manifest.json` |

## Invariants

1. `consumer_id` est unique dans le registre.
2. Un consumer ne peut que **lire** depuis `data/data_center/` — jamais écrire.
3. `contract_class` doit correspondre à un `contract_class` déclaré dans le registre producers.
4. `fallback: silent_empty` est le défaut recommandé pour les surfaces UI.
5. `fallback: error` est obligatoire pour les consumers de reporting ou d'export critique.
6. Un consumer avec `migration_needed: true` doit indiquer `read_path_current` (path actuel non-Data-Center).
7. Un consumer non implémenté peut être déclaré dans le registre avec `implementation_status: not_started`.

## Registre des consumers

```text
data/data_center/_registry/consumers.json
```

Format :

```json
{
  "registry_version": "v1",
  "updated_at": "<ISO timestamp>",
  "consumers": [
    {
      "consumer_id": "<string>",
      "surface": "<PF_*>",
      "contract_class": "<string>",
      "read_path": "<string>",
      "access_pattern": "<string>",
      "fallback": "<string>",
      "implementation_status": "implemented | planned | not_started",
      "migration_needed": true,
      "validated_at": "<YYYY-MM-DD | null>"
    }
  ]
}
```

## Anti-patterns

| Interdit | Raison |
|---|---|
| Consumer écrivant dans `data/data_center/` | Le Data Center est read-only côté consumer |
| Consumer sans `fallback` déclaré | Comportement undefined sur fichier absent |
| Consumer lisant `raw/` en production | `raw/` est pour audit/replay uniquement |
| `fallback: silent_empty` sur un export Sheets ou pipeline critique | Masque une panne |
| Consumer dont `contract_class` ne correspond à aucun producer | Contrat orphelin non vérifiable |
