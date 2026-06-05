---
doc_id: GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - consolidation
  - strategy
  - engines
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01/00_CADRAGE.md
point_de_reprise: "Consolider les 4 engines stratégiques éclatés en un répertoire unifié modules/strategy/."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/02_CONSOLIDATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/90_CLOSEOUT.md
---

# 00_CADRAGE — CONSOLIDATION_STRATEGY_CLUSTER_01

## 1_MASTER_TARGET

Consolider les 4 engines de stratégie éclatés en un répertoire unifié `modules/strategy/`, en préservant l'architecture data-driven (JSON pipeline) et en documentant la hiérarchie.

## 2_CONSTAT

```text
PR #246 (AUDIT_ORPHAN_MODULES) a identifié le cluster STRATEGY comme P1.

4 modules éclatés dans modules/ :
  decision_engine/    (contient strategy_logic.py — le cœur stratégique)
  execution_engine/   (traduction décisions → plans d'exécution)
  position_engine/    (gestion d'état des positions)
  portfolio_engine/   (agrégation portefeuille)

Note : strategy_engine/ n'existe pas en tant que répertoire séparé.
La logique stratégique est dans decision_engine/app/strategy_logic.py.

ZÉRO couplage Python entre les 4 modules.
Communication purement data-driven via fichiers JSON.
Chaque module a son propre README, scripts, configs.
```

## 3_PERIMETRE

```text
INCLUS :
  - Migration des 4 répertoires sous modules/strategy/
  - Conservation de tous les fichiers (code, configs, scripts, READMEs)
  - Mise à jour des imports internes (références aux anciens chemins)
  - Création d'un README.md unifié pour modules/strategy/
  - Backup des anciens répertoires dans _archive/

EXCLUS :
  - Modification du code métier
  - Changement des interfaces JSON
  - Exécution de tests (0 runtime)
  - Suppression destructive
```

## 4_ARCHITECTURE_CIBLE

```text
modules/strategy/
├── README.md               ← documentation unifiée du pipeline
├── pipeline.md             ← flow JSON entre les 4 étages
├── decision/
│   ├── __init__.py
│   ├── app/
│   │   ├── decision_engine.py
│   │   └── strategy_logic.py    ← cœur stratégique (BTC/ETH/Gold levels)
│   ├── config/              ← sample_liquidations, probability, ranker
│   └── scripts/
├── execution/
│   ├── __init__.py
│   ├── executor.py
│   ├── app/execution_engine.py
│   ├── adapters/paper.py    ← adapter d'exécution papier
│   ├── config/              ← sample_decisions, risk
│   └── scripts/
├── position/
│   ├── __init__.py
│   ├── models.py
│   ├── position_manager.py
│   ├── storage.py
│   ├── app/position_engine.py
│   ├── config/              ← sample_decisions, execution, risk
│   └── scripts/
└── portfolio/
    ├── __init__.py
    ├── app/portfolio_engine.py
    ├── config/              ← sample_journal, perf, positions, risk
    └── scripts/
```

## 5_FLUX_JSON

```text
[Market Data / Ranker / Probability / Liquidation]
                    │
                    ▼
         decision/  ──►  decision_output.json
                    │
                    ▼
         execution/ ──►  execution_plan.json
                    │
                    ▼
         position/  ──►  position_state.json
                    │
                    ▼
         portfolio/ ──►  portfolio_view.json
```

## 12_INVARIANTS

```text
- 0 runtime, 0 exécution de code
- 0 modification du code métier
- 0 suppression sans backup dans _archive/
- Chaque répertoire d'origine est sauvegardé avant migration
- Les imports internes sont mis à jour si des chemins absolus référencent les anciens modules
- Le README unifié documente le pipeline complet
```

## 17_RESUME_POINT

```text
CONSOLIDATION_STRATEGY_CLUSTER_01 ouvert.
4 engines → modules/strategy/{decision,execution,position,portfolio}
Zéro couplage Python → migration simple.
Prochaine action : validation → plan de migration → closeout.
```

## RISKS

- À qualifier.
