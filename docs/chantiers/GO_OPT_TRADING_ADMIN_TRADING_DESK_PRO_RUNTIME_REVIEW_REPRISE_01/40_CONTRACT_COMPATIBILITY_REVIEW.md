---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01_CONTRACT_COMPATIBILITY
doc_type: contract_compatibility_review
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 40_CONTRACT_COMPATIBILITY_REVIEW - Contract Compatibility Review

## Desk Pro peut-il consommer signal_event V1?

### État actuel

Desk Pro **ne consomme pas** `signal_event` directement. Le runtime lit :
- `desk/snapshots/latest.json` (snapshots visuels)
- `desk/inputs/tv_inputs_latest.json` (extractions TV)
- Modules internes (probability_engine, decision_engine, etc.)

### Compatibilité V1

| Champ signal_event V1 | Desk Pro a-t-il besoin? | Disponible? | Gap |
| --- | --- | --- | --- |
| `source` | oui (pour traçabilité) | non produit | adapter nécessaire |
| `event_type` | oui (pour filtrage) | non produit | adapter nécessaire |
| `engine` | oui (pour routage) | oui (dans events.jsonl) | mapping V0→V1 |
| `symbol` | oui (pour jointure) | oui | normalisation `BTCUSDT` vs `BTCUSDT.P` |
| `timeframe` | oui (pour jointure) | oui (alias `tf`) | mapping |
| `direction` | oui (pour décision) | oui (alias `signal`) | mapping |
| `timestamp` | oui (pour fraîchesse) | oui (alias `_ts`) | mapping |
| `status` | oui (pour filtrage) | non explicite | derive |
| `payload_hash` | optionnel | non produit | futur |
| `visual_context_ref` | optionnel | non produit | futur |
| `desk_snapshot_ref` | optionnel | non produit | futur |

### Verdict signal_event

Desk Pro peut consommer `signal_event` V1 **avec un adapter** qui :
1. Lit `state/events.jsonl`
2. Mappe V0 → V1 (signal→direction, tf→timeframe, _ts→timestamp)
3. Normalise les symboles (BTCUSDT → BTCUSDT.P)
4. Expose les signaux dans un format consumable par le pipeline

**Pas de blocage contractuel** — l'adapter est une couche d'intégration, pas un breaking change.

## Desk Pro peut-il consommer visual_context V1?

### État actuel

Desk Pro **consomme indirectement** `visual_context` via :
- `desk/snapshots/latest.json` → PNG paths → `desk_analyze` (OpenAI vision)
- Les PNG sont les artefacts bruts de la pipeline vision

### Compatibilité V1

| Champ visual_context V1 | Desk Pro a-t-il besoin? | Disponible? | Gap |
| --- | --- | --- | --- |
| `source` | oui (pour traçabilité) | `source: null` dans latest.json | enrichissement nécessaire |
| `capture_id` | optionnel | non produit | futur |
| `symbol` | oui (pour jointure) | oui | direct |
| `timeframe` | oui (pour jointure) | oui (`tf`) | direct |
| `captured_at` | oui (pour fraîchesse) | oui (`snapshot_ts`) | mapping |
| `image_ref` | oui (pour vision) | oui (`path`) | direct |
| `status` | oui (pour filtrage) | non produit | derive |
| `payload_hash` | optionnel | non produit | futur |
| `signal_event_ref` | optionnel | non produit | futur |

### Verdict visual_context

Desk Pro **peut déjà consommer** les artefacts `visual_context` via `desk/snapshots/latest.json`. Le sidecar JSON V1 n'est pas lu par Desk Pro, mais les champs essentiels (symbol, timeframe, path) sont disponibles.

**Pas de blocage** — enrichissement du sidecar recommandé mais non bloquant.

## Desk Pro peut-il consommer desk_snapshot?

### État actuel

Desk Pro **consomme directement** `desk_snapshot` via :
- `desk/snapshots/latest.json` (index)
- `desk/snapshots/{SYMBOL}/{SYMBOL}_H1_{ts}.png` (images)

### Compatibilité

| Champ desk_snapshot | Desk Pro a-t-il besoin? | Disponible? | Gap |
| --- | --- | --- | --- |
| `symbol` | oui | oui | direct |
| `tf` | oui | oui | direct |
| `snapshot_ts` | oui (pour fraîchesse) | oui | direct |
| `path` | oui (pour accès image) | oui | direct |
| `ingested_at` | optionnel | oui | direct |
| `source` | optionnel | `null` | enrichissement |
| `host` | optionnel | `null` | enrichissement |

### Verdict desk_snapshot

Desk Pro **consomme déjà** `desk_snapshot` de manière fonctionnelle. Les champs `source` et `host` sont null mais non bloquants.

**Aucun gap bloquant.**

## Desk Pro synthesis/report contract

### Contrat d'entrée Desk Pro (observé)

Desk Pro orchestrator attend un fichier de config JSON (`run_config.example.json`) qui liste les modules à exécuter. Chaque module a ses propres inputs.

### Inputs directs par module

| Module | Input principal | Source |
| --- | --- | --- |
| market_scanner | sample config | interne |
| liquidation_analyzer | sample config | interne |
| probability_engine | sample config | interne |
| opportunity_ranker | sample config | interne |
| decision_engine | sample config | interne |
| risk_engine | sample config | interne |
| execution_engine | sample config | interne |
| position_engine | sample config | interne |
| perf_engine | sample config | interne |
| journal_engine | sample config | interne |
| portfolio_engine | sample config | interne |

### Observations

1. Les modules utilisent des **sample configs** (mode PAPER), pas des inputs live
2. `desk_state` agrège les données mais n'est pas directement consommé par les modules du pipeline
3. `desk_analyze` est séparé du pipeline orchestrator (Telegram /analyze)
4. Les modules ne lisent pas `signal_event`, `visual_context` ou `desk_snapshot` directement

### Gap principal

Desk Pro n'a **pas d'adapter** pour consommer les contrats V1. Le pipeline fonctionne en mode sample/mock. Pour une intégration réelle :
1. Chaque module devrait lire ses inputs depuis les contrats V1
2. Un adapter `signal_event → decision_engine` serait nécessaire
3. Un adapter `visual_context → probability_engine` serait nécessaire

## Matrice de compatibilité

| Contract | Required by Desk Pro | Available now | Gap | Adapter needed |
| --- | --- | --- | --- | --- |
| signal_event V1 | oui (pour décision live) | events.jsonl (V0) | mapping V0→V1, normalisation symbol | oui |
| visual_context V1 | oui (pour analyse visuelle) | desk/snapshots/latest.json | sidecar non lu, source null | non (déjà consommé) |
| desk_snapshot | oui (pour snapshots) | desk/snapshots/latest.json | source/host null | non (déjà consommé) |
| desk_state | oui (pour agrégat) | desk/state/latest.json | STALE (2 mois) | non (relancer desk_state) |
| Desk Pro synthesis | operator | data/desk_runs/ | non automatisé | non (manuel) |

## Jointures symbol/timeframe/timestamp/ref/hash

### Jointure signal_event ↔ desk_snapshot

| Join key | Signal Event | Desk Snapshot | Fiabilité |
| --- | --- | --- | --- |
| `symbol` | `symbol` (V1) | `symbol` | haute (normalisation nécessaire: `BTCUSDT` → `BTCUSDT.P`) |
| `timeframe` | `timeframe` (V1) | `tf` | haute |
| `timestamp` fenêtre | `timestamp` (V1) | `snapshot_ts` | moyenne (±5min pour H1) |

### Jointure signal_event ↔ visual_context

Documentée dans `50_SIGNAL_EVENT_ENRICHMENT_COMPATIBILITY.md` (GO précédent).

### Jointure desk_snapshot ↔ visual_context

| Join key | Desk Snapshot | Visual Context | Fiabilité |
| --- | --- | --- | --- |
| `symbol` | `symbol` | `symbol` | haute |
| `timeframe` | `tf` | `timeframe` | haute |
| `snapshot_ts` | `snapshot_ts` | `captured_at` | haute (même source) |

## Verdict global

Desk Pro peut être décrit comme consumer final de `signal_event + visual_context + desk_snapshot` :
- `desk_snapshot` est déjà consommé (CONFIRMED)
- `visual_context` est consommé indirectement via snapshots (AVAILABLE)
- `signal_event` nécessite un adapter V0→V1 (ADAPTER NEEDED)
- Les contrats V1 sont compatibles sans breaking change
- Les gaps sont des lacunes d'intégration, pas des blocages contractuels
