---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01_INITIAL
doc_type: initial_project_doc
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
pf_id: PF_STRATEGY_FRAMEWORK_REGISTRY
status: IN_PROGRESS
created_at: 2026-05-27
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01

## Objectif

Connecter `trading_lab_v1` à une source de données XAUUSD M1 réelle ou réaliste, sans live trading, afin de commencer à produire des trades avec coverage multi-dates et coverage complète des 4 variants.

## Contexte

- PR #865 merged: pipeline E2E validé sur `sample_xauusd_m1.csv` (12 lignes synthétiques, 2 dates, données non diversifiées)
- Gap constaté: le sample existant couvre 2 dates, produit uniquement `xau_open_sweep_fvg` sur les 4 variants possibles
- Remaining gap parent: `perf_status=UNMEASURED` — pas d'exits enregistrés, pas de données multi-sessions réalistes

## Règles

- GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
- Ne pas modifier le live trading ni envoyer d'ordre
- Ne pas promouvoir perf_status ni lifecycle automatiquement
- Ne pas committer de secrets ni d'exports broker bruts sensibles
- Ne pas ajouter de stratégie au registry

## Scope

| Fichier | Rôle |
|---|---|
| `docs/chantiers/GO_.../` | Chantier docs |
| `modules/trading_lab_v1/data/sample_xauusd_m1_real_like.csv` | Sample réaliste multi-sessions |
| `docs/index/inbox/GO_...md` | Closeout index |
