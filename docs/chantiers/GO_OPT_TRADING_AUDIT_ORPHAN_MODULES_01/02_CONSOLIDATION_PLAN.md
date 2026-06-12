---
doc_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01_CONSOLIDATION_PLAN
doc_type: consolidation_plan
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
status: draft_for_review
lifecycle_stage: child_consolidation_plan
parent_go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - consolidation
  - clusters
  - modules
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/02_CONSOLIDATION_PLAN.md
point_de_reprise: "Plan de consolidation des 8 clusters de modules éclatés."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/01_ORPHAN_AUDIT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/04_SYNTHESIS_AND_HYPOTHETICAL_TREE.md
---

# 02_CONSOLIDATION_PLAN

## 1_OBJECTIF

Pour chaque cluster de modules éclatés, définir le survivant canonique, la cible de consolidation, la priorité, et le GO associé.

## 2_PRIORITES

```text
P1 (IMMÉDIAT) : STRATEGY, UI/DASHBOARD, PERF, DEEPSEEK
P2 (COURT TERME) : BOT_VISION, COLLECTORS
P3 (MOYEN TERME) : OPENCLAW
P4 (LONG TERME) : SCRIPTS_LEGACY
```

---

## 3_CLUSTER_P1 — STRATEGY

### 3.1 État actuel

```text
Composants éclatés :
  modules/strategy_engine/     → moteur de stratégie (A AUDITER, décision: RATTACHER)
  modules/decision_engine/     → moteur de décision (KEEP_CANDIDATE)
  modules/execution_engine/    → moteur d'exécution (KEEP_CANDIDATE)
  modules/position_engine/     → moteur de position (KEEP_CANDIDATE)
  modules/portfolio_engine/    → moteur de portefeuille (KEEP_CANDIDATE)

Problème : 5 modules éclatés sans hiérarchie claire, sans documentation unifiée.
Chacun est KEEP_CANDIDATE mais isolé.
```

### 3.2 Plan de consolidation

```text
Cible : modules/strategy/  (nouveau répertoire unifié)

Survivant canonique : strategy_engine (donne le nom de la famille)

Structure cible :
  modules/strategy/
  ├── __init__.py
  ├── engine.py          ← strategy_engine consolidé
  ├── decision.py        ← decision_engine migré
  ├── execution.py       ← execution_engine migré
  ├── position.py        ← position_engine migré
  ├── portfolio.py       ← portfolio_engine migré
  └── README.md          ← documentation unifiée

Action :
  1. Créer modules/strategy/
  2. Migrer chaque engine en sous-module
  3. Unifier les imports et les interfaces
  4. Documenter l'architecture
  5. Archiver les anciens répertoires dans _archive/

GO associé : GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01
Priorité : P1
```

---

## 4_CLUSTER_P1 — UI / DASHBOARD

### 4.1 État actuel

```text
Composants éclatés :
  modules/desk_pro_dashboard/ → dashboard Desk Pro (dans l'Atlas: USABLE_LIMITED)
  modules/ui_registry_msi/    → registre UI MSI
  modules/market_scanner/     → scanner de marché (KEEP_CANDIDATE)
  LocalCMS                    → CMS local (dans l'Atlas: DOC_ONLY)
```

### 4.2 Plan de consolidation

```text
Cible : modules/desk_pro/  (Desk Pro comme hub UI unifié)

Survivant canonique : desk_pro_dashboard (déjà dans l'Atlas)

Structure cible :
  modules/desk_pro/
  ├── dashboard/          ← desk_pro_dashboard
  ├── scanner/            ← market_scanner migré
  ├── registry/           ← ui_registry_msi migré
  ├── runner/             ← desk_pro_runner (déjà dans Desk Pro)
  └── README.md

Note : LocalCMS reste externe (pas dans modules/), mais est référencé
comme dépendance optionnelle de la couche UI.

GO associé : GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01
Priorité : P1
```

---

## 5_CLUSTER_P1 — PERF

### 5.1 État actuel

```text
Composants éclatés :
  modules/perf_engine/        → moteur de performance (KEEP_CANDIDATE, preuves live)
  modules/perf/               → analyse de performance
  perf/perf_app.py            ← fichier racine
  adapters/webhook_to_perf.py ← pont webhook → perf
```

### 5.2 Plan de consolidation

```text
Cible : modules/perf/  (unifié sous le nom court "perf")

Survivant canonique : perf_engine (le plus documenté, avec preuves live)

Structure cible :
  modules/perf/
  ├── engine.py           ← perf_engine
  ├── analysis.py         ← modules/perf/ migré
  ├── app.py              ← perf_app.py migré (depuis racine)
  ├── webhook_bridge.py   ← webhook_to_perf.py migré (depuis adapters/)
  └── README.md

Action :
  1. Créer modules/perf/ (écrase l'ancien modules/perf/ après migration)
  2. Unifier sous perf_engine
  3. Déplacer perf_app.py de la racine
  4. Nettoyer adapters/

GO associé : GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
Priorité : P1
```

---

## 6_CLUSTER_P1 — DEEPSEEK

### 6.1 État actuel

```text
Composants éclatés :
  modules/deepseek_hub/       → façade principale (KEEP_CANDIDATE)
  modules/deepseek_student/   → étudiant AI en transition
  modules/deepseek_response/  → compatibilité réponse
  modules/deepseek_thinking/  → compatibilité thinking
  scripts/student/            → runtime scripts (hors modules/)
```

### 6.2 Plan de consolidation

```text
Cible : modules/deepseek/  (unifié sous le nom court "deepseek")

Survivant canonique : deepseek_hub (façade principale)

Structure cible :
  modules/deepseek/
  ├── hub.py              ← deepseek_hub
  ├── student.py          ← deepseek_student
  ├── response.py         ← deepseek_response
  ├── thinking.py         ← deepseek_thinking
  ├── scripts/            ← scripts/student/ migré dans modules/
  └── README.md

Action :
  1. Créer modules/deepseek/
  2. Migrer les 4 modules deepseek_*
  3. Migrer scripts/student/ vers modules/deepseek/scripts/
  4. Archiver les anciens répertoires

GO associé : GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
Priorité : P1
```

---

## 7_CLUSTER_P2 — BOT_VISION

### 7.1 État actuel

```text
Composants éclatés :
  modules/vision_bot/         → capture (dans l'Atlas: USABLE_LIMITED)
  modules/bot_vision_step2/   → analyse
  modules/bot_vision/         → legacy
```

### 7.2 Plan de consolidation

```text
Cible : modules/vision/  (unifié)

Survivant canonique : vision_bot + bot_vision_step2

Structure cible :
  modules/vision/
  ├── bot.py              ← vision_bot
  ├── analysis.py         ← bot_vision_step2
  ├── legacy/             ← bot_vision (archive en lecture seule)
  └── README.md

GO associé : GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01
Priorité : P2
```

---

## 8_CLUSTER_P2 — COLLECTORS

### 8.1 État actuel

```text
Composants éclatés :
  modules/derivatives_collector/   → canonique (dans l'Atlas: USABLE_LIMITED)
  modules/collector_coingecko/     → spot coingecko
  modules/collector_binance_spot/  → spot binance
  packages/collectors_core/        → base commune
  modules/marketdata/              → rôle flou (A AUDITER, décision: RATTACHER)
```

### 8.2 Plan de consolidation

```text
Cible : modules/collectors/  (hub unifié)

Survivant canonique : derivatives_collector

Structure cible :
  modules/collectors/
  ├── core/                ← collectors_core migré dans modules/
  ├── derivatives/         ← derivatives_collector
  ├── spot_coingecko/      ← collector_coingecko
  ├── spot_binance/        ← collector_binance_spot
  ├── marketdata/          ← marketdata (rôle à clarifier pendant la migration)
  └── README.md

Note : marketdata sera soit intégré comme façade unifiée des collectors,
soit archivé s'il fait doublon avec derivatives_collector.

GO associé : GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01
Priorité : P2
```

---

## 9_CLUSTER_P3 — OPENCLAW

### 9.1 État actuel

```text
9 modules OpenClaw + 2 observers + docs.
Déjà cartographié (77 sources). Dans l'Atlas comme USABLE_LIMITED.

Ce cluster est déjà relativement bien organisé.
La consolidation consiste principalement à :
  - réduire le nombre de modules si possible
  - documenter l'architecture unifiée
  - définir une spec runtime unique
```

### 9.2 Plan

```text
GO associé : GO_OPT_TRADING_CONSOLIDATION_OPENCLAW_CLUSTER_01
Priorité : P3 (moyen terme, moins urgent)

Action :
  1. Audit des 11 composants OpenClaw
  2. Proposition de fusion des doublons
  3. Documentation d'architecture unifiée
```

---

## 10_CLUSTER_P4 — SCRIPTS_LEGACY

### 10.1 État actuel

```text
scripts/desk_pro_*.sh    → gelés (OT_OPS_05B)
scripts/reseau_*         → scripts réseau
scripts/ui_debug/        → debug UI
scripts/db_layer/        → couche DB
scripts/desk_bridge/     → pont desk
```

### 10.2 Plan

```text
GO associé : GO_OPT_TRADING_CONSOLIDATION_SCRIPTS_CLUSTER_01
Priorité : P4 (long terme)

Action :
  1. Audit de chaque script
  2. Décision : ARCHIVE (gelé) / MIGRER vers modules/ / CONSERVER (support)
  3. Nettoyage des scripts obsolètes
```

---

## 11_PLANNING_GLOBAL

```text
Phase 1 (IMMÉDIAT — 4 GO) :
  GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01
  GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01
  GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
  GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01

Phase 2 (COURT TERME — 2 GO) :
  GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01
  GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01

Phase 3 (MOYEN TERME — 1 GO) :
  GO_OPT_TRADING_CONSOLIDATION_OPENCLAW_CLUSTER_01

Phase 4 (LONG TERME — 1 GO) :
  GO_OPT_TRADING_CONSOLIDATION_SCRIPTS_CLUSTER_01
```

## 12_REGLES_DE_CONSOLIDATION

```text
R1. Toujours créer un backup dans _archive/ avant de déplacer.
R2. Le survivant canonique est le module le plus documenté et le plus utilisé.
R3. Les imports doivent être mis à jour dans tout le repo après migration.
R4. Chaque consolidation fait l'objet d'un GO dédié avec son propre closeout.
R5. Les tests (s'ils existent) doivent continuer à passer après migration.
R6. Le README.md du nouveau répertoire documente l'architecture unifiée.
```

## 17_RESUME_POINT

```text
8 clusters identifiés et planifiés.
4 prioritaires (P1) : STRATEGY, UI, PERF, DEEPSEEK.
2 court terme (P2) : BOT_VISION, COLLECTORS.
1 moyen terme (P3) : OPENCLAW.
1 long terme (P4) : SCRIPTS_LEGACY.
8 GO de consolidation à ouvrir, priorisés par phase.
```

## RISKS

- À qualifier.
