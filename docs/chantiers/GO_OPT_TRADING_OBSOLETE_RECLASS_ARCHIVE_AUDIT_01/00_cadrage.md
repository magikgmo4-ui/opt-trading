---
doc_id: GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: repo_hygiene
go_id: GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - obsolete
  - declass
  - archive
  - legacy
  - reclass
  - repo_hygiene
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md
---

# 00_cadrage — GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01

## Classification
**audit — repo-first — doc-only — qualification obsolete / déclassé / archive / legacy / sous arbitrage**

## Besoin initial
Évaluer la différence entre :
- la vue canonique (continuité, politiques, chantiers) déjà clarifiée
- la pollution physique réelle du repo (objets dispersés, legacy, archives, stubs, reliquats, arbitrages)

## Cible finale
Produire un état canonique exploitable pour décider ensuite, lot par lot :
- quoi garder
- quoi déplacer
- quoi archiver
- quoi supprimer (après validation)
- quoi laisser en legacy toléré
- quoi laisser sous arbitrage

## Surfaces prioritaires (PHASE B)
GROUPE 1 — objets racine sous arbitrage (selon `REPO_ROOT_POLICY.md`) :
- `Readme`
- `TOOLBOX.txt`
- `UI_URLS.md`
- `smartmoney.txt`
- `bitget_bridge.py`
- `_archive/`
- `.gitignore.bak*`
- surfaces journal retirees du repo canonique (lot execute)

GROUPE 2 — reliquats `workflow_post_change` :
- `modules/workflow_post_change_v2_fix1`
- `modules/workflow_post_change_v2_fix2`
- `modules/workflow_post_change_v2_fix3`
- `modules/workflow_post_change_v2`
- `_archive/workflow_post_change_v2_broken_backup`

Application close/poussée — `GO_OPT_TRADING_WORKFLOW_LEGACY_RECLASS_01` :
- reclassement validé vers `_archive/legacy_modules/` pour les variantes legacy et le backup cassé
- retrait de l’entrée `workflow_post_change_v2_fix3` du registre des modules
- conservation stricte de `modules/workflow_post_change_v2` hors périmètre
- SHA canonique : `f0aceb1` ; HEAD publié courant : `1d54322`

GROUPE 3 — docs historiques dispersées :
- `docs/CLOSEOUT_FINAL_BOT_VISION.txt`
- `docs/ETABLI_BOT_VISION.txt`
- `docs/RESIDUEL_BOT_VISION.txt`

GROUPE 4 — surfaces support non canoniques à surveiller :
- `docs/ot/trae/trae_pack_texts/trae_pack/*`
- autres groupes réellement observés comme dispersés / legacy / déclassés / ambigus (repo-first uniquement)

## Méthode imposée
1. repo-first : l’état réel du repo prime sur la mémoire et les hypothèses
2. audit/qualification uniquement : aucune action destructive (move/delete) dans ce parent sans validation explicite
3. ne pas rouvrir les lots déjà clos PASS
4. ne pas recréer de doctrine parallèle : référencer les politiques/decisions existantes
5. produire une matrice opposable (catégorie, justification, risque, action, dépendances, validation)

## Limites
- pas de suppression massive
- pas de déplacement global
- pas de refactor transverse

## Sortie attendue (PHASE C/D)
- matrice canonique exploitable
- plan de lots physiques futurs (sans exécution)
- point de reprise stable

## Bundle de cadrage (hors repo)
Bundle source (cadrage) :
- `C:\Users\ghost\Downloads\OPT_TRADING_OBSOLETE_RECLASS_AUDIT_BUNDLE.zip`

## REPRISE
Point de reprise unique :
- `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md`
