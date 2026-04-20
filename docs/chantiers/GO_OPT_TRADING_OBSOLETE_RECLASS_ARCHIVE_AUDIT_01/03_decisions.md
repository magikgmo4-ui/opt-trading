---
doc_id: GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: repo_hygiene
go_id: GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01
status: active
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - obsolete
  - declass
  - archive
  - legacy
  - reclass
surface: chantier
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/NEXT_GO_CANDIDATES.md
---

# 03_decisions — GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01

## D1 — Nature du chantier (audit uniquement)
Ce parent est un chantier :
- d’audit
- de qualification
- de matrice décisionnelle
- de préparation au reclassement physique futur

Il n’est pas un chantier :
- de suppression massive
- de déplacement global
- de refactor transverse

## D2 — Règle repo-first
- l’état réel du repo prime sur la mémoire et les hypothèses
- la vue canonique est un cadre de lecture ; elle ne prouve pas à elle seule l’état physique

## D3 — Règle closeout PASS
- un closeout PASS retire un GO des flux actifs
- un closeout PASS ne justifie pas à lui seul une suppression ou un déplacement physique

## D4 — Catégories autorisées (matrice)
- actif
- référence
- déclassé
- legacy toléré
- archive existante
- sous arbitrage

## D5 — Actions autorisées (matrice)
- garder
- laisser en place
- déplacer
- archiver
- supprimer après validation
- surveiller

## D6 — Anti-destruction (phase audit)
- aucune suppression, aucun move, aucun archivage physique sans :
  - matrice validée
  - lot explicitement validé
  - risque documenté
  - rollback prévu si nécessaire

## D7 — Exclusions
- ne pas rouvrir les lots déjà clos PASS
- ne pas confondre “hors actif” avec “supprimable”
- ne pas créer de doctrine parallèle : référencer `REPO_ROOT_POLICY`, `REPO_SURFACES_MAP`, `JOURNAL_HIERARCHY`, `docs/index/*`

## D8 — Preuve repo-first des callers/usages (PHASE B)
Pour tout item à risque :
- prouver repo-first les callers/usages avant toute validation de move/delete/archive
- distinguer strictement :
  - appelé réellement (caller outillage / runtime / wrapper / script)
  - mention documentaire seulement
  - aucun caller trouvé
  - ambigu / à confirmer (usage opérateur hors repo, ou preuve insuffisante)

Règle de prudence :
- si absence de preuve repo-first, classer “ambigu / à confirmer” ou “à surveiller”, jamais “supprimable”
- une déclaration dans un registre (`registry/*.yaml`) est une preuve de consommation par outillage, pas une preuve d’exécution runtime

## D9 — LOT_DOCS_HISTORIQUES_BOT_VISION (premier lot applicable)
Périmètre strict :
- `docs/CLOSEOUT_FINAL_BOT_VISION.txt`
- `docs/ETABLI_BOT_VISION.txt`
- `docs/RESIDUEL_BOT_VISION.txt`

Nature :
- lot documentaire uniquement (doc-only)
- aucun changement runtime

Cible d’archivage canonique proposée :
- `docs/ot/closings/bot_vision/`

Exclusions :
- ne pas traiter `workflow_post_change_v2` (hors lot)
- ne pas traiter `bitget_bridge.py` (hors lot)
- ne pas traiter `journal_add.sh` (hors lot)
- ne pas déplacer d’autres fichiers hors périmètre

Risque :
- risque principal = liens/refs cassés (continuité documentaire), pas le runtime

Rollback :
- rollback standard par revert du commit du lot
- rollback local : annuler `git mv` avant commit si besoin

Critères PASS / FAIL
- PASS si : diff borné (3 moves + mises à jour de liens) et aucune référence restante vers les anciens chemins
- FAIL si : déplacement hors périmètre, ou références cassées non corrigées

## D10 — Exécution validée du lot D9
- Exécution autorisée et appliquée en périmètre strict D9.
- Les 3 `git mv` ont été exécutés uniquement vers `docs/ot/closings/bot_vision/`.
- Les références minimales ont été mises à jour uniquement dans les 3 fichiers prévus.
- Vérifications exigées confirmées :
  - diff borné au lot documentaire
  - absence de références résiduelles vers les anciens chemins ciblés
- Contrainte de non-élargissement respectée :
  - aucun changement `workflow_post_change_v2`
  - aucun changement `bitget_bridge.py`
  - aucun changement `journal_add.sh`

## D11 — GO_OPT_TRADING_WORKFLOW_LEGACY_RECLASS_01 (reclassement archive minimal)
Périmètre strict :
- `modules/workflow_post_change_v2_fix1`
- `modules/workflow_post_change_v2_fix2`
- `modules/workflow_post_change_v2_fix3`
- `_archive/workflow_post_change_v2_broken_backup`

Décision :
- reclassement vers `_archive/legacy_modules/` (pas de suppression)
- suppression de l’entrée `module_name: workflow_post_change_v2_fix3` dans `registry/modules_registry.yaml`
- ne pas ajouter d’entrée “archive” dans ce registre

Exclusions :
- ne pas toucher `modules/workflow_post_change_v2`
- ne pas faire de sweep global des docs (mise à jour bornée au parent)

## REPRISE
Point de reprise unique :
- `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md`
