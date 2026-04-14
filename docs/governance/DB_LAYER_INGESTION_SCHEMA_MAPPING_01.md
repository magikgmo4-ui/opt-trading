# DB LAYER — INGESTION SCHEMA MAPPING 01

## 1. Objet
- Ce document spécifie le **mapping logique** d’ingestion futur côté `db-layer` : artefacts Desk Pro → entités/tables logiques cibles.
- Il ne remplace pas les runbooks actuels (consultation/diagnostic).
- Il ne prouve pas une implémentation existante : aucune ingestion DB runtime n’est actuellement établie.

## 2. Besoin initial
- Dépasser la simple lecture de `/shared/desk_pro/latest/`.
- Préparer un schéma logique stable et opposable pour une ingestion future.
- Éviter une implémentation ad hoc sans contrat de données explicite.

## 3. Objectif final visé
- Définir un schéma logique cible pour les artefacts Desk Pro **réellement prouvés** comme sources minimales.
- Permettre une ingestion future lisible, idempotente et traçable, sans casser la chaîne actuelle.
- Maintenir la séparation :
  - production Desk Pro (`admin-trading`)
  - distribution inter-machines (`/shared`)
  - ingestion future (`db-layer`)

Plan validé (résumé) :
- Partir de `/shared/desk_pro/latest/`.
- Ne retenir que les artefacts repo-sourcés prouvés.
- Produire : entités logiques + mapping + invariants (sans code, sans choix DB).

## 4. État établi actuel

### 4.1 Fil machine
- `admin-trading` = production / export vers `/shared/desk_pro/latest/`
- `student` = consultation
- `db-layer` = consultation + préparation ingestion future (pas d’ingestion DB prouvée)

### 4.2 Fil repo / produit
- Surface source canonique : `/shared/desk_pro/latest/`.
- Artefacts source minimaux prouvés par les wrappers `db-layer` :
  - `run_summary.json` (requis)
  - `portfolio_engine.json` (optionnel, consommé si présent)
- Wrappers/scripts présents :
  - `scripts/db_layer/desk_pro_db_cmd.sh`
  - `scripts/db_layer/desk_pro_db_latest_shared_info.sh`
- Aucune ingestion DB réelle implémentée (ETABLI).

Gap restant (constat) :
- Le schéma logique et le mapping opposable manquaient ; le moteur DB, le schéma physique et le scheduling restent non figés.

## 5. Artefacts source minimaux
Ne pas inventer : cette liste ne contient que les artefacts explicitement consommés par les scripts `db-layer`.

### 5.1 `run_summary.json` (requis)
- Rôle : identifiant de run + résumé minimal du run.
- Champs minimum observés comme recherchés (grep) :
  - `run_id` ou `run_timestamp` (au moins un des deux pour la clé logique de run)
  - `modules_ok`, `modules_failed` (si présents)
  - `summary` (si présent)

### 5.2 `portfolio_engine.json` (optionnel)
- Rôle : snapshot portefeuille/risque lisible (si présent).
- Champs minimum observés comme recherchés (grep) :
  - `portfolio_state`
  - `exposure_profile`
  - `total_max_risk_pct`
  - `summary` (si présent)

## 6. Entités / tables logiques proposées
Schéma logique cible, sans choix de moteur DB.

### 6.1 Entité `runs`
- Rôle : représenter une exécution Desk Pro (un run) à ingérer.
- Clé logique : `run_key` (dérivée de `run_id` si présent, sinon de `run_timestamp`).
- Champs minimaux :
  - `run_key`
  - `run_id` (nullable)
  - `run_timestamp` (nullable)
  - `source_path` (ex : `/shared/desk_pro/latest/`)
  - `ingest_observed_at_utc` (timestamp d’observation côté ingestion)
- Provenance :
  - `run_id`, `run_timestamp` depuis `run_summary.json`
  - le reste est contextuel ingestion (non source Desk Pro)

### 6.2 Entité `run_module_counts`
- Rôle : stocker un résumé minimal “OK/FAILED” des modules du run.
- Clé logique : (`run_key`)
- Champs minimaux :
  - `run_key`
  - `modules_ok_count` (nullable)
  - `modules_failed_count` (nullable)
- Provenance : `modules_ok`, `modules_failed` depuis `run_summary.json` (si présents).

### 6.3 Entité `portfolio_snapshots`
- Rôle : stocker un état portefeuille/risque associé à un run (si artefact présent).
- Clé logique : (`run_key`)
- Champs minimaux :
  - `run_key`
  - `portfolio_state` (nullable)
  - `exposure_profile` (nullable)
  - `total_max_risk_pct` (nullable)
  - `portfolio_summary` (nullable)
- Provenance : `portfolio_engine.json` (si présent).

## 7. Mapping artefact → schéma logique

| Artefact source | Entité(s) cible(s) | Champs minimaux attendus | Transformation minimale | Notes / limites |
|---|---|---|---|---|
| `run_summary.json` | `runs`, `run_module_counts` | `run_id` ou `run_timestamp` | Construire `run_key` depuis `run_id` sinon `run_timestamp` ; extraire `modules_ok/modules_failed` si présents | Si aucun identifiant n’est présent, ingestion SKIPPED (non opposable) |
| `portfolio_engine.json` | `portfolio_snapshots` | `portfolio_state`, `exposure_profile`, `total_max_risk_pct` | Extraire les champs si présents ; associer au `run_key` issu du run_summary | Optionnel : absence n’est pas bloquante |

## 8. Invariants de reprise et d’ingestion
Sans code : invariants minimaux à respecter par toute implémentation future.

### 8.1 Idempotence minimale
- Un `run_key` déjà ingéré ne doit pas créer de doublon logique.
- Le mapping doit être déterministe : mêmes artefacts → mêmes valeurs (à champs non déterministes près, ex : timestamps d’ingestion).

### 8.2 Clé de run
- `run_key` est obligatoire.
- Priorité :
  1) `run_id` si présent
  2) sinon `run_timestamp`
- Si ni `run_id` ni `run_timestamp` ne sont présents : ingestion **SKIPPED** avec raison explicite.

### 8.3 Artefact manquant / partiel
- Si `/shared` non monté ou `/shared/desk_pro/latest/` absent : ingestion **SKIPPED** (no-op).
- Si `run_summary.json` absent : ingestion **SKIPPED** (contrat source minimal non satisfait).
- Si `portfolio_engine.json` absent : ingestion continue (entité `portfolio_snapshots` non produite).
- Si champ attendu absent dans un artefact présent : valeur NULL + note de traçabilité.

### 8.4 Traçabilité minimale
- Pour chaque tentative : journaliser `run_key` (si déductible), liste d’artefacts vus, et un statut :
  - `SUCCESS` / `SKIPPED` / `FAIL`
- Conserver un pointeur “dernier run ingéré” (mécanisme non figé).

## 9. Choix figés vs non figés

### Figés / ETABLIS
- Source : `/shared/desk_pro/latest/`.
- Artefact requis : `run_summary.json`.
- Artefact optionnel : `portfolio_engine.json`.
- Objectif : ingestion future côté `db-layer` sans patcher le producteur Desk Pro.

### NON FIGÉS
- Moteur DB exact et stockage cible.
- Schéma physique final (DDL, types, index).
- Scheduling et fréquence.
- Rétention et archivage.
- Backfill historique vs latest-only.
- Concurrence et stratégie d’atomicité (snapshot local, locks, etc.).

## 10. Ce que cette spec n’autorise pas encore
- Pas d’implémentation runtime.
- Pas de migration implicite.
- Pas de choix DB forcé.
- Pas de promesse de temps réel.
- Pas de surpromotion de `db-layer`.
- Pas de confusion de périmètre avec `desk_snapshot_ingest` (screenshots inbox → snapshots), hors sujet ici.

## 11. Prochain GO recommandé
> GO_DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01

## 12. Références canoniques minimales
- [DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md)
- [DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md)
- [db_layer_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_runbook.md)
- [db_layer_desk_pro_quick_reference.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_quick_reference.md)
- [desk_pro_multi_machine_map.md](file:///c:/Users/ghost/opt-trading/docs/desk_pro_multi_machine_map.md)
- [admin_trading_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/admin_trading_desk_pro_runbook.md)
- [desk_snapshot_ingest README](file:///c:/Users/ghost/opt-trading/modules/desk_snapshot_ingest/README.md)
