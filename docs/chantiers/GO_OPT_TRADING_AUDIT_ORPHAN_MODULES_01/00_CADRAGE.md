---
doc_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - audit
  - orphan-modules
  - consolidation
  - cleanup
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/00_CADRAGE.md
point_de_reprise: "Auditer les 10 modules orphelins et produire un plan de consolidation pour les 8 clusters identifies."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/04_SYNTHESIS_AND_HYPOTHETICAL_TREE.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/01b_REPO_PRODUCT_CANDIDATES_ADDENDUM.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
---

# 00_CADRAGE — AUDIT_ORPHAN_MODULES_01

## 1_MASTER_TARGET

Auditer les 10 modules orphelins identifiés par `REPO_INVENTORY_01` (PR #240) et produire un plan de consolidation pour les 8 clusters de modules éclatés.

Objectif : nettoyer le repo, réduire la fragmentation, documenter chaque décision (ARCHIVE / KEEP / CONSOLIDATE / PROMOTE).

## 2_CONSTAT

```text
PR #240 (REPO_INVENTORY_01) a scanné ~87 surfaces du repo.
Résultat :
  - 7 ADD_TO_ATLAS (traitées par PR #242)
  - 16 KEEP_CANDIDATE
  - 27 DO_NOT_PROMOTE / ARCHIVE_ONLY
  - 10 A AUDITER
  - 1 UNKNOWN_NEEDS_RESCAN (kil_v1)

Les 10 "A AUDITER" sont des modules sans documentation exploitable,
sans preuve d'usage, ou au rôle inconnu.

8 clusters de modules éclatés ont été identifiés (STRATEGY, UI, PERF,
DEEPSEEK, BOT_VISION, COLLECTORS, OPENCLAW, SCRIPTS_LEGACY).
```

## 3_PERIMETRE

### 3.1 Les 10 modules à auditer

| # | Module | Problème |
|---|---|---|
| 1 | `kil_v1` | Rôle totalement inconnu. UNKNOWN_NEEDS_RESCAN |
| 2 | `hf_free_platform` | Aucune doc canonique. Plateforme HF. Aucune preuve d'usage |
| 3 | `mimo_open_observer` | Aucune doc canonique. Observateur MIMO. Aucune preuve d'usage |
| 4 | `strategy_engine` | Module isolé, éclaté, peu documenté. Pas de chantier actif |
| 5 | `marketdata` | Rôle flou. Preuve d'usage peu documentée |
| 6 | `webhook_server.py` | Runtime racine historique. Doublon potentiel avec `modules/webhook/` |
| 7 | `e2e_telegram_smoke.py` | Racine. Branche Botpress. À relier ou archiver |
| 8 | `smoke_adapter.py` | Racine. Branche Botpress. À relier ou archiver |
| 9 | `smoke.sh` | Script. Périmètre à confirmer |
| 10 | `smoke_tv_engine.py` | Script. Périmètre à confirmer |

### 3.2 Les 8 clusters à consolider

| # | Cluster | Composants éclatés |
|---|---|---|
| 1 | STRATEGY | `strategy_engine`, `decision_engine`, `execution_engine`, `position_engine`, `portfolio_engine` |
| 2 | UI / DASHBOARD | `desk_pro_dashboard`, `ui_registry_msi`, `market_scanner`, `LocalCMS` |
| 3 | PERF | `perf_engine`, `perf`, `perf_app.py`, `webhook_to_perf.py` |
| 4 | DEEPSEEK | `deepseek_hub`, `deepseek_student`, `deepseek_response`, `deepseek_thinking`, `scripts/student/` |
| 5 | BOT_VISION | `vision_bot`, `bot_vision_step2`, `bot_vision` |
| 6 | COLLECTORS | `derivatives_collector`, `collector_coingecko`, `collector_binance_spot`, `collectors_core`, `marketdata` |
| 7 | OPENCLAW | 9 modules + 2 observers + docs |
| 8 | SCRIPTS_LEGACY | `scripts/desk_pro_*.sh`, `scripts/reseau_*`, `scripts/ui_debug/` |

## 4_MASTER_PROJECT_PLAN

1. Pour chaque module "A AUDITER" : lire le code source, déterminer le rôle réel, vérifier les dépendances.
2. Produire une décision par module : ARCHIVE, KEEP_CANDIDATE, ou RATTACHER.
3. Pour chaque cluster : proposer un survivant canonique, un plan de migration, une priorité.
4. Produire une matrice de décision finale.
5. Respecter les invariants : 0 runtime, 0 secret, 0 suppression destructive sans backup.

## 6_FINAL_TARGET

Livrables :

```text
docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/
├── 00_CADRAGE.md
├── 01_ORPHAN_AUDIT.md       ← audit complet des 10 modules
├── 02_CONSOLIDATION_PLAN.md ← plan pour les 8 clusters, priorisé
└── 90_CLOSEOUT.md           ← verdict + décisions finales

+ inbox :
  docs/index/inbox/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01.md
```

## 12_INVARIANTS

```text
- 0 runtime
- 0 secret
- 0 suppression destructive sans backup dans _archive/
- 0 modification de code (audit documentaire uniquement)
- Chaque décision doit être documentée avec sa justification
- Les modules archivés restent dans _archive/legacy_modules/ (pas de rm -rf)
- Les consolidations sont des PLANS, pas des exécutions (les GO de consolidation suivront)
- Respecter le UPDATE_PROTOCOL canonisé (PR #245)
```

## 15_REMAINING_GAP

```text
- Certains modules n'ont aucun fichier de documentation → l'audit devra inférer le rôle depuis le code
- Les dépendances inter-modules ne sont pas toutes cartographiées
- Les 5 clusters non-prioritaires (BOT_VISION, COLLECTORS, OPENCLAW, SCRIPTS_LEGACY) sont documentés mais non planifiés en détail
```

## 17_RESUME_POINT

```text
AUDIT_ORPHAN_MODULES_01 ouvert.
10 modules à auditer, 8 clusters à planifier.
0 runtime, 0 secret, audit documentaire uniquement.
Prochaine action : validation → audit → consolidation plan → closeout.
```
