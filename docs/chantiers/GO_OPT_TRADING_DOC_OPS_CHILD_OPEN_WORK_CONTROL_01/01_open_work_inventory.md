---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_OPEN_INVENTORY
doc_type: inventory
repo: opt-trading
project: opt-trading
module:
  go_id: GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01
status: open
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - doc_ops
  - open_work_control
  - continuity
  - go_index
surface: inventory
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-25
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/BRANCH_STATE.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01 — open work inventory

## ETABLI

- Branche: `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
- Base: `sot/mainline` après merge PR #164
- Périmètre: docs-only
- Fichiers lus:
  - `docs/index/GO_INDEX.md`
  - `docs/index/ACTIVE_STREAMS.md`
  - `docs/index/NEXT_GO_CANDIDATES.md`
  - `docs/index/REPRISE.md`
  - `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/00_cadrage.md`
  - `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/BRANCH_STATE.md`
- Nombre de GO non clos retenus par les index: `14`
- Aucun arbitrage de branche effectué.
- Aucune suppression effectuée.
- `BRANCH_STATE.md` global non modifié.

## 7_CANONICAL_STATE

Après PR #164, le cleanup branches est fermé et intégré. Le présent GO correspond à l’étape 2 du parent `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`: contrôler les chantiers ouverts ou non terminés avant toute reprise principale, arbitrage de branche ou suppression contrôlée.

Les surfaces `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md` et `REPRISE.md` convergent sur un périmètre opératoire de 14 GO non clos retenus. Les entrées `REFERENCE` restent hors exécution courante.

## TABLEAU INVENTAIRE

| GO_ID | SOURCE | STATUS_SOURCE | BRANCH_LINK | WORK_STATUS | DECISION_PROVISOIRE | JUSTIFICATION | NEXT_ACTION |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | OPEN / P0 | go/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | ACTIVE_REAL | KEEP_ACTIVE | Parent canonique de reprise repo-first; ordre branches/supports ouverts puis ouverts/non terminés confirmé. | Continuer ce GO enfant OPEN_WORK_CONTROL avant toute ouverture de parents spécialisés. |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P0 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Chantier parent actif pour réaligner docs/index et continuité; gap encore établi. | Exécuter LOT 1 index puis LOT 2 selon cadrage dédié. |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P0 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Bundle et cadrage ouverts; prochaine implémentation base encore à valider sur machine réelle. | Reprendre GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01 après choix du flux principal. |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P0 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Audit non destructif des familles obsolete / archive / legacy; matrice et plan de lots restent à produire. | Produire matrice canonique PHASE C puis plan PHASE D sans exécution physique. |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P1 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Carte des surfaces publiée; ajustements encore à consolider sans duplication registry. | Consolider les points d’ancrage structurels en gap-only. |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P1 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Politique racine posée; arbitrages de reclassement racine encore ouverts. | Consolider les classes racine sans redéfinir la frontière repo/hors-repo. |
| GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P1 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Pack legacy déplacé sous docs/ot/trae; statut helper/archive à figer. | Vérifier si closeout doc-only possible sans re-promouvoir les anciens templates. |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P1 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Fiches status familles publiées; arbitrages survivant/transition/legacy restent ouverts. | Consolider familles mixtes en gap-only. |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P1 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Scope et exceptions registry clarifiés; couverture déclarative à poursuivre. | Poursuivre via registry/README.md comme source canonique unique. |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | ACTIVE / P1 | sot/mainline | OPEN_DOC_ONLY | REVIEW_NEXT | Dossier minimal ouvert pour un GO actif; suite autonome encore insuffisamment explicitée. | Formaliser la suite opératoire dédiée avant tout lot d’exécution. |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | OPEN / P1 | non précisée | ACTIVE_REAL | KEEP_ACTIVE | Survivant canonique reseau_ssh_step2 confirmé; preuve détaillée et classification complète de la famille restent incomplètes. | Exécuter l’audit détaillé reseau_ssh dans ce GO, hors présent inventaire. |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | OPEN / P2 | origin/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | STALE_TO_REVIEW | REVIEW_NEXT | Parent intégré doc-only mais dossier parent complet non matérialisé dans cette copie locale. | Garder comme point de reprise; rouvrir un enfant seulement sur preuve documentaire. |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | OPEN / P2 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Doctrine légère de dérivation ouverte sous matrice maître; pilote borné non terminé. | Poursuivre pilote documentaire sans rouvrir la matrice maître. |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_INDEX / ACTIVE_STREAMS / REPRISE / NEXT_GO_CANDIDATES | OPEN / P2 | sot/mainline | ACTIVE_REAL | KEEP_ACTIVE | Parent naming ouvert audit-only; inventaire et normalizer enfants restent à produire/qualifier. | Reprendre GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01 avant toute application. |

## HYPOTHESIS

- Certains GO `ACTIVE` pourraient être proches du closeout, mais aucun closeout n’est validé dans cette passe.
- `GO_GIT_PROGRESSIVE_MIGRATION_START_13` est retenu en `OPEN_DOC_ONLY` / `REVIEW_NEXT` car sa suite autonome reste à expliciter.
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` reste `STALE_TO_REVIEW` car le dossier parent complet n’est pas matérialisé localement selon les index.
- Les 33 `A_VERIFIER_DEEPER` du cleanup branches restent hors décision dans ce GO.

## TODO

- Relire les GO `REVIEW_NEXT` avant toute décision de closeout.
- Préparer `02_decisions.md` avec décisions de classement documentaire.
- Ne modifier `BRANCH_STATE.md` qu’après décision séparée et justifiée.
- Ne créer `90_closeout.md` qu’après validation de `01_open_work_inventory.md` et `02_decisions.md`.

## 17_RESUME_POINT

```powershell
cd C:\Users\ghost\opt-trading-open-work-control
git fetch origin --prune
git checkout go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01
git status --short --branch
git rev-list --left-right --count origin/go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01...HEAD
```

Prochaine action:

```text
Produire docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/02_decisions.md
```

## 18_TO_DOCUMENT

TAGS:

- GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01
- OPEN_WORK_CONTROL
- GO_INDEX
- ACTIVE_STREAMS
- NEXT_GO_CANDIDATES
- REPRISE

Blocs à extraire:

- 7_CANONICAL_STATE
- TABLEAU INVENTAIRE
- HYPOTHESIS
- TODO
- 17_RESUME_POINT

## 19_TO_REMEMBER

Memory Bricks projet:

- OPEN_WORK_CONTROL_INVENTORY_CREATED_AFTER_BRANCH_CLEANUP_MERGE
- OPEN_WORK_CONTROL_DOES_NOT_ARBITRATE_BRANCH_DELETIONS
- OPEN_WORK_CONTROL_NEXT_STEP_IS_02_DECISIONS_BEFORE_CLOSEOUT
