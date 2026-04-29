---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - doc_ops
  - open_work_control
  - continuity
  - go_index
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-25
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01 — cadrage

## 1_MASTER_TARGET

Figer la liste réelle des chantiers ouverts ou non terminés dans `opt-trading`, sans suppression de branche et sans arbitrage de cleanup, avant toute reprise d’un flux principal ou ouverture de nouveaux parents spécialisés.

## 2_INITIAL_PROJECT_DOC

Documents de référence obligatoires :

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md`
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`

## 3_INITIAL_NEED

Après la fermeture et le merge de `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`, reprendre l’étape 2 du parent `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` : contrôler les ouverts et les non terminés.

Le besoin n’est pas de supprimer, fusionner ou relancer un chantier. Le besoin est de produire une photo fiable de ce qui reste réellement actif, ouvert, bloqué, référence, ou à déprioriser.

## 4_MASTER_PROJECT_PLAN

Séquence parent retenue :

1. Hygiène Git / branches / supports ouverts — fermé par `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`.
2. Contrôle des ouverts / non terminés — présent GO.
3. Reprise d’un flux principal.
4. Carte cible future des parents projet / machine.
5. Ouverture canonique future des parents spécialisés.
6. Audit final de conformité.

## 5_GO_PLAN

Sous-GO actif :

- `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`

But :

- relire `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md` ;
- figer les ouverts et non terminés réels ;
- distinguer `ACTIVE`, `OPEN`, `REFERENCE`, `BLOCKED`, `STALE`, `TO_CLOSE_CANDIDATE` ;
- identifier ce qui est réellement exécutable, seulement documentaire, en attente, ou à déprioriser ;
- préparer le passage vers `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01`.

## 6_FINAL_TARGET

Livrables attendus :

1. `01_open_work_inventory.md` — inventaire des chantiers ouverts/non terminés.
2. `02_decisions.md` — décisions de classement sans fermeture physique non validée.
3. `90_closeout.md` — closeout du sous-GO, si l’inventaire est complet.

## 7_CANONICAL_STATE

### ETABLI

- PR `#164` mergée dans `sot/mainline`.
- `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` est fermé et intégré.
- Aucun `DROP` n’a été validé dans le cleanup.
- Les 33 branches `A_VERIFIER_DEEPER` restent hors décision de suppression.
- Le parent `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` reste ouvert.
- `GO_INDEX.md` reste la vérité de liste locale des chantiers non clos.
- `BRANCH_STATE.md` ne gouverne que la surface branches.

### BRANCHE DÉDIÉE

- Branche : `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
- Base d’ouverture : merge commit PR #164 `0bd1bcbe581ff15b916a7681b6e1d7631a54d1df`
- Support Git : branche dédiée, justifiée par la revue documentaire multi-index.

## 8_VALIDATED_PLAN

1. Lire les surfaces canoniques.
2. Extraire les entrées non closes de `GO_INDEX.md`.
3. Croiser avec `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md`.
4. Produire une table de contrôle.
5. Classer chaque entrée sans fermeture automatique.
6. Identifier les écarts et contradictions.
7. Préparer les corrections ou arbitrages dans une passe séparée.
8. Fermer le sous-GO si la photo est complète.

## 9_SELECTED_SOLUTION

Solution retenue : audit documentaire borné, repo-first, sans mutation opérationnelle.

## 10_SELECTED_SETUP

- Base : `sot/mainline`
- Branche : `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
- Dossier : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/`
- Périmètre autorisé : documentation du sous-GO et inventaire des surfaces de continuité.

## 11_KEY_DECISIONS

- Ne pas rouvrir le cleanup branches.
- Ne pas arbitrer les 33 branches `A_VERIFIER_DEEPER` dans ce GO.
- Ne pas supprimer de branche.
- Ne pas modifier les modules runtime.
- Ne pas intégrer les chantiers locaux non suivis hors périmètre.
- Traiter d’abord l’état documentaire des ouverts/non terminés.

## 12_INVARIANTS

- `sot/mainline` reste la base canonique.
- `GO_INDEX.md` est la vérité de liste locale.
- `REPRISE.md` est un support de pilotage, pas une seconde vérité de liste.
- `BRANCH_STATE.md` ne gouverne que les branches.
- Aucun chantier n’est fermé sans closeout explicite.
- Aucun `ACTIVE` ou `OPEN` n’est déclassé sans preuve.

## 13_ESTABLISHED

- Le sous-GO précédent est intégré.
- Le présent sous-GO correspond à l’étape 2 du plan parent.
- Le repo contient encore des chantiers ouverts et actifs à qualifier.

## 14_HYPOTHESIS

- Certains chantiers `ACTIVE` pourraient être obsolètes ou seulement référentiels.
- Certains `OPEN` pourraient nécessiter closeout ou reclassification.
- Certains points de `REPRISE.md` pourraient être en retard sur `GO_INDEX.md`.

## 15_REMAINING_GAP

- Inventaire exhaustif des ouverts/non terminés non encore produit.
- Croisement avec surfaces actives non encore fait.
- Décision sur le prochain flux principal non encore prise.

## 16_TODO

- Produire `01_open_work_inventory.md`.
- Croiser les statuts `GO_INDEX` avec `ACTIVE_STREAMS`, `NEXT_GO_CANDIDATES`, `REPRISE`.
- Produire `02_decisions.md`.
- Préparer un closeout si l’audit est complet.

## 17_RESUME_POINT

Reprise opérationnelle :

```powershell
cd C:\Users\ghost\opt-trading
git fetch origin --prune
git checkout go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01
git status --short --branch
```

Puis lire :

- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`

## 18_TO_DOCUMENT

TAGS :

- `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
- `OPEN_WORK_CONTROL`
- `GO_INDEX`
- `ACTIVE_STREAMS`
- `NEXT_GO_CANDIDATES`
- `REPRISE`

## 19_TO_REMEMBER

Memory Bricks projet :

- `OPEN_WORK_CONTROL_STARTS_AFTER_BRANCH_CLEANUP_MERGED`
- `DO_NOT_ARBITRATE_BRANCH_DROPS_IN_OPEN_WORK_CONTROL`
- `GO_INDEX_IS_SOURCE_OF_TRUTH_FOR_OPEN_WORK_CONTROL`
