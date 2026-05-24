---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01_REPRISE
doc_type: reprise
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_READONLY_WRAPPERS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE

## État

Chantier child ouvert pour matérialiser des wrappers read-only fixtures-first, attaché à :

- parent : `GO_DESKPRO_INPUT_EXPANSION_01`

## État établi (repo-first)

Pattern read-only existant :

- `modules/desk_pro/signal_event_adapter.py` : normalize + validate + read (no side effects)

Assemblage dry-run (no runtime live) :

- `modules/desk_pro/dry_run.py` compose :
  - `signal_event` (V0→V1)
  - `desk_snapshot` (contrat minimal)
  - `visual_context` (contrat minimal)

Reader vision context existant (read-only) :

- `modules/desk_pro/service/vision_context_reader.py` lit `vision_context.coinglass.v1` depuis `data/deskpro/inputs/.../latest.json`

## Point de reprise (next step)

1) Décider si un wrapper dédié doit être ajouté pour :
   - `desk_snapshot.v1`
   - `visual_context.v1`
   ou si les validations internes `dry_run.py` suffisent à ce stade.
2) Si wrappers ajoutés :
   - les placer dans `modules/desk_pro/` en cohérence avec `signal_event_adapter.py`
   - ajouter fixtures + tests unitaires (no side effects)
3) Préparer contrats/fixtures pour `vision_analysis.v1`, `market_metrics.v1`, `telegram_claim.v1` sans implémentation runtime live.

## Contraintes rappel

- pas de runtime live
- pas de Telegram live
- pas d’écriture Google Sheets
- pas de secrets
- pas d’index globaux sans nécessité prouvée

