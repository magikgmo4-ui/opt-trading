---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01_FIXTURE_PLAN
doc_type: plan
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_FIXTURE_PLAN

## Objectif

Adopter une stratégie fixtures-first pour matérialiser les wrappers read-only.

## Surface fixtures (existante)

Le repo utilise déjà des fixtures JSON pour Desk Pro / signal_event :

- `tests/fixtures/admin_trading_contract_smoke/`

## Plan fixtures

### A. Fixtures “présentes” (réutiliser)

- `signal_event_v0_minimal.json`
- `signal_event_v0_complete.json`
- `desk_snapshot_minimal.json`
- `visual_context_v1_minimal.json`

Objectif : éviter tout doublon.

### B. Nouvelles fixtures (à créer si wrappers ajoutés)

Créer un sous-dossier dédié child (pour éviter de polluer le parent) :

```text
tests/fixtures/deskpro_input_expansion_readonly_wrappers/
```

Nouvelles fixtures proposées :

- `desk_snapshot_v1_minimal.json`
- `visual_context_v1_complete.json`
- `vision_analysis_v1_minimal.json` (contractuel)
- `market_metrics_v1_minimal.json` (contractuel)
- `telegram_claim_v1_minimal.json` (contractuel)

Contraintes :

- pas de valeurs secrètes
- pas d’identifiants Telegram réels si sensibles (utiliser placeholders non secrets)
- timestamps ISO avec timezone

## Résultat attendu côté tests

- tests unitaires qui valident :
  - normalize + validate (si wrapper existe)
  - lecture read-only depuis un path fixture
- aucune écriture hors `tmp_path` pytest

