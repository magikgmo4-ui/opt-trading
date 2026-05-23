# GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_PF_STATUS_AUDIT_01

## GO_STRUCTURAL_ROLE

GO_CHILD_ATTACHED_TO_PARENT

## Parent de continuité

GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01

## 1_MASTER_TARGET

MASTER_TARGET_CONTINUITY_INDEX_CLEAN_PARENT_PRODUCT_STATE_01

## 6_FINAL_TARGET

TARGET_MASTER_PROJECT_PLAN_PF_STATUS_AUDIT_01

## Besoin initial

Transformer la table d’audit PF_* publiée dans GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01 en statut confirmé par surface : COMPLETE, MISSING_PARENT, MISSING_MASTER_PROJECT_PLAN, MISSING_BOTH, NEEDS_CLOSE_GATE ou TBD_DECISION.

## Règle forte validée

Avant d’ouvrir un parent pour une surface PF_*, vérifier d’abord si la surface est déjà couverte par le parent umbrella :

GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01

Si la surface est couverte par umbrella, rattacher au parent umbrella et identifier le child ou le next item Kanban, sans créer de parent artificiel.

Si la surface n’est pas couverte par umbrella, chercher un parent dédié existant.

Si aucun parent dédié réel n’existe et que la surface n’est pas optionnelle, proposer ou ouvrir une continuité minimale.

Si la surface est optionnelle, marquer TBD_DECISION.

## Surfaces auditées

- PF_DESK_PRO
- PF_DATA_CENTER
- PF_TELEGRAM_SCREENER
- PF_TELEGRAM_INGESTION
- PF_BOT_VISION_HEADLESS
- PF_SIGNAL_CHAIN_PRODUCT
- PF_OPENCLAW_ORCHESTRATOR_FULL
- PF_OPERATOR_RUNTIME
- PF_LOCALCMS_COCKPIT
- PF_STRATEGY_FRAMEWORK_REGISTRY
- PF_PERF_ENGINE_TRADING_LAB
- PF_GOOGLE_SHEETS_CONSUMER
- PF_STRICT_WORKERS_AI_TEAM
- PF_FIGMA_FINANCIAL_COCKPIT

## Livrables

- Table d’audit consolidée PF -> MPP -> parent -> umbrella -> next -> close gate.
- Classification confirmée par surface.
- NEXT_GO map sans création automatique de parent.
- Bundle de transport doc-only.

## Invariants

- Doc-only.
- Pas de runtime.
- Pas de cleanup branches.
- Pas de parent artificiel.
- Pas de closeout sans CLOSE_GATE_MASTER_TARGET.
- PF_FIGMA_FINANCIAL_COCKPIT reste TBD_DECISION sans validation explicite.
