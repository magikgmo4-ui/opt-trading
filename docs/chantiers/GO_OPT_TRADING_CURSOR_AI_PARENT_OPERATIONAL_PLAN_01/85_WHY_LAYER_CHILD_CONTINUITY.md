---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_85_WHY_LAYER_CHILD_CONTINUITY
doc_type: chantier/parent_continuity
repo: opt-trading
machine: cursor-ai
parent_go: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01
child_go: GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01
branch: go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01
status: active
surface: docs/chantiers
---

# 85_WHY_LAYER_CHILD_CONTINUITY

## 1_MASTER_TARGET

Rattacher le child GO `GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01` au parent cursor-ai sans modifier les index globaux, sauf le bloc machine anti-conflit explicitement demandé.

## 3_INITIAL_NEED

Transformer l'audit du "pourquoi" deja present dans la documentation du repo en chantier doc-only rattache a cursor-ai.

## 5_GO_PLAN

- Parent: `GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01`
- Child: `GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01`
- Branche dediee: `go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01`
- Machine: cursor-ai
- Type: doc-only

## 7_CANONICAL_STATE

Le repo contient deja une couche WHY diffuse: intentions produit, invariants, arbitrages, gates, reprise et anti-derive. Le gap valide est la dispersion de cette couche, non son absence.

## 8_VALIDATED_PLAN

1. Creer le child GO dans `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01/`.
2. Documenter l'audit WHY layer.
3. Documenter les gaps et templates recommandes.
4. Rattacher le child au parent cursor-ai par ce fichier de continuite.
5. Rattacher la branche au bloc `CURSOR_AI` de `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01` uniquement.

## 12_INVARIANTS

- Ne pas modifier le runtime.
- Ne pas modifier `GO_INDEX`.
- Ne pas modifier `BRANCH_STATE`.
- Ne pas modifier `REPRISE`.
- Ne pas modifier la matrice globale.
- Ne pas promouvoir automatiquement ce child en statut global.
- Le rattachement machine dans `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01` est l'exception explicitement demandee.

## 16_TODO

- Finaliser la PR doc-only.
- Verifier que le diff reste limite aux docs de chantier parent/child et au bloc `CURSOR_AI` de la fiche anti-conflit.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01`, depuis le child GO, avec comme contrainte centrale: documenter le WHY layer sans toucher aux index globaux ni au runtime.
