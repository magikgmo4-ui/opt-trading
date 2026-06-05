---
doc_id: OPT_TRADING_WORKFLOW_POST_CHANGE_CONSOLIDATION_03
doc_type: governance_execution_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_WORKFLOW_POST_CHANGE_CONSOLIDATION_03
status: validated
lifecycle_stage: consolidation
topic_keys:
  - workflow_post_change
  - consolidation
  - deprecation
  - modules
surface: module_family
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/status/workflow_post_change_canonique.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02.md
---

# GO_OPT_TRADING_WORKFLOW_POST_CHANGE_CONSOLIDATION_03

## Objet

Consolider proprement la famille `workflow_post_change_v2*` dans `opt-trading`.

---

## Besoin initial

La famille est déjà cadrée côté gouvernance :

- `workflow_post_change_v2` = version canonique
- `fix1` / `fix2` = obsolètes
- `fix3` = mergé dans `v2`

Mais un reliquat réel subsiste dans le trunk :
le module canonique `workflow_post_change_v2` possède encore un `scripts/install_shortcuts.sh` qui installe des raccourcis vers `workflow_post_change_v2_fix3`.

---

## Cible finale

Obtenir une famille cohérente et auto-documentée :

- `workflow_post_change_v2` = seul survivant live
- `workflow_post_change_v2_fix1` = historique obsolète
- `workflow_post_change_v2_fix2` = historique obsolète
- `workflow_post_change_v2_fix3` = historique déprécié, déjà mergé dans `v2`
- `_archive/workflow_post_change_v2_broken_backup` = archive uniquement

---

## État établi retenu

### 1. Canon déjà documenté
Le document `docs/status/workflow_post_change_canonique.md` fixe déjà que :

- `workflow_post_change_v2` est la version canonique active
- `fix1` / `fix2` sont obsolètes
- `fix3` a été mergé dans `v2`

### 2. État réel du code observé
La famille présente :

- `modules/workflow_post_change_v2`
- `modules/workflow_post_change_v2_fix1`
- `modules/workflow_post_change_v2_fix2`
- `modules/workflow_post_change_v2_fix3`
- `_archive/workflow_post_change_v2_broken_backup`

Constat réel :

- `post_change.sh` de `workflow_post_change_v2` et `workflow_post_change_v2_fix3` sont identiques
- `fix1` et `fix2` ne diffèrent que par la variante `ssh -t` / `ssh -tt` autour du `sudo`
- le bug résiduel se situe dans `modules/workflow_post_change_v2/scripts/install_shortcuts.sh`, qui cible encore `workflow_post_change_v2_fix3`

---

## Décision validée

### Survivant live
Le seul module live retenu est :
- `modules/workflow_post_change_v2`

### Statut des autres variantes
- `modules/workflow_post_change_v2_fix1` = `DEPRECATED_OBSOLETE`
- `modules/workflow_post_change_v2_fix2` = `DEPRECATED_OBSOLETE`
- `modules/workflow_post_change_v2_fix3` = `DEPRECATED_MERGED`
- `_archive/workflow_post_change_v2_broken_backup` = `ARCHIVE_ONLY`

### Correctif minimal retenu
Le lot de consolidation 03 retient uniquement :

1. correction de `modules/workflow_post_change_v2/scripts/install_shortcuts.sh`
2. ajout d’un `DEPRECATED.md` dans `workflow_post_change_v2_fix1`
3. ajout d’un `DEPRECATED.md` dans `workflow_post_change_v2_fix2`

### Ce qui n’est pas fait dans ce lot
- suppression physique des dossiers `fix*`
- refactor du script métier `post_change.sh`
- compaction du `registry/modules_registry.yaml`
- nettoyage global des anciens reports historiques

---

## Ce qui est validé

1. `workflow_post_change_v2` reste la seule cible active.
2. `fix3` n’est plus une cible de continuité, même si son dossier reste présent.
3. `fix1` et `fix2` sont des reliques historiques et non des options vivantes.
4. les raccourcis installés par le module canonique doivent pointer vers `workflow_post_change_v2`, pas vers `fix3`.
5. la famille est désormais consolidée côté continuité, même si l’archive physique est conservée.

---

## Verdict

**PASS — consolidation de continuité retenue et correctif minimal appliqué**

## RISKS

- À qualifier.
