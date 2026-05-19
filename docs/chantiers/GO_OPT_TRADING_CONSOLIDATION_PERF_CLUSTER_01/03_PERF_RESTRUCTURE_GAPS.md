---
doc_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01_RESTRUCTURE_GAPS
doc_type: restructure_gaps
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_gaps
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - perf
  - restructure
  - gaps
  - risks
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/03_PERF_RESTRUCTURE_GAPS.md
point_de_reprise: "Gaps, risques et proposition de GO séparé pour restructuration PERF."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/01_PERF_CLUSTER_INVENTORY.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/02_PERF_CONSOLIDATION_MAP.md
---

# 03_PERF_RESTRUCTURE_GAPS

## 1_OBJECTIF

Documenter les gaps structurels du cluster PERF et les risques associés à une restructuration physique, sans exécuter ladite restructuration.

## 2_GAPS_STRUCTURELS

### G1 — Code racine

```text
perf/perf_app.py est à la racine du repo, pas dans modules/.
C'est une violation du standard : tout code applicatif devrait être dans modules/.

Impact : rend le repo moins lisible, complique la découverte.
Risque si on déplace : casser uvicorn (module path), casser les scripts de lancement.
```

### G2 — Adaptateur orphelin

```text
adapters/webhook_to_perf.py n'a aucun caller.
Le code est écrit et fonctionnel, mais le pipeline webhook → perf n'est pas activé.

Impact : code mort potentiel. À intégrer ou archiver.
Risque si on intègre : créer un flux non testé en production.
```

### G3 — Façade shell vs runtime

```text
modules/perf/ est une coquille shell qui pointe vers perf/perf_app.py.
La façade ne fait pas ce que son emplacement suggère.

Impact : confusion pour les opérateurs. modules/perf/ semble être le module
         mais le vrai code est ailleurs.
Risque si on consolide : la façade shell doit être préservée ou remplacée.
```

### G4 — Base SQLite hors modules

```text
perf/perf.db est à la racine, pas dans data/.
Le chemin est hardcodé dans perf_app.py.

Impact : mélange code et données à la racine.
Risque si on déplace : casser la persistence des données existantes.
```

## 3_RISQUES_DE_RESTRUCTURATION

| Action | Risque | Sévérité | Mitigation |
|---|---|---|---|
| Déplacer perf_app.py → modules/perf/ | uvicorn path cassé, scripts à mettre à jour | HIGH | GO dédié avec tests |
| Déplacer perf_engine → modules/perf/ | desk_pro_orchestrator subprocess cassé | HIGH | GO dédié avec tests |
| Déplacer webhook_to_perf.py → modules/perf/ | Aucun caller = risque faible | LOW | Intégration en même temps |
| Déplacer perf.db → data/ | Perte de données si mal migré | MEDIUM | Backup + migration script |
| Fusionner modules/perf/ + modules/perf_engine/ | Conflit de nom, shell vs Python | MEDIUM | Renommer la façade shell |

## 4_PROPOSITION_DE_GO_SEPARE

```text
GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01

Objectif :
  Planifier la restructuration physique du cluster PERF sans l'exécuter.

Livrables :
  - 00_CADRAGE.md
  - 01_MIGRATION_PLAN.md (script de migration pas-à-pas)
  - 02_IMPACT_ANALYSIS.md (tous les fichiers/scripts/registres impactés)
  - 03_ROLLBACK_PLAN.md
  - 90_CLOSEOUT.md

Prérequis :
  - CONSOLIDATION_PERF_CLUSTER_01 = PASS (le présent child)
  - Accord opérateur sur la restructuration

Cible proposée (à valider dans le GO séparé) :
  modules/perf/
  ├── README.md
  ├── __init__.py
  ├── engine/          ← perf_engine migré
  ├── app.py           ← perf_app.py migré (depuis racine)
  ├── webhook.py       ← webhook_to_perf.py migré (depuis adapters/)
  └── data/            ← perf.db migré (depuis racine)
```

## 5_REGLES_POUR_LE_GO_DE_RESTRUCTURATION

```text
R1. Le GO de restructuration est un PLAN, pas une exécution.
R2. L'exécution réelle viendra dans un 3e GO : PERF_MODULE_RESTRUCTURE_IMPL_01.
R3. Aucune restructuration ne peut casser desk_pro (dépendance critique).
R4. Toute modification de uvicorn path doit être coordonnée avec les scripts de lancement.
R5. La base SQLite doit être backupée avant migration.
R6. Le webhook_to_perf doit être intégré au pipeline ou archivé.
```

## 6_DECISION_DIFFEREE

```text
Les actions suivantes sont DIFFÉRÉES à un GO séparé :
  - Déplacement de perf/perf_app.py
  - Déplacement de modules/perf_engine/
  - Déplacement de adapters/webhook_to_perf.py
  - Changement de uvicorn module path
  - Changement de SQLite path
  - Modification des imports desk_pro
  - Mise à jour des scripts de lancement
```

## 17_RESUME_POINT

```text
4 gaps structurels documentés.
5 risques de restructuration évalués avec mitigation.
1 GO séparé proposé : PERF_MODULE_RESTRUCTURE_PLAN_01.
Aucune restructuration exécutée dans ce child.
```
