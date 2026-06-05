---
doc_id: GO_UNIFORM_CONTINUITY_HARDENING_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_UNIFORM_CONTINUITY_HARDENING_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - continuity
  - hardening
  - indexes
surface: chantier
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/next/NEXT_GO_CANDIDATES.md
---

# 00_cadrage — GO_UNIFORM_CONTINUITY_HARDENING_01

## Identité
- GO : GO_UNIFORM_CONTINUITY_HARDENING_01
- Repo : opt-trading
- Branche : sot/mainline
- Statut : active
- Type de travail : hardening documentaire ciblé

## État de départ retenu
- état repo retenu : le socle uniforme est posé sur 5 repos, mais certains index locaux restent en retard par rapport aux pilotes déjà clos
- artefacts existants retenus : index `opt-trading` et `localcms`, closeouts pilotes PASS, gouvernance locale et transverse
- limites connues : décalage réel entre état des chantiers et résumé indexé
- dépendances : aucune dépendance fonctionnelle, seulement cohérence documentaire

## Objectif du lot
- objectif principal : remettre les index locaux en cohérence avec l’état réel déjà posé
- résultat attendu : prochaine mise à jour des index `opt-trading` et `localcms` sans ouvrir de nouveau chantier métier

## Non-objectifs
- créer de nouveaux modules
- modifier le canon `memory_bricks`
- ouvrir un nouveau chantier métier dans `hf_trading`

## Critères PASS / FAIL
- PASS si : les index locaux reflètent au minimum les pilotes PASS et le prochain point de reprise réel
- FAIL si : les index restent en retard ou contradictoires après hardening

## RISKS

- À qualifier.
