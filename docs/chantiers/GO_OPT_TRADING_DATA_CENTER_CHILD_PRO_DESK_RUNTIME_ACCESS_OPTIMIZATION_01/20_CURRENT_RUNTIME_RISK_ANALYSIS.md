---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_RUNTIME_ACCESS_PROBLEM
doc_type: analysis
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
---

# 10_RUNTIME_ACCESS_PROBLEM

## Objet

Diagnostiquer le probleme d'acces runtime aux inventaires avant que DeskPro ou Strategy commencent a requeter massivement.

## 1. Situation actuelle

```text
modules/data_center/registry/
├── producers.json              (7 entries, ~3 KB)
├── consumers.json              (14 entries, ~5 KB)
├── pro_desk_data_inventory.json (~500 fields, ~150 KB)
└── source_candidates.json      (31 sources, ~30 KB)
```

Environnement de lecture actuel :
- `market_metrics_reader.py` lit `views/market_metrics/latest.json`
- `spot_snapshot_reader.py` lit `views/pair_market_snapshot/latest.json`
- Les readers DeskPro lisent des fichiers individuels, pas l'inventaire complet

Probleme futur :
- Quand les inventaires `pro_desk_data_inventory.json` et `source_candidates.json` seront utilises pour le source selector / resolver
- Chaque requete `resolve(contract_class, symbol, data_key)` devra croiser :
  - l'inventaire pour verifier que le data_key existe et sa priorite
  - les sources candidates pour lister les producers eligibles
  - le scoring pour choisir la meilleure source

## 2. Goulot identifie

```text
Requete: resolve("market_metrics.v1", "BTCUSDT", "open_interest")
    │
    ├── lit pro_desk_data_inventory.json (150 KB parse)
    ├── lit source_candidates.json (30 KB parse)
    ├── lit producers.json (3 KB parse)
    ├── calcule source_score pour chaque candidat
    ├── selectionne meilleur
    └── retourne canonical_value

Si 10 consumers × 10 symboles × 6 data_keys = 600 appels :
    → 600 × (150 + 30 + 3) = ~110 MB de JSON parse
    → ~10-30 secondes CPU juste pour parser les inventaires
```

## 3. Profil d'acces

| Type de donnee | Taille | Frequence acces | Modifie |
|---|---|---|---|
| pro_desk_data_inventory | ~150 KB | CHAQUE requete resolve() | Rarement (doc-only) |
| source_candidates | ~30 KB | CHAQUE requete resolve() | Rarement (ajout source) |
| producers.json | ~3 KB | CHAQUE requete resolve() | Ajout/retrait producer |
| consumers.json | ~5 KB | CHAQUE requete consumer setup | Ajout/retrait consumer |
| Contract schemas | ~2 KB/contract | Validation chaque write | Changement schema |
| Source scores | ~2 KB/source | A chaque scoring | Chaque evaluation |

## 4. Impact

```text
SANS OPTIMISATION :
  - 600 resolve()/min → 110 MB JSON parse/min → CPU bound
  - Latence p99 > 500ms par resolve
  - Risque de contention I/O si plusieurs consumers

AVEC OPTIMISATION :
  - Index compiles en memoire → 0 KB JSON parse par resolve
  - Latence p99 < 5ms par resolve
  - Pas de contention I/O
```

## 5. Separation des preoccupations

```text
COLD PATH (rare, lent accepte) :
  - Modification inventaire (ajout champ P0-P21)
  - Ajout source candidate
  - Registration nouveau producer/consumer
  - Mise a jour schema contract

HOT PATH (frequent, doit etre < 5ms) :
  - resolve(contract_class, symbol, data_key)
  - Validation schema d'un write producer
  - Lecture view par consumer
  - Check freshness / stale flag

## 6. Analyse de risques runtime (R01-R10)

### R01 — Latence de parsing > seuil consumer

```text
Risk:  un consumer (DeskPro) fait 100 resolve() par cycle dashboard.
       Sans optimisation, chaque resolve parse 150 KB JSON → 100 × 11ms = 1.1s.
Impact: UI lag, timeout, donnees manquantes dans le dashboard.
Mitigation: compiled indexes + memory cache (target <0.1ms per resolve).
```

### R02 — Contention I/O multi-consumers

```text
Risk:  10 consumers concurrents lisent les memes JSON files.
       I/O bound, mutex implicite du filesystem.
Impact: p99 latency explose, certains consumers timeout.
Mitigation: cache memoire partage (read-only pour hot path, lock-free).
```

### R03 — Corruption fichier registre

```text
Risk:  ecriture concurrente ou crash pendant write de pro_desk_data_inventory.json.
Impact: JSON parse fail → cache rebuild fail → tout le hot path retourne stale.
Mitigation: atomic write (write temp + rename), hash SHA256 verification avant rebuild.
```

### R04 — Cache stale apres modification inventaire

```text
Risk:  ajout d'un champ P0-P21, cache pas encore rebuild, source selector ignore le champ.
Impact: nouvelle donnee invisible pour les consumers.
Mitigation: watchdog mtime/hash + rebuild async < 50ms + atomic swap.
```

### R05 — Source candidate non-scoree selectionnee

```text
Risk:  source_candidates.json a score=0 + status=candidate.
       Un bug dans le source selector selectionne cette source.
Impact: valeur non fiable injectee dans canonical_value sans avertissement.
Mitigation: regle explicite score=0 + candidate = non selectable. eligible_statuses whitelist.
```

### R06 — Desynchro producer registry vs source candidates

```text
Risk:  producers.json retire un producer, source_candidates.json le reference encore.
Impact: source selector cherche un producer disparu → erreur ou stale fallback.
Mitigation: sanity check au rebuild: all active_registry producer_ids exist in producers.json.
```

### R07 — Memory leak du cache

```text
Risk:  cache garde des references mortes (anciens producers, anciens symboles).
Impact: memoire croit lentement, OOM sur long uptime.
Mitigation: cache taille fixe (~405 KB), rebuild complet (pas incremental), swap atomique.
```

### R08 — Atomic swap race condition

```text
Risk:  deux rebuilds concurrents (ex: modification inventaire + modification producers.json).
Impact: le second rebuild ecrase le premier, donnees intermediaires perdues.
Mitigation: rebuild mutex (threading.Lock), pas de rebuild si un autre est en cours.
```

### R09 — Source selector decision non tracee

```text
Risk:  source selector choisit une source sans produire resolver_decision.v1.
Impact: impossible d'auditer pourquoi cette valeur a ete choisie, lineage casse.
Mitigation: toute selection produit resolver_decision.v1 obligatoirement (cf child 4+5).
```

### R10 — Fallback silencieux sans alerte

```text
Risk:  toutes les sources stale → source selector retourne derniere valeur connue.
       Consumer ne sait pas que la donnee est perimee.
Impact: decision trading sur donnee obsolete.
Mitigation: canonical_value.v1.stale = true + freshness_state = stale visible dans DeskPro.
```

