# DB LAYER — SHARED TO DB INGESTION SPEC 01

## Lecture canonique

- lire cette specification apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- utiliser `docs/governance/MATRICE_GOUVERNANTE_V2.md` seulement comme annexe stable secondaire si un recroisement est utile
- ne pas utiliser cette specification a la place des surfaces souveraines de continuite ou de liste

## 1. Objet
- Ce document spécifie l’ingestion future côté `db-layer`, à partir de la surface source Desk Pro partagée via `/shared`.
- Il ne remplace pas les runbooks actuels (consultation/diagnostic).
- Il ne prouve pas une implémentation existante : aucune ingestion DB runtime n’est actuellement établie.

## 2. Besoin initial
- Dépasser la simple consultation de `/shared/desk_pro/latest/` sur `db-layer`.
- Préparer un aval exploitable pour stockage et exploitation ultérieure (sans casser la chaîne actuelle Desk Pro).
- Conserver une séparation propre entre :
  - production Desk Pro (`admin-trading`)
  - distribution inter-machines (`/shared`)
  - ingestion future (`db-layer`)

## 3. Objectif final visé
- Pipeline canonique de type :
  - `/shared/desk_pro/latest/` → `db-layer` → stockage cible
- Ingestion bornée, lisible, reproductible :
  - idempotente (rejouable sans doublons)
  - traçable (logs + reprise)
  - tolérante aux absences partielles d’artefacts
- Consommation des artefacts Desk Pro sans modifier le producteur (pas de patch runtime Desk Pro dans ce lot).

## 4. État établi actuel

### 4.1 Fil machine
- `admin-trading` = production / pilotage / export
  - exécute les runs Desk Pro
  - exporte vers `/shared/desk_pro/latest/`
- `student` = consultation
- `db-layer` = consultation + préparation ingestion future
  - lit `/shared/desk_pro/latest/`
  - wrappers de consultation présents
  - aucun job d’ingestion DB prouvé

### 4.2 Fil repo / produit
- Surface source canonique actuelle : `/shared/desk_pro/latest/`.
- Artefacts source minimaux réellement prouvés (côté consommation `db-layer`) :
  - `run_summary.json` (testé explicitement comme présence attendue)
  - `portfolio_engine.json` (lu si présent, non requis)
- Wrappers / commandes de consultation `db-layer` réellement présents (repo-sourcés) :
  - `scripts/db_layer/desk_pro_db_cmd.sh` (status/summary/sanity/shared-info)
  - `scripts/db_layer/desk_pro_db_latest_shared_info.sh` (lecture /shared + affichage champs)
- Limites actuelles (ETABLI) :
  - pas de pipeline `db-layer` implémenté
  - pas de stockage DB prouvé
  - pas de scheduling/job d’ingestion prouvé

## 5. Contrat source minimal
Ce contrat liste uniquement ce que le repo prouve aujourd’hui comme source minimale.

- **Producteur source** : `admin-trading` (export final vers `/shared/desk_pro/latest/`).
- **Surface source canonique** : `/shared/desk_pro/latest/`.
- **Artefact minimal requis** :
  - `run_summary.json` (le pack `db-layer` le vérifie comme indicateur “Shared Latest: AVAILABLE”).
- **Artefacts candidats (optionnels)** :
  - `portfolio_engine.json` (consommé si présent)
  - autres fichiers présents dans `/shared/desk_pro/latest/` (non contractualisés ici)
- **Point d’entrée machine actuel (`db-layer`)** :
  - `desk-pro-db-shared-info` (wrapper) et/ou `scripts/db_layer/desk_pro_db_latest_shared_info.sh` (script)

## 6. Pipeline cible proposé (sans code)
Pipeline proposé côté `db-layer`, conçu pour être compatible avec l’état actuel (consultation) et ajoutable sans toucher à `admin-trading`.

1. **Lecture de la surface**
   - Lire `/shared/desk_pro/latest/` comme source.
   - Ne pas supposer que `/shared` est toujours monté : détecter et sortir proprement (mode “no-op”).

2. **Validation minimale**
   - Exiger au minimum la présence de `run_summary.json`.
   - Extraire un identifiant de run (ex : `run_id` ou `run_timestamp` si présent) pour :
     - la déduplication
     - l’idempotence
     - la traçabilité

3. **Snapshot local (recommandé)**
   - Copier les artefacts nécessaires dans une zone locale `db-layer` (spool) avant transformation.
   - Objectif : éviter d’ingérer un état “en cours de remplacement” si `/shared/desk_pro/latest/` bouge pendant la lecture.

4. **Transformation (mapping)**
   - Mapper les champs utiles vers un format d’ingestion cible (schéma à définir).
   - Conserver une version brute (raw) des JSON sources ingérés pour audit/rejeu si nécessaire.

5. **Écriture vers stockage cible**
   - Écrire dans le stockage cible (type non figé).
   - Garantir l’idempotence : un run déjà ingéré n’est pas réécrit ou est réécrit de manière déterministe.

6. **Traçabilité / logs / reprise**
   - Produire un log d’ingestion horodaté, avec :
     - identifiant run
     - liste d’artefacts ingérés
     - statut (SUCCESS/FAIL/SKIPPED)
     - raison explicite en cas de SKIPPED/FAIL
   - Conserver un pointeur “dernier run ingéré” (mécanisme non figé : fichier state local, table DB, etc.).

## 7. Choix déjà figés vs non figés

### Figés / ETABLIS
- Source = `/shared/desk_pro/latest/`.
- Producteur = `admin-trading` ; consommateur = `db-layer`.
- `db-layer` dispose aujourd’hui d’une surface de consultation (wrappers/scripts) qui lit `run_summary.json` et peut lire `portfolio_engine.json` si présent.
- Le montage `/shared` est une brique canonique inter-machines (doctrine `shared` + montage SSHFS permanent possible).

### NON FIGÉS
- Type exact de base / stockage cible (PostgreSQL, SQLite, timeseries, fichiers, etc.).
- Schéma final (tables/collections, clés, index, versioning).
- Scheduling (cron/systemd timer/manual) et fréquence d’ingestion.
- Politique de rétention / archivage.
- Stratégie de backfill (historique) vs latest-only.
- Stratégie de cohérence (atomicité de snapshot) et gestion de concurrence.

## 8. Ce que cette spec n’autorise pas encore
- Pas d’implémentation runtime (pas de scripts nouveaux, pas de services, pas de module d’ingestion).
- Pas de migration DB implicite.
- Pas de promesse de temps réel.
- Pas de surpromotion de `db-layer` en produit “déjà fini”.
- Pas de confusion de périmètre avec `desk_snapshot_ingest` (pipeline screenshots inbox → snapshots), qui n’est pas l’ingestion Desk Pro depuis `/shared/desk_pro/latest/`.

## 9. Prochain GO recommandé
> GO_DB_LAYER_INGESTION_SCHEMA_MAPPING_SPEC_01

## 10. Références canoniques minimales
- [DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md)
- [db_layer_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_runbook.md)
- [db_layer_desk_pro_quick_reference.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_quick_reference.md)
- [desk_pro_multi_machine_map.md](file:///c:/Users/ghost/opt-trading/docs/desk_pro_multi_machine_map.md)
- [admin_trading_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/admin_trading_desk_pro_runbook.md)
- [shared README](file:///c:/Users/ghost/opt-trading/modules/shared/README.md)
- [shared_sshfs_permanent README](file:///c:/Users/ghost/opt-trading/modules/shared_sshfs_permanent/README.md)

## RISKS

- À qualifier.
