---
doc_id: GO_UNIFORM_CONTINUITY_HARDENING_01_PLAN
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_UNIFORM_CONTINUITY_HARDENING_01
status: active
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - continuity
  - hardening
  - indexes
surface: chantier
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/00_cadrage.md
---

# 01_plan — GO_UNIFORM_CONTINUITY_HARDENING_01

## But du plan
- but : synchroniser les index restants avec l’état réel des pilotes et des points de reprise
- ordre d’exécution retenu : vérifier les écarts -> mettre à jour `opt-trading` -> mettre à jour `localcms` -> fermer le lot

## Étapes
1. relever les écarts réels entre index et closeouts pilotes
2. mettre à jour `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `REPRISE.md`, `NEXT_GO_CANDIDATES.md` dans `opt-trading`
3. mettre à jour les index locaux utiles dans `localcms`
4. fermer le hardening avec un closeout court

## Validations prévues
- cohérence entre index et closeouts PASS
- cohérence entre index et prochain point de reprise réel
- absence de nouveau chantier métier ouvert dans ce lot

## RISKS

- À qualifier.
