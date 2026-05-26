---
doc_id: GO_OPT_TRADING_MODULE_FAMILY_P2_CLOSEOUT_01_REMAINING_GAPS
doc_type: gap_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_MODULE_FAMILY_P2_CLOSEOUT_01
status: draft_for_review
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - modules
  - family
  - p2
  - gaps
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-26
links:
  - docs/chantiers/GO_OPT_TRADING_MODULE_FAMILY_P2_CLOSEOUT_01/10_P2_DELIVERY_SUMMARY.md
  - docs/chantiers/GO_OPT_TRADING_MODULE_FAMILY_P2_CLOSEOUT_01/20_APPLIED_VS_DOC_ONLY.md
---

# 30_REMAINING_GAPS

## Gap G1 - `deepseek_student` central registry status

- l'etat runtime/famille est clarifie: legacy/transitional, hors verite canonique actuelle
- il reste hors registries centrales par choix explicite
- un GO dedie doit decider soit un vrai statut central `legacy`, soit une fermeture physique/runtime d'abord

## Gap G2 - `machine_target` is too coarse

- plusieurs lots P2 montrent que `machine_target` ne distingue pas assez bien facade operateur, runtime reel, support auxiliaire, ou surface cross-machine
- le cas `student`, `msi_db_layer`, `admin_trading`, `any` reste utile mais trop plat pour certaines stacks
- un futur contrat source-of-truth registry doit dire si ce champ est enrichi, derive, ou complete par une autre dimension

## Gap G3 - Physical/runtime cleanup remains separate

- `desk` garde des questions d'absorption physique et de frontieres entre owner, facade et satellites
- `deepseek` garde la frontiere `modules/deepseek_student/`, `scripts/student/`, `student/scripts/`
- `openclaw` garde des extensions runtime/e2e distinctes de la simple representation registry

## Gap G4 - Registry source-of-truth contract still not fully explicit

- P2 a applique plusieurs realignements centraux utiles
- il reste a formaliser quels registres sont source de verite, quelles vues sont derivees, et comment les divergences doivent etre traitees

## Next GO candidates

1. `GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01` ou equivalent si la priorite est la dette DeepSeek residuelle
2. `GO_OPT_TRADING_DESK_STACK_PHYSICAL_ABSORPTION_CADRAGE_01` si la priorite est cleanup physique Desk
3. `GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01` si la priorite est governance transverse

## Recommended next

Le meilleur point d'appui transverse apres ce closeout P2 est:

- `GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01`

Alternative si priorite runtime:

- `GO_OPT_TRADING_DESK_STACK_PHYSICAL_ABSORPTION_CADRAGE_01`
- ou un GO dedie `deepseek_student` boundary/legacy
