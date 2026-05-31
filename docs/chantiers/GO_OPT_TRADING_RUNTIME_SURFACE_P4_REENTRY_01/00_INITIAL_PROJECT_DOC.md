---
go_id: GO_OPT_TRADING_RUNTIME_SURFACE_P4_REENTRY_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-31
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Reprendre les chantiers produit/runtime apres cloture complete du modele registry P3, sans rouvrir la registry elle-meme.

## 3_INITIAL_NEED
Le modele registry est stabilise et le residuel `mimo_open_observer` est ferme. Le repo a maintenant besoin d'un point de reentree produit/runtime qui identifie la prochaine ligne utile a faire avancer, plutot que de poursuivre des optimisations de gouvernance deja suffisantes.

## 6_FINAL_TARGET
Un cadrage doc-only qui choisit le prochain axe produit/runtime prioritaire et fixe le point de reprise utile pour P4.

## 12_INVARIANTS
- doc-only
- no registry mutation
- no runtime mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Relire les flux actifs et les closeouts registry P3
- [x] Comparer les candidats runtime/produit immediats
- [ ] Verifier le scope doc-only

## 17_RESUME_POINT
Le role de ce GO est de sortir de la logique registry closeout pour reattacher l'effort aux flux produit actifs les plus proches d'une vraie utilite runtime.
