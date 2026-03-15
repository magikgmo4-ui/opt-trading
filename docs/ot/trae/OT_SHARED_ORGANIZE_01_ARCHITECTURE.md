# OT-SHARED-ORGANIZE-01 — ARCHITECTURE (ARBO CIBLE /shared)

Date (America/Montreal) : 2026-03-13

## 1. RÉSUMÉ EXÉCUTIF
- `/shared` est la surface canonique inter-machines ; son contenu doit rester simple, lisible, et compatible avec les flux existants.
- La racine `/shared` est aujourd’hui surchargée par des dizaines de fichiers à plat (principalement `.zip` et scripts `.sh`).
- Des dossiers sont **réservés/pipeline** et ne doivent pas être déplacés sans preuve forte : `inbox`, `outbox`, `modules`, `_logs`, `vision_*`, `desk_pro`.
- Cette mission propose une arborescence cible et une stratégie de migration douce **sans déplacer quoi que ce soit**.

## 2. RÔLE CANONIQUE DE /shared
- Surface canonique inter-machines (source `admin-trading:/srv/sftp/shared_files/shared`, clients Linux montés sur `/shared`, Windows via SFTP vers `/shared` en chroot).
- Utilisation : transferts opératoires, artefacts de déploiement, export “latest” du desk, flux vision (inbox/outbox/processed), logs opératoires.

## 3. CONTRAINTES (NON NÉGOCIABLES)
- Ne rien déplacer/renommer automatiquement dans cette mission.
- Ne pas casser les chemins consommés par des services/daemons/wrappers.
- Racine `/shared` : rester légère et stable (surtout pour l’opérateur et pour éviter les confusions).

## 4. DOSSIERS QUI DOIVENT RESTER À LA RACINE (RÉSERVÉS / PIPELINE)
Ces dossiers sont utilisés par des flux runtime et doivent être traités comme **réservés** :
- `inbox/` : entrée transfert (WinSCP/SFTP) et ingestion snapshots (processed interne).
- `outbox/` : sortie transfert (fetch vers Windows/ops).
- `modules/` : dépôt de zips modules (push/pull).
- `_logs/` : logs opératoires liés au flux WinSCP/ops.
- `vision_inbox/`, `vision_outbox/`, `vision_processed/` : flux vision_bot (service) + chaîne vision.
- `desk_pro/` : export canonical `/shared/desk_pro/latest` (consommé sur db-layer/student).

Dossiers stables existants (non prouvés “pipeline”, mais à garder en place tant que non analysés finement) :
- `documents/`
- `windows/`
- `_git_archives/`

## 5. ARBORESCENCE CIBLE PROPOSÉE (SIMPLE + DURABLE)
Objectif : déplacer ultérieurement les fichiers “à plat” vers 3–4 répertoires de classement, sans toucher aux dossiers réservés.

### 5.1 Structure cible
```
/shared
  README.txt
  boot_test.txt

  inbox/                 (réservé pipeline)
  outbox/                (réservé pipeline)
  modules/               (réservé pipeline)
  _logs/                 (réservé pipeline)

  vision_inbox/          (réservé pipeline)
  vision_outbox/         (réservé pipeline)
  vision_processed/      (réservé pipeline)

  desk_pro/              (réservé pipeline)
  documents/             (stable)
  windows/               (stable/à confirmer)
  _git_archives/         (stable/à confirmer)

  _bundles/              (nouveau) zips “packs/bundles” reclassables
  _ops/                  (nouveau) scripts opératoires (.sh) reclassables
  _refs/                 (nouveau) markdown/txt “références” reclassables
  _archives/             (nouveau) anciens/duplicats/volumineux/à isoler
```

### 5.2 Rôle de chaque nouveau dossier cible
- `_bundles/` : stockage unique des livrables `.zip` (packs, bundles, patches) actuellement à plat.
- `_ops/` : scripts de glue/diagnostic/install (actuellement à plat) ; facilite l’usage opératoire.
- `_refs/` : documents “mémo” (`*.md`, `README*`, notes) pour éviter la pollution racine.
- `_archives/` : anciens bundles, doublons `(1)`, et artefacts volumineux/à risque.

## 6. RÉPONSES EXPLICITES AUX QUESTIONS
1. Dossiers impérativement à la racine : `inbox`, `outbox`, `modules`, `_logs`, `vision_*`, `desk_pro`.
2. Nouveaux dossiers à créer : `_bundles`, `_ops`, `_refs`, `_archives`.
3. Types de fichiers qui encombrent : zips (`*_bundle*.zip`, `*_patch*.zip`, packs), scripts `.sh`, quelques `.md/.txt`, artefacts volumineux (`.venv.zip`) et sensibles (`.ssh.zip`).
4. Structure la plus simple/durable : 4 catégories (`_bundles/_ops/_refs/_archives`) + dossiers réservés inchangés.
5. Éléments prêts à reclasser sans risque : la majorité des fichiers `.zip` et `.sh` **à plat** (hors cas sensibles) vers les dossiers cibles.
6. Éléments à ne pas bouger : tous les dossiers réservés listés en §4 + `boot_test.txt`.
7. Stratégie prudente : créer d’abord les dossiers cibles, déplacer par petits lots “évidents”, garder un log de mouvements, et ne déplacer aucun dossier réservé.

