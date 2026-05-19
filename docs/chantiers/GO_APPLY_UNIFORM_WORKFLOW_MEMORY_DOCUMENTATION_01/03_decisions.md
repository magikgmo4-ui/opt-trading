---
doc_id: GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: documentary_normalization
go_id: GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01
status: active
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - continuity
  - headings
  - documentation
surface: chantier
source_kind: canonical
updated_at: 2026-04-18
links:
  - docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md
  - docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/90_closeout.md
  - docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/00_cadrage.md
---

# 03_decisions — GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01

## D1 — Chaîne hardening (pas de parent concurrent)
Ce GO est le GO canonique d’exécution attendu par la chaîne :
- `GO_UNIFORM_CONTINUITY_HARDENING_02` (règle + lot fermé + exclusions)

Il n’introduit pas un nouveau parent conceptuel concurrent : il applique la règle et reste borné.

## D2 — Lot fermé (périmètre figé)
Seuls les fichiers suivants sont autorisés :
- `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`
- `docs/ot/trading/22_RANGE_STRATEGY_V1_STRUCT_01.md`
- `docs/ot/reports/OT_RANGE_STRATEGY_V1_STRUCT_01.md`

## D3 — Normalisation headings uniquement
- appliquer uniquement les mappings à équivalence claire vers le tronc commun (`Besoin initial`, `Cible finale`, `Plan validé`, `ETABLI`, `Gap restant`, `Next GO`, `REPRISE`)
- ne pas réécrire le fond

## D4 — Parent actif PHASE 4 (justification continuité)
- `GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01` est assumé comme parent actif réel (PHASE 4 / LOT 7)
- cette ouverture contribue au passage de 10 à 11 GO non clos dans les index

## REPRISE
Point de reprise unique :
- `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/02_journal_technique.md`
