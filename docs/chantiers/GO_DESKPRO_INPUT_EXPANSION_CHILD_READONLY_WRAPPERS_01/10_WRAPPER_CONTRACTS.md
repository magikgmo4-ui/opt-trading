---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01_WRAPPER_CONTRACTS
doc_type: contracts
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 10_WRAPPER_CONTRACTS

## Principe (pattern repo)

Le repo contient déjà un pattern “read-only adapter” :

- `normalize_*` : conversion vers un format V1 canonical
- `validate_*` : validation (blocking vs non-blocking)
- `read_*` : lecture depuis un artefact (JSON/JSONL) sans écrire ni side effects

Références :

- `modules/desk_pro/signal_event_adapter.py`
- `modules/desk_pro/dry_run.py`
- tests : `tests/test_signal_event_adapter.py`, `tests/test_desk_pro_dry_run.py`

## Contrats cibles (classes)

### 1) `signal_event.v1` (existant)

Source canonique actuelle : `modules/desk_pro/signal_event_adapter.py`

Champs structurants observés :

- `source` = `tradingview.webhook`
- `event_type` = `signal_event`
- `engine`, `symbol`, `timeframe`, `direction`, `timestamp`
- `status` (`accepted|rejected|skipped|error`)
- `payload_hash`
- refs (à compléter plus tard) :
  - `visual_context_ref`
  - `desk_snapshot_ref`

### 2) `desk_snapshot.v1` (déjà utilisé)

Contrat minimal déjà consommé par `modules/desk_pro/dry_run.py` :

```text
{ symbol, tf, snapshot_ts, path }
```

Statut : “présent mais non normalisé” (pas encore de wrapper dédié identifié).

### 3) `visual_context.v1` (déjà utilisé)

Contrat minimal déjà consommé par `modules/desk_pro/dry_run.py` :

Champs requis (validation interne actuelle) :

```text
source, capture_id, symbol, timeframe, captured_at, image_ref, status
```

Statut : “présent mais non normalisé” (pas encore de wrapper dédié identifié).

### 4) `vision_analysis.v1` (contractuel)

But : produire une vision structurée consommable par Desk Pro (pas de headless live ici).

Contrat à définir “fixtures-first” :

- `input_class = vision_analysis.v1`
- `symbol`, `timeframe`, `captured_at`
- `analysis` (structure minimale, ex: `zones`, `labels`, `confidence`)
- refs :
  - `visual_context_ref`
  - `desk_snapshot_ref`

### 5) `market_metrics.v1` (partiellement présent)

Le repo contient déjà :

- reader : `modules/desk_pro/service/market_metrics_reader.py`
- writer côté collector : `modules/derivatives_collector/app/market_metrics_writer.py`

Mais la classe “Desk Pro hub input” doit rester read-only ici.

Contrat “fixtures-first” (minimal) :

- `input_class = market_metrics.v1`
- `symbol`
- `as_of_ts`
- `metrics[]` (clé/valeur + unit + quality)

### 6) `telegram_claim.v1` (contractuel)

Interdiction : pas de Telegram live dans ce GO.

Contrat “fixtures-first” (minimal) :

- `input_class = telegram_claim.v1`
- `claim_id`
- `source_chat` (id/alias, sans secrets)
- `received_at`
- `symbol` (si détectable)
- `intent` (ex: `open`, `close`, `status`, `question`)
- `raw_text_ref` (ref artefact local, pas de contenu secret)

## Décision de placement (code)

Wrappers à créer uniquement si une surface naturelle est déjà utilisée :

- `modules/desk_pro/` (adapters/readers déjà présents)
- `tests/` + `tests/fixtures/` (fixtures-first déjà présent)

