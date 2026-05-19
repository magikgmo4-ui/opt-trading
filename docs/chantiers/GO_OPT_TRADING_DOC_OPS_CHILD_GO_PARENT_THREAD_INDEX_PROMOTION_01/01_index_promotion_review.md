---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01_REVIEW
doc_type: revue
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - parent_thread_map
  - index
  - review
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Revue d'utilite"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 01_index_promotion_review — Revue d'utilite de l'index

## Question

`docs/index/GO_PARENT_THREAD_MAP.md` est-il utile comme index canonique derive ?

## Arguments POUR

1. **Consolidation** : les donnees parent/thread sont actuellement dispersees dans 5 dossiers chantier. Un index leve les consolide en un seul endroit.

2. **Lisibilite** : un index avec une table unique GO -> parent -> fil -> action est plus lisible que 5 matrices separees.

3. **Navigation** : l'index permet de naviguer rapidement d'un GO a son parent et a son fil de continuite.

4. **Derivation claire** : avec `source_kind: derived` et `reference_canonique_principale: docs/index/GO_INDEX.md`, le statut derive est explicite.

5. **Conformite MATRICE** : la MATRICE_DOC_OPS_MASTER_MATRIX_01.md prevoit des surfaces operatoires canoniques sous `docs/index/`. Un index parent/thread y a sa place.

## Arguments CONTRE

1. **Duplication** : l'index duplique des donnees deja presentes dans GO_INDEX.md et les dossiers chantier.

2. **Maintenance** : tout changement de parent/fil devrait etre propage dans GO_INDEX.md ET dans GO_PARENT_THREAD_MAP.md.

3. **Risque de derive** : l'index pourrait devenir une seconde verite de liste si la discipline de maintenance est insuffisante.

## Verdict d'audit

**CREER** — les arguments POUR l'emportent, a condition que :
- le contrat soit clair (source_kind: derived)
- la regle de priorite soit explicite (GO_INDEX.md prime)
- l'index soit leger (table unique, pas de duplication des Entrees GO_INDEX)

L'index est utile comme vue derivee legere. Il ne remplace pas GO_INDEX.md.
