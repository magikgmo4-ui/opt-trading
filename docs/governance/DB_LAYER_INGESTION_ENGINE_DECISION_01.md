# DB LAYER — INGESTION ENGINE DECISION 01

## 1. Objet
- Ce document décide le niveau moteur / DDL minimal pour l’ingestion future côté `db-layer`.
- Il ne remplace ni la spec pipeline, ni le mapping logique, ni la décision de schéma physique minimal.
- Il ne prouve pas une implémentation existante : aucune ingestion DB runtime n’est actuellement établie.

## 2. Besoin initial
- Dépasser le niveau schéma abstrait et préparer une implémentation future sans ambiguïté excessive.
- Éviter un codage ad hoc au moment de l’ingestion minimale (choix moteur implicite, DDL improvisé).

## 3. Objectif final visé
- Disposer d’une décision opposable sur :
  - moteur retenu ou non retenu (niveau de figement)
  - niveau de figement du DDL minimal (gabarit vs dialecte exact)
  - conditions minimales pour ouvrir l’implémentation

## 4. État établi actuel

### 4.1 Fil machine
- `admin-trading` = production / export vers `/shared/desk_pro/latest/`
- `student` = consultation
- `db-layer` = consultation + préparation ingestion future (pas d’ingestion DB prouvée)

### 4.2 Fil repo / produit
- Spec pipeline : [DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md)
- Mapping logique : [DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md)
- Schéma physique minimal V1 : [DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md)
- État établi :
  - moteur DB final : non figé
  - DDL exact (dialecte/types) : non figé
  - aucune implémentation runtime (DB + DDL appliqué + job) n’est prouvée

Gap restant (constat) :
- Décider ce qui peut être figé sur le moteur et le niveau “DDL minimal” sans inventer un moteur non prouvé.

## 5. Options moteur réellement justifiables

### Option A — Moteur figé maintenant
- Ce que ça permet :
  - DDL exact et immédiatement exécutable (types/contraintes/index selon moteur)
  - ouverture directe d’une implémentation minimale bornée
- Ce que ça fige :
  - moteur, tooling d’exploitation, migrations/backups
- Ce que ça impose trop tôt :
  - une contrainte d’ops et de déploiement non prouvée dans l’état établi
- Verdict : non retenue (aucune preuve repo-sourcée imposant un moteur DB final pour cette ingestion).

### Option B — Moteur non figé, DDL minimal générique figé
- Ce que ça permet :
  - un contrat “DDL gabarit” opposable et stable (tables/champs/PK/UNIQUE/index minimaux)
  - une implémentation future sans dérive, tout en laissant le moteur DB libre
- Ce que ça fige :
  - la structure physique minimale (tables/collections déjà décidées), les contraintes minimales, les index minimaux
- Ce que ça n’impose pas :
  - dialecte exact, types DB exacts, migrations, tuning
- Verdict : retenue.

## 6. Décision retenue
DECISION : moteur non figé, DDL minimal générique figé.

- **Moteur** : NON FIGÉ.
- **DDL minimal** : FIGÉ au niveau “gabarit” (structure + contraintes/index minimaux), NON FIGÉ au niveau “dialecte exécutable”.
- **Niveau opposable** : ce document + la décision de schéma physique minimal définissent le contrat d’implémentation.

Conditions minimales pour ouvrir l’implémentation :
1) une décision explicite sur le moteur (ou un stockage cible concret) ;
2) la traduction du gabarit DDL en DDL exécutable (dialecte + types) ;
3) une stratégie minimale de migration/rollback (même si mono-version) ;
4) une stratégie minimale de runtime gating (comment prouver SUCCESS/SKIPPED/FAIL sans surpromesse).

## 7. DDL minimal retenu (gabarit, pas dialecte)
Le DDL ci-dessous est un **gabarit**. Les types exacts restent non figés tant que le moteur n’est pas décidé.

### 7.1 `runs`
- Champs minimaux (gabarit) :
  - `run_key` (PK, NOT NULL)
  - `run_id` (NULLABLE)
  - `run_timestamp` (NULLABLE)
  - `source_path` (NOT NULL)
  - `ingest_observed_at_utc` (NOT NULL)
  - `ingest_status` (NOT NULL) — `SUCCESS` / `SKIPPED` / `FAIL`
  - `ingest_reason` (NULLABLE)
- Contraintes minimales :
  - UNIQUE(`run_key`)
  - `run_key` non vide
- Index minimaux :
  - index sur `ingest_observed_at_utc`
  - index sur `run_timestamp` (si disponible)

### 7.2 `run_module_counts`
- Champs minimaux :
  - `run_key` (NOT NULL, 1:1 avec `runs`)
  - `modules_ok_count` (NULLABLE)
  - `modules_failed_count` (NULLABLE)
- Contraintes minimales :
  - UNIQUE(`run_key`)
- Index minimaux :
  - index sur `run_key`

### 7.3 `portfolio_snapshots`
- Champs minimaux :
  - `run_key` (NOT NULL, 1:1 avec `runs`)
  - `portfolio_state` (NULLABLE)
  - `exposure_profile` (NULLABLE)
  - `total_max_risk_pct` (NULLABLE)
  - `portfolio_summary` (NULLABLE)
- Contraintes minimales :
  - UNIQUE(`run_key`)
- Index minimaux :
  - index sur `run_key`

## 8. Invariants moteur / écriture
- Idempotence : `run_key` est l’unique clé d’idempotence ; jamais de doublon logique.
- Ordre d’écriture minimal : écrire `runs` d’abord (statut/raison inclus), puis les tables 1:1 si disponibles.
- Artefact requis absent (`run_summary.json`) : produire `runs` en `SKIPPED` avec raison explicite, sans écrire les tables dérivées.
- Artefact optionnel absent (`portfolio_engine.json`) : `runs` peut être `SUCCESS`, `portfolio_snapshots` est omis.
- Traçabilité minimale : chaque tentative doit produire une ligne `runs` avec `ingest_status` et `ingest_reason` si non succès.
- Compatibilité future : schéma extensible (ajout colonnes/tables si de nouveaux artefacts deviennent prouvés).

## 9. Choix figés vs non figés

### Figés / ETABLIS (par cette décision)
- Moteur DB : non figé (décision explicite de ne pas figer).
- DDL minimal : figé au niveau gabarit (champs/contraintes/index minimaux par table).
- Contrat d’implémentation : idempotence/traçabilité et comportements SKIPPED/SUCCESS/FAIL.

### NON FIGÉS
- Moteur DB final / stockage cible concret.
- DDL exact exécutable (dialecte, types, migrations).
- Migrations/rollback.
- Rétention/archivage/backfill.
- Scheduling / jobs automatiques.
- Temps réel, tuning, indexation avancée.
- Déploiement runtime.

## 10. Ce que cette décision n’autorise pas encore
- Pas d’implémentation runtime.
- Pas de service.
- Pas de job automatique.
- Pas de promesse de temps réel.
- Pas de promotion de `db-layer` en produit fini.

## 11. Prochain GO recommandé
> GO_DB_LAYER_INGESTION_ENGINE_FINAL_CHOICE_01

## 12. Références canoniques minimales
- [DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md)
- [DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md)
- [DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md)
- [DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md)
- [db_layer_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_runbook.md)
- [db_layer_desk_pro_quick_reference.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_quick_reference.md)
