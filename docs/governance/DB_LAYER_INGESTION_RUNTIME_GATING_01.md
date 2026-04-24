# DB LAYER — INGESTION RUNTIME GATING 01

## Lecture canonique

- lire cette decision apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- utiliser `docs/governance/MATRICE_GOUVERNANTE_V2.md` seulement comme annexe stable secondaire si un recroisement est utile
- ne pas utiliser cette decision a la place des surfaces souveraines de continuite ou de liste

## 1. Objet
- Ce document fixe le gating runtime avant toute implémentation d’ingestion côté `db-layer`.
- Il ne remplace pas la spec pipeline, le mapping logique, la décision physique minimale, ni la décision moteur/DDL minimal.
- Il ne prouve pas une implémentation existante : aucune ingestion DB runtime n’est actuellement établie.

## 2. Besoin initial
- Éviter une implémentation prématurée ou ambiguë.
- Rendre l’ouverture runtime contrôlée, traçable et réversible.
- Empêcher qu’un lot d’implémentation redécide seul le moteur, le schéma ou les garanties minimales.

## 3. Objectif final visé
- Disposer d’un gate opposable avant tout `GO_DB_LAYER_INGESTION_MINIMAL_IMPL_01`.
- Rendre explicites :
  - préconditions obligatoires
  - interdits
  - preuves minimales attendues
  - critères PASS / FAIL
  - conditions de rollback minimal

Plan validé (résumé) :
- Partir de la surface `/shared/desk_pro/latest/` et des artefacts prouvés côté `db-layer`.
- Exiger que l’implémentation future respecte les décisions déjà figées (schéma physique minimal V1 + DDL gabarit + invariants).

## 4. Etat établi actuel

### 4.1 Fil machine
- `admin-trading` = production / export vers `/shared/desk_pro/latest/`
- `student` = consultation
- `db-layer` = consultation + préparation ingestion future (pas d’ingestion DB prouvée)

### 4.2 Fil repo / produit
- Spec pipeline posée : `docs/governance/DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md`
- Mapping logique posé : `docs/governance/DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md`
- Schéma physique minimal posé : `docs/governance/DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md`
- Décision moteur / DDL minimal posée : `docs/governance/DB_LAYER_INGESTION_ENGINE_DECISION_01.md`
- État établi :
  - moteur DB final non figé
  - DDL minimal figé au niveau gabarit (pas dialecte)
  - aucune implémentation runtime encore présente
- Surface de consultation existante (à ne pas casser) :
  - `scripts/db_layer/desk_pro_db_cmd.sh` (status/summary/sanity/shared-info)
  - `scripts/db_layer/desk_pro_db_latest_shared_info.sh` (lecture artefacts depuis `/shared/desk_pro/latest/`)

Gap restant (constat) :
- Ouvrir un lot runtime sans gate risquerait de créer une implémentation ad hoc (moteur/DDL/gating redécidés implicitement).

## 5. Préconditions obligatoires avant implémentation
Ces préconditions doivent être satisfaites *avant* tout travail runtime (module/service/scripts d’ingestion).

1) **Source et artefacts requis (contrat minimal)**
- Source : `/shared/desk_pro/latest/`.
- Artefact requis : `run_summary.json`.
- Artefact optionnel : `portfolio_engine.json`.
- Règle : l’implémentation doit documenter explicitement ce qui est requis vs optionnel (sans inventer d’autres artefacts obligatoires).

2) **Décisions préalables présentes et non contredites**
- Pipeline spec, mapping logique, schéma physique minimal V1, décision moteur/DDL minimal doivent être lus et respectés.
- Toute déviation doit être explicitée comme “écart” et requalifiée en mission dédiée (pas absorbée).

3) **Décision explicite sur le stockage cible concret**
- Soit :
  - une décision explicite “moteur/stockage cible retenu” (moteur DB ou autre stockage concret),
  - soit une décision explicite “moteur non figé” + description de la stratégie de persistance temporaire (si elle existe) et de ses limites.
- Interdit : laisser un moteur/stockage implicite non documenté.

4) **Gabarit DDL minimal utilisable**
- Les tables/collections minimales et leurs contraintes/index minimaux doivent rester identiques au gabarit fixé.
- Si le moteur est choisi, un “DDL dialecte” doit être produit (dans le lot runtime) mais ce gate n’en impose pas encore la forme.

5) **Stratégie minimale de migration/rollback documentée**
- Même en “V0/V1” : définir comment revenir en arrière sans perte silencieuse (ex : supprimer DB locale de test, revert schema version, etc.).
- Ne pas supposer des migrations lourdes ; rester minimal et opposable.

6) **Stratégie minimale de validation documentée**
- Définir à l’avance quelles preuves seront produites (cf. section 7) et sous quelle forme (logs/diffs).

## 6. Interdits avant ouverture runtime
Ces interdits doivent rester vrais tant que le lot runtime n’est pas terminé, validé, et borné.

- Pas de service / cron / timer permanent.
- Pas de promesse de temps réel.
- Pas de migration implicite ou destructive (suppression silencieuse de données).
- Pas de modification de la chaîne Desk Pro côté producteur (`admin-trading`) dans le même lot.
- Pas d’extension multi-machine non bornée (rester `db-layer` only).
- Pas de changement cassant la consultation existante (`desk-pro-db-shared-info`, `desk_pro_db_cmd.sh shared-info`).
- Pas de décision implicite sur un moteur DB “par défaut”.

## 7. Preuves minimales attendues
Ce qu’un futur lot d’implémentation devra démontrer (preuves opposables), sans exiger ici le code.

1) **Lecture réelle de la surface source**
- Preuve : exécution qui constate `/shared/desk_pro/latest/` et liste les artefacts présents.
- Doit couvrir le cas “/shared non monté” → sortie propre (SKIPPED/no-op).

2) **Validation artefact requis**
- Preuve : détection explicite de `run_summary.json`.
- Si absent : preuve de statut SKIPPED + raison explicite.

3) **Écriture minimale conforme au gabarit**
- Preuve : création/écriture dans les tables/collections minimales (`runs`, `run_module_counts`, `portfolio_snapshots`).
- Doit inclure la traçabilité : `ingest_status` + `ingest_reason` si non succès.

4) **Idempotence minimale**
- Preuve : relancer l’ingestion deux fois sur la même source ne crée pas de doublons (clé `run_key`).

5) **Comportements optionnels**
- Preuve : si `portfolio_engine.json` absent, ingestion reste SUCCESS ou PARTIEL mais non FAIL, et `portfolio_snapshots` est omis.

6) **Logs / traces minimales**
- Preuve : logs lisibles indiquant SUCCESS/SKIPPED/FAIL et raisons.

7) **Rollback minimal testable**
- Preuve : procédure de rollback documentée et démontrée (au minimum par commande/diff), sans supposer un service.

8) **Non-régression consultation**
- Preuve : les wrappers existants de consultation (`shared-info`, `status`) restent fonctionnels et inchangés ou compatible.

## 8. Critères PASS / FAIL du futur lot runtime

### PASS si
- La consultation existante `db-layer` reste opérationnelle (status/shared-info).
- La lecture `/shared/desk_pro/latest/` est prouvée et gère le cas “/shared absent” en SKIPPED propre.
- `run_summary.json` est traité comme requis ; absence → SKIPPED avec raison, pas FAIL silencieux.
- Le schéma physique minimal V1 est respecté (3 tables/collections minimales) et la traçabilité minimale est écrite.
- Idempotence prouvée (2 exécutions → pas de doublon sur `run_key`).
- Les interdits sont respectés (pas de service/timer, pas temps réel, pas patch producteur).
- Rollback minimal démontré.

### FAIL si
- Un moteur/stockage est choisi implicitement sans décision explicite.
- Le lot modifie `admin-trading` / Desk Pro producteur (scope creep).
- Le lot introduit un service/timer/cron permanent ou promet du temps réel.
- `run_summary.json` absent produit un état ambigu (ni SUCCESS ni SKIPPED, ou pas de raison).
- La relance crée des doublons (idempotence non tenue).
- La consultation existante est cassée (régression).
- Le rollback n’est pas défini ou pas démontrable.

## 9. Rollback / reprise minimale
- Doit être possible de :
  - revenir à l’état “consultation-only” (aucune ingestion active)
  - supprimer/neutraliser le stockage local d’ingestion sans toucher `/shared`
  - conserver des logs suffisamment clairs pour comprendre ce qui a été ingéré
- En cas d’échec :
  - statut explicite `FAIL` ou `SKIPPED` avec raison
  - reprise possible sans ambiguïté (même run re-jouable grâce à `run_key`)

## 10. Choix figés vs non figés

### Figés / ETABLIS (verrouillés par ce gate)
- Respect des décisions existantes (pipeline + mapping + schéma physique minimal + moteur/DDL minimal).
- Artefact requis : `run_summary.json` ; artefact optionnel : `portfolio_engine.json`.
- Invariants : idempotence via `run_key`, statuts SUCCESS/SKIPPED/FAIL + raisons.
- Interdits runtime : pas de service/timer, pas temps réel, pas patch producteur.

### NON FIGES
- Moteur DB final / stockage cible concret (tant qu’aucune décision dédiée ne l’a tranché).
- DDL exact exécutable (dialecte/types/migrations).
- Scheduling, rétention, tuning, exploitation long terme.
- Généralisation multi-source.

## 11. Ce que ce gate n’autorise pas encore
- Pas d’implémentation hors lot dédié (pas de micro-implémentation “en passant”).
- Pas de service prod.
- Pas de job automatique permanent.
- Pas d’extension de périmètre machine.
- Pas de promesse de production complète.

## 12. Prochain GO recommandé
> GO_DB_LAYER_INGESTION_MINIMAL_IMPL_01

## 13. Références canoniques minimales
- [DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md)
- [DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md)
- [DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md)
- [DB_LAYER_INGESTION_ENGINE_DECISION_01.md](file:///c:/Users/ghost/opt-trading/docs/governance/DB_LAYER_INGESTION_ENGINE_DECISION_01.md)
- [desk_pro_db_cmd.sh](file:///c:/Users/ghost/opt-trading/scripts/db_layer/desk_pro_db_cmd.sh)
- [desk_pro_db_latest_shared_info.sh](file:///c:/Users/ghost/opt-trading/scripts/db_layer/desk_pro_db_latest_shared_info.sh)
