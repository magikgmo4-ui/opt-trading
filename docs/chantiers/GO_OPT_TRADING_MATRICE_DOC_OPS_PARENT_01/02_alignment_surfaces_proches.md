---
doc_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_02
doc_type: chantier_alignment
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
status: reference
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - matrice_doc_ops
  - alignment
  - nearby_surfaces
  - doc_only
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 7 - Point de reprise"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md
  - docs/next/NEXT_GO_CANDIDATES.md
  - docs/product_targets/GO_PRODUCT_TARGET_CANONIZATION_01_DECISION.md
  - docs/product_targets/RUNTIME_TO_TARGET_MAPPING.md
  - docs/ot/project_cards/PROJECT_CARD_DESKPRO_01.md
  - docs/status/desk_pro_stack_canonique.md
  - docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/index/BRANCH_STATE.md
---

# ALIGNMENT_SURFACES_PROCHES_02

## 1. Objet

Executer le lot doc-only borne d'alignement des surfaces proches a partir de `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.

Ce lot ne :
- re-redige pas la matrice maitre
- n'ouvre pas de parent concurrent
- ne lance pas de suppression physique sensible
- ne traite pas des surfaces hors perimetre

Support Git du present passage :
- branche parent de reference : `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`
- branche de lot doc-only isolee : `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_01`

Il qualifie et recadre le role des surfaces proches pour qu'aucune ne reste lue comme seconde reference souveraine transverse.

---

## 2. Tableau de qualification

| Surface | Role actuel | Role cible | Decision doc-only retenue |
| --- | --- | --- | --- |
| `docs/next/NEXT_GO_CANDIDATES.md` | stub de redirection deja declassé | compat / redirection seulement | conserver, clarifier le statut compat et le renvoi vers la matrice maitre + `docs/index/NEXT_GO_CANDIDATES.md` |
| `docs/product_targets/GO_PRODUCT_TARGET_CANONIZATION_01_DECISION.md` | note de decision partielle `A_REVALIDER` | derive de revalidation produit | conserver, marquer comme non souverain et derive |
| `docs/product_targets/RUNTIME_TO_TARGET_MAPPING.md` | mapping partiel runtime -> cible | derive de mapping produit | conserver, marquer comme derive et non souverain |
| `docs/ot/project_cards/*` | fiches compactes de reprise produit / famille | surfaces operatoires de reprise bornees | conserver, recadrer comme operatoires et non souveraines |
| `docs/status/*` | fiches courtes de lignee / famille | derives de qualification famille | conserver, recadrer comme derives de famille |
| `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md` | vue globale ponctuelle | snapshot / archive de lecture | conserver, marquer comme snapshot non gouvernant |
| `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md` | continuite produit haute, sans frontmatter | annexe canonique stable sous la matrice maitre | conserver, ajouter noyau frontmatter et borne d'autorite |
| `docs/index/BRANCH_STATE.md` | photo operatoire des branches | surface operatoire branches seulement | conserver, recadrer explicitement sous la matrice maitre ; pas de reclassification exhaustive dans ce lot |

---

## 3. Doublons souverains reels

Doublon souverain transverse reel : aucun second document ne concurrence `MATRICE_DOC_OPS_MASTER_MATRIX_01.md` comme matrice maitre transversale.

Doublons ou recouvrements a clarifier :
- doublon de nom : `docs/next/NEXT_GO_CANDIDATES.md` versus `docs/index/NEXT_GO_CANDIDATES.md`
- recouvrement partiel sur la continuite produit : `PRODUCT_CONTINUITY_HIERARCHY_01.md`, `project_cards/*`, `status/*`, `product_targets/*`
- recouvrement partiel sur la vue globale : `PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`
- recouvrement partiel sur la lecture Git : `BRANCH_STATE.md`

Regle retenue :
- la matrice maitre reste seule souveraine
- les surfaces proches gardent un role borne, explicite et compatible

---

## 4. Categories cibles retenues

### Annexes stables

- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`

### Surfaces operatoires

- `docs/ot/project_cards/*`
- `docs/index/BRANCH_STATE.md`

### Surfaces derivees

- `docs/product_targets/GO_PRODUCT_TARGET_CANONIZATION_01_DECISION.md`
- `docs/product_targets/RUNTIME_TO_TARGET_MAPPING.md`
- `docs/status/*`

### Surfaces snapshot / compat

- `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`
- `docs/next/NEXT_GO_CANDIDATES.md`

---

## 5. Plan de patch doc-only borne

Le patch borne de ce lot est :
1. ajouter un marquage de role explicite sur chaque surface du perimetre
2. ajouter un noyau frontmatter minimal quand il manque et que le document reste vivant
3. ajouter le renvoi vers `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
4. ne pas supprimer physiquement les surfaces sensibles
5. ne pas deplacer physiquement les fichiers dans ce lot

Ce lot ne fait pas :
- de fusion physique
- de reclassement hors perimetre
- de campagne naming
- de refresh exhaustif du parc branches

---

## 6. Effet attendu

Apres ce lot :
- la matrice maitre reste l'unique reference souveraine transverse
- les surfaces proches ont un role clarifie
- aucun doublon souverain n'est laisse ambigu
- la reprise reste compatible

---

## 7. Point de reprise

Si un lot suivant reste necessaire, il devra rester :
- doc-only
- borne
- centre sur les surfaces explicitement recadrees ici

Le prochain geste naturel devient, seulement si un ecart subsiste :
- un lot de patch doc-only borne d'alignement complementaire
