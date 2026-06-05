---
doc_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01_CONSOLIDATION_MAP
doc_type: consolidation_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_consolidation_map
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - perf
  - map
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/02_PERF_CONSOLIDATION_MAP.md
point_de_reprise: "Carte de consolidation documentaire PERF : ce qu'on sait, ce qui manque."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/01_PERF_CLUSTER_INVENTORY.md
---

# 02_PERF_CONSOLIDATION_MAP

## 1_ETAT_DOCUMENTAIRE_ACTUEL

| Composant | README | Doc chantier | Inline doc (code) | Statut |
|---|---|---|---|---|
| modules/perf_engine/ | Oui | Non | Correcte | DOCUMENTÉ |
| modules/perf/ | Oui (note facade) | Non | N/A (shell) | DOCUMENTÉ |
| perf/perf_app.py | Non | Non | Partielle | PEU DOCUMENTÉ |
| adapters/webhook_to_perf.py | Non | Non | Correcte | PEU DOCUMENTÉ |

## 2_CONSOLIDATION_DOCUMENTAIRE

Ce que ce GO peut faire (docs-only, 0 runtime) :

```text
1. Créer un README unifié dans modules/perf/ qui documente
   les 4 composants et leurs relations.

2. Cartographier le data flow complet :
   - perf_engine.json → desk_pro_orchestrator → dashboard
   - POST /perf/event → perf_app SQLite → /perf/ui
   - webhook_to_perf → (futur) → POST /perf/event

3. Documenter les dépendances critiques :
   - perf_app → desk_pro (API mount) : chemin modules.desk_pro.*
   - perf_app → SQLite : chemin perf/perf.db
   - perf_app → uvicorn : module path perf.perf_app:app
   - perf_engine → desk_pro_orchestrator : subprocess string
```

### README unifié proposé (à créer)

```markdown
# PERF Cluster

Cluster de performance trading pour opt-trading Desk Pro.

## Composants

| Composant | Emplacement | Rôle | Runtime |
|---|---|---|---|
| perf_engine | modules/perf_engine/ | Moteur de performance CLI | Subprocess |
| perf facade | modules/perf/ | Façade shell opérateur | Shell scripts |
| perf_app | perf/perf_app.py | Serveur FastAPI + SQLite | uvicorn :8010 |
| webhook_to_perf | adapters/webhook_to_perf.py | Adaptateur webhook → PerfEvent | Import Python |

## Flux

```
[perf_engine] ──perf_engine.json──> [desk_pro_orchestrator] ──> [desk_pro_dashboard]
[webhook] ──POST /perf/event─────> [perf_app :8010] ──SQLite──> /perf/ui dashboard
```

## Dépendances critiques

- perf_app dépend de modules/desk_pro/ (API mount /desk)
- perf_app utilise SQLite perf/perf.db
- perf_engine est lancé par desk_pro_orchestrator (subprocess)

## Statut Atlas

Cluster PERF = KEEP_CANDIDATE (USABLE_LIMITED potentiel).
Les 4 composants sont découplés en Python, liés par données + orchestration.
```

## 3_CE_QUI_MANQUE

```text
GAP_DOC_1 : perf/perf_app.py n'a pas de README dédié.
            Le code (995 lignes) mérite une doc d'architecture.

GAP_DOC_2 : adapters/webhook_to_perf.py n'a pas de README.
            Aucun caller documenté → à clarifier.

GAP_DOC_3 : Le flux webhook → perf_app n'est pas documenté comme pipeline.
            webhook_to_perf existe mais n'est intégré nulle part.

GAP_DOC_4 : La base SQLite perf/perf.db n'a pas de schéma documenté.
            Tables events et trades, pas de migration script.

GAP_DOC_5 : Les alertes Telegram (no-activity, drawdown) ne sont pas documentées
            dans un fichier dédié (configurées inline dans perf_app.py).
```

## 4_ACTIONS_DOCUMENTAIRES_IMMEDIATES

Actions que ce GO peut réaliser :

```text
1. Créer modules/perf/README.md unifié (remplace le README facade actuel).
2. Documenter les 5 gaps ci-dessus.
3. Proposer un GO séparé pour la restructuration physique si nécessaire.
```

## 5_CE_QUI_RESTE_HORS_PERIMETRE

```text
HORS_SCOPE_1 : Déplacer perf/perf_app.py → modules/perf/app.py
HORS_SCOPE_2 : Déplacer perf_engine/ → modules/perf/engine/
HORS_SCOPE_3 : Déplacer webhook_to_perf.py → modules/perf/webhook.py
HORS_SCOPE_4 : Changer uvicorn perf.perf_app:app → uvicorn modules.perf.app:app
HORS_SCOPE_5 : Changer SQLite perf/perf.db → modules/perf/data/perf.db
HORS_SCOPE_6 : Modifier les imports desk_pro

Toutes ces actions requièrent un GO séparé :
  GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01
```

## 17_RESUME_POINT

```text
Consolidation documentaire uniquement.
5 gaps documentaires identifiés.
1 README unifié à créer.
Toute restructuration physique → GO séparé PERF_MODULE_RESTRUCTURE_PLAN_01.
```

## RISKS

- À qualifier.
