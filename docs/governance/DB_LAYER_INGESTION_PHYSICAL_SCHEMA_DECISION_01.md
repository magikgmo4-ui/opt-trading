# DB LAYER — INGESTION PHYSICAL SCHEMA DECISION 01

## 1. Objet
- Ce document décide le schéma physique minimal futur de l’ingestion côté `db-layer`.
- Il ne remplace ni la spec pipeline ni le mapping logique.
- Il ne prouve pas une implémentation existante : aucune ingestion DB runtime n’est actuellement établie.

## 2. Besoin initial
- Dépasser la seule logique abstraite (entités/mapping) en préparant une implémentation future sans ambiguïté.
- Éviter une dérive ad hoc au moment du codage (tables, clés, contraintes, indexes, traçabilité).
- Rester compatible avec l’état établi : production Desk Pro inchangée, lecture depuis `/shared/desk_pro/latest/`.

## 3. Objectif final visé
- Disposer d’une base de décision physique minimale opposable :
  - tables/collections physiques minimales
  - clés minimales (unicité, idempotence)
  - contraintes minimales (NOT NULL / UNIQUE)
  - index minimaux (requêtes usuelles)
  - traçabilité minimale (statut/erreurs)
- Sans figer plus que ce que le repo permet (moteur DB, scheduling, rétention).

## 4. État établi actuel

### 4.1 Fil machine
- `admin-trading` = production / export vers `/shared/desk_pro/latest/`
- `student` = consultation
- `db-layer` = consultation + préparation ingestion future (pas d’ingestion DB prouvée)

### 4.2 Fil repo / produit
- Spec pipeline posée : [DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md)
- Mapping logique posée : [DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md)
- Artefacts source minimaux prouvés (côté consommation `db-layer`) :
  - `run_summary.json` (requis)
  - `portfolio_engine.json` (optionnel)
- Aucune implémentation physique (DB + DDL + job) n’est présente/prouvée.

## 5. Options de décision physique

### Option A — Moteur DB figé maintenant
- Permet : DDL strict, types/indices optimisés, implémentation immédiate bornée.
- Fige trop tôt : moteur, tooling, procédures d’exploitation, migration/backup.
- Statut : non retenue (aucune preuve repo-sourcée imposant un moteur DB final).

### Option B — Moteur non figé, schéma physique minimal V1 figé (générique)
- Permet : préparer l’implémentation sans ambiguïté sur tables/contraintes/index, tout en laissant le moteur libre.
- Fige trop tôt : moins de détails DDL (types exacts, index avancés) ; nécessite une passe ultérieure “DDL concret” au moment de choisir le moteur.
- Statut : retenue (compatible avec l’état établi + respecte “ne pas figer un moteur DB”).

### Option C — Aucune décision physique (A_REVALIDER)
- Permet : rester au niveau logique uniquement.
- Coût : risque de dérive ad hoc au moment de coder.
- Statut : non retenue (le mapping logique est suffisamment précis pour figer un socle physique minimal).

## 6. Décision retenue
DECISION : moteur non figé, schéma physique minimal V1 figé.

- **Moteur** : NON FIGÉ.
- **Niveau opposable** : tables minimales + clés + contraintes minimales + index minimaux + invariants de traçabilité.
- **Non opposable ici** : DDL exact, types DB exacts, tuning, migrations, scheduling, rétention.

## 7. Schéma physique minimal retenu
Le schéma ci-dessous doit pouvoir être matérialisé dans n’importe quel moteur (SQL ou non) sans changer le contrat logique.

### 7.1 Table / collection physique `runs`
- Rôle : registre physique des runs ingérés (ou tentés), clé d’idempotence.
- Clé primaire : `run_key` (string).
- Colonnes/champs minimaux :
  - `run_key` (PK, NOT NULL)
  - `run_id` (string, NULLABLE)
  - `run_timestamp` (string ou timestamp, NULLABLE)
  - `source_path` (string, NOT NULL) — valeur attendue : `/shared/desk_pro/latest/`
  - `ingest_observed_at_utc` (timestamp, NOT NULL)
  - `ingest_status` (string, NOT NULL) — `SUCCESS` / `SKIPPED` / `FAIL`
  - `ingest_reason` (string, NULLABLE) — raison explicite si `SKIPPED`/`FAIL`
- Contraintes minimales :
  - UNIQUE(`run_key`)
  - CHECK : `run_key` non vide
- Index minimaux :
  - index sur `ingest_observed_at_utc`
  - index sur `run_timestamp` (si disponible)

### 7.2 Table / collection physique `run_module_counts`
- Rôle : résumé physique minimal de santé modules par run.
- Clé primaire : `run_key` (ou PK technique + UNIQUE(`run_key`)).
- Colonnes/champs minimaux :
  - `run_key` (FK logique vers `runs.run_key`, NOT NULL)
  - `modules_ok_count` (int, NULLABLE)
  - `modules_failed_count` (int, NULLABLE)
- Contraintes minimales :
  - UNIQUE(`run_key`)
- Index minimaux :
  - index sur `run_key`

### 7.3 Table / collection physique `portfolio_snapshots`
- Rôle : snapshot physique minimal portefeuille/risque associé à un run (si artefact présent).
- Clé primaire : `run_key` (ou PK technique + UNIQUE(`run_key`)).
- Colonnes/champs minimaux :
  - `run_key` (FK logique vers `runs.run_key`, NOT NULL)
  - `portfolio_state` (string/json, NULLABLE)
  - `exposure_profile` (string/json, NULLABLE)
  - `total_max_risk_pct` (float, NULLABLE)
  - `portfolio_summary` (string, NULLABLE)
- Contraintes minimales :
  - UNIQUE(`run_key`)
- Index minimaux :
  - index sur `run_key`

## 8. Invariants physiques minimaux

### 8.1 Unicité / idempotence
- `run_key` est l’unique clé d’idempotence.
- Toute écriture doit respecter : un `run_key` déjà présent ne crée pas de doublon.
- Les tables `run_module_counts` et `portfolio_snapshots` sont au maximum 1 ligne par `run_key`.

### 8.2 Ordre d’écriture minimal
- Créer/mettre à jour `runs` en premier (statut/raison inclus), puis remplir les tables associées si les artefacts/valeurs existent.

### 8.3 Artefacts obligatoires / optionnels
- Si `run_summary.json` absent : enregistrer un `runs` en `SKIPPED` avec `ingest_reason` explicite, sans écrire `run_module_counts` ni `portfolio_snapshots`.
- Si `portfolio_engine.json` absent : `runs` peut être `SUCCESS` ; `portfolio_snapshots` n’est pas écrit.

### 8.4 Traçabilité minimale
- Chaque tentative doit produire une ligne `runs` (SUCCESS/SKIPPED/FAIL).
- `ingest_reason` est obligatoire dès que `ingest_status != SUCCESS`.

### 8.5 Compatibilité future minimale
- Le schéma doit tolérer l’ajout futur :
  - de nouvelles colonnes/champs
  - de nouvelles tables/collections (si de nouveaux artefacts Desk Pro deviennent prouvés)
  - d’un “raw store” séparé si une décision ultérieure l’exige

## 9. Choix figés vs non figés

### Figés / ETABLIS (par cette décision)
- Moteur DB non figé.
- Tables physiques minimales : `runs`, `run_module_counts`, `portfolio_snapshots`.
- Unicité/idempotence par `run_key`.
- Statuts et traçabilité minimale via `runs.ingest_status` + `runs.ingest_reason`.
- Index minimaux sur `run_key` et timestamps d’observation.

### NON FIGÉS
- Moteur DB final.
- DDL exact (types précis, contraintes spécifiques, migrations).
- Scheduling et automatisation (service/timer/cron).
- Rétention/archivage/backfill.
- Tuning et indexation avancée.
- Temps réel.

## 10. Ce que cette décision n’autorise pas encore
- Pas d’implémentation runtime.
- Pas de service / cron / timer.
- Pas de promesse de temps réel.
- Pas de promotion de `db-layer` en produit fini.

## 11. Prochain GO recommandé
> GO_DB_LAYER_INGESTION_MINIMAL_IMPL_01

## 12. Références canoniques minimales
- [DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md)
- [DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md)
- [DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md)
- [db_layer_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_runbook.md)
- [db_layer_desk_pro_quick_reference.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_quick_reference.md)
- [admin_trading_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/admin_trading_desk_pro_runbook.md)
