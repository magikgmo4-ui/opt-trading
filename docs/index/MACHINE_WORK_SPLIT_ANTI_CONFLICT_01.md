---
doc_id: OPT_TRADING_MACHINE_WORK_SPLIT_ANTI_CONFLICT_01
doc_type: index
repo: opt-trading
project: opt-trading
status: reference
lifecycle_stage: continuity_index
topic_keys:
  - machines
  - routing
  - anti-collision
  - branches
  - continuity
  - work_split
surface: index
source_kind: canonical
updated_at: 2026-05-09
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/BRANCH_STATE.md
  - docs/index/BRANCH_PROJECT_MAP.md
  - docs/index/GO_INDEX.md
---

# MACHINE_WORK_SPLIT_ANTI_CONFLICT_01

## Objet

Cette fiche est la vue de routage machine anti-conflit du repo `opt-trading`.

Elle sert a :
- repondre aux demandes "chantiers pour <machine>" sans rearbitrage complet
- eviter les collisions Git entre machines
- offrir une lecture orientee machine du parc branches

## Source de verite

Cette fiche est une vue de routage machine, subordonnee a :
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/index/BRANCH_STATE.md`
- `docs/index/BRANCH_PROJECT_MAP.md`
- `docs/index/GO_INDEX.md`

La source canonique de statut branche reste `docs/index/BRANCH_STATE.md`.

## Regle de routage

Quand la demande est "chantiers pour <machine>", la reponse doit ressortir directement le bloc machine correspondant de cette fiche.

---

## Bloc CURSOR_AI

### DOC_OPS — WHY_LAYER_ACTIVE

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01` | WHY layer audit — doc-only ; rattache au parent cursor-ai ; aucun runtime ; aucun GO_INDEX |
