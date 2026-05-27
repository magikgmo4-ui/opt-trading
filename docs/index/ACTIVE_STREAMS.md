---
doc_id: OPT_TRADING_ACTIVE_STREAMS
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - active_streams
  - continuity
  - reprise
  - master_project_plan
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section MASTER_PROJECT_PLAN active streams"
updated_at: 2026-05-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
---

# ACTIVE_STREAMS — opt-trading

## Objet

Ce document référence les flux parents actifs avec produit utilisable ou correction structurelle de lecture produit dans `opt-trading`.

Depuis la remédiation produit/surface, les flux actifs doivent être lus comme continuité de `MASTER_PROJECT_PLAN`, pas seulement comme liste de GO.

---

## Règles

- ne référencer ici que les parents avec produit utilisable, cible produit claire ou correction structurante de la lecture produit ;
- les enfants, micro-GO, bundles et artefacts support vivent dans les dossiers chantier ;
- l'état réel du repo prime sur toute reconstruction documentaire ;
- `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` classe les produits/surfaces finales utilisables `PF_*` ;
- chaque flux actif doit tendre vers : `PF_* -> 1_MASTER_TARGET -> 4_MASTER_PROJECT_PLAN -> parent de continuité -> child/bundle` ;
- support/tool/other doit avoir son parent de continuité ou être rattaché explicitement à un `4_MASTER_PROJECT_PLAN`.

---

## MASTER_PROJECT_PLAN active streams

| PF_ID | MASTER_PROJECT_PLAN_ID | Parent continuité | Statut | Gap actif | Next action |
|---|---|---|---|---|---|
| `PF_DESK_PRO` | `MPP_DESK_PRO_OPERATIONAL` | `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_01` | à rattacher/compléter | close gate produit à confirmer | `TBD_MASTER_PROJECT_PLAN` |
| `PF_DATA_CENTER` | `MPP_DATA_CENTER_NORMALIZED_REGISTRY` | `GO_OPT_TRADING_DATA_CENTER_PARENT_01` | à créer | parent absent | `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01` |
| `PF_TELEGRAM_SCREENER` | `MPP_TELEGRAM_SCREENER_OPERATIONAL` | `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_01` | à créer/promouvoir | parent absent ou non canonisé | `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01` |
| `PF_TELEGRAM_INGESTION` | `MPP_TELEGRAM_INGESTION_OPERATIONAL` | `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_01` | à créer/promouvoir | parent absent ou non canonisé | `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01` |
| `PF_BOT_VISION_HEADLESS` | `MPP_BOT_VISION_HEADLESS_OPERATIONAL` | `GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01` | à rattacher | parent produit à confirmer | `TBD_MASTER_PROJECT_PLAN` |
| `PF_SIGNAL_CHAIN_PRODUCT` | `MPP_SIGNAL_CHAIN_PRODUCT_COMPLETE` | `GO_OPT_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_BUNDLE_20260519` | actif à compléter | closeout produit incomplet | `TBD_CLOSE_GATE` |
| `PF_OPENCLAW_ORCHESTRATOR_FULL` | `MPP_OPENCLAW_ORCHESTRATOR_FULL` | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | à rattacher/promouvoir | parent hors pilotage immédiat | `TBD_MASTER_PROJECT_PLAN` |
| `PF_OPERATOR_RUNTIME` | `MPP_OPERATOR_RUNTIME` | `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | actif à compléter | close gate runtime à définir | `TBD_CLOSE_GATE` |
| `PF_LOCALCMS_COCKPIT` | `MPP_LOCALCMS_COCKPIT` | `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | ouvert à compléter | inventaire UI non réalisé | `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01` |
| `PF_STRATEGY_FRAMEWORK_REGISTRY` | `MPP_STRATEGY_FRAMEWORK_REGISTRY` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | actif à compléter | closeout produit incomplet | `TBD_CLOSE_GATE` |
| `PF_PERF_ENGINE_TRADING_LAB` | `MPP_PERF_ENGINE_TRADING_LAB` | `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_01` | à créer | parent absent | `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01` |
| `PF_GOOGLE_SHEETS_CONSUMER` | `MPP_GOOGLE_SHEETS_GLOBAL_CONSUMER` | `GO_OPT_TRADING_GOOGLE_SHEETS_CONSUMER_PARENT_01` | à créer/rattacher | parent absent ou non canonisé | `GO_OPT_TRADING_GOOGLE_SHEETS_CONSUMER_PARENT_OPEN_01` |
| `PF_STRICT_WORKERS_AI_TEAM` | `MPP_STRICT_WORKERS_AI_TEAM` | `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | ouvert à compléter | closeout draft_only / continuité à réaligner | `TBD_CLOSE_GATE` |
| `PF_FIGMA_FINANCIAL_COCKPIT` | `MPP_FIGMA_FINANCIAL_COCKPIT` | `GO_OPT_TRADING_FIGMA_FINANCIAL_COCKPIT_PARENT_01` | optionnel à confirmer | décision produit requise | `TBD_DECISION` |

---

## Flux parents actifs historiques

Ces flux restent utiles comme continuité existante. Leur rattachement cible est désormais visible dans la table `MASTER_PROJECT_PLAN active streams`.

### GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01
- produit utilisable : registre canonique des produits/surfaces finales `PF_*`
- statut : OPEN
- gap restant : audit des parents actifs contre `PF_*`
- target courant : alignement matrice + index globaux
- next action : `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01`
- blocage : aucun ; doc/governance only

### GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
- produit utilisable : doctrine multi-agents canonisée
- statut : OPEN
- gap restant : entrée d'index agrégée ; closeout final à produire ; rattachement PF/MPP à confirmer
- target courant : maintenir la méthode parent-local + inbox
- next action : surveiller prochains INDEX_PATCH
- blocage : aucun runtime

### GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
- produit utilisable : parent machine admin-trading
- statut : OPEN
- gap restant : parent ouvert, child non ouvert ; rôle support/machine à rattacher à un MPP
- target courant : maintenir le parent
- next action : ouvrir child si besoin produit
- blocage : aucun

### GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01
- produit utilisable : parent machine db-layer
- statut : OPEN
- gap restant : parent ouvert, child non ouvert ; rôle support/machine à rattacher à un MPP
- target courant : maintenir le parent
- next action : ouvrir child si besoin produit
- blocage : aucun

### GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01
- produit utilisable : classification des lignées runtime
- statut : ACTIVE
- gap restant : arbitrages de lignée ouverts ; peut rester support P3 si non testable comme produit
- target courant : consolider survivant/transition/legacy/archive
- next action : figer en gap-only
- blocage : aucun

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- produit utilisable : canonique modules/reseau_ssh
- statut : OPEN
- gap restant : compatibilité scripts/reseau_ssh et step1b
- target courant : réduire compat réseau/ssh
- next action : ouvrir lot de réduction compat sur scripts/reseau_ssh
- blocage : ne pas retirer anciens points d'entrée avant coupe explicite

### GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
- produit utilisable : cadrage tmux-ide et bundle IDE
- statut : ACTIVE
- gap restant : validation machine cible réelle
- target courant : implémentation tmux-ide
- next action : exécuter GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
- blocage : machine cible à vérifier ; OpenClaw hors scope

### GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01
- produit utilisable : intégration UI producer-consumer
- statut : OPEN
- gap restant : inventaire UI non réalisé
- target courant : intégration UI producer-consumer
- next action : reprise recommandée sur GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01
- blocage : aucun

### GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
- produit utilisable : architecture équipe d'agents documentée
- statut : OPEN
- gap restant : dossier parent complet non matérialisé ; rattachement à `MPP_STRICT_WORKERS_AI_TEAM` ou MPP dédié à décider
- target courant : architecture équipe d'agents
- next action : utiliser comme base si GO enfant d'audit documentaire
- blocage : reprise enfant non réouverte

### GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01
- produit utilisable : runtime tmux/opencode/openclaw
- statut : ACTIVE
- gap restant : continuité runtime à maintenir
- target courant : runtime tmux/opencode/openclaw
- next action : maintenir le runtime ; ouvrir suite si besoin produit
- blocage : aucun

### GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01
- produit utilisable : chaîne architecture Mermaid cartographiée, auditée et priorisée
- statut : ACTIVE
- gap restant : ouvrir uniquement des children de preuve fine ou de refactor code ciblé
- target courant : continuité audit architecture + reprise propre depuis closeout
- next action : `GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_LINK_PROOF_01` déjà mergé ; prochaine suite selon boundary de refactor sûre
- blocage : ne pas refactorer le code avant preuve suffisante des boundaries critiques

---

## Hors pilotage immédiat (parents sans produit actif immédiat)

Ces parents sont ouverts dans GO_INDEX.md mais sans produit actif immédiat :
- GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
- GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01
- GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
