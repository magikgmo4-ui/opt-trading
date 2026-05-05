# 05_MASTER_PROJECT_PLAN — GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01

## Plan séquentiel

| Phase | Fichier | Résumé | Dépendance |
|-------|---------|--------|------------|
| 1 | 10_PHASE_1_LOCAL_MCP_OBSERVER.md | Smoker tradingview-mcp depuis Claude Code sur cursor-ai | Aucune |
| 2 | 20_PHASE_2_ALERTS_INVENTORY_AND_CONTROL.md | Inventaire et manipulation contrôlée des alertes | Phase 1 PASS |
| 3 | 30_PHASE_3_OPT_TRADING_WRAPPER.md | Wrapper opt-trading lecteur seul | Phase 1 PASS |
| 4 | 40_PHASE_4_OPENCLAW_SKILL_INTEGRATION.md | Skill OpenClaw orchestrateur | Phases 1-3 PASS |
| 5 | 50_PHASE_5_ADMIN_TRADING_BRIDGE_OPTIONAL.md | Pont optionnel admin-trading | Phases 1-4 PASS |
| 6 | 60_PHASE_6_PRODUCT_HARDENING.md | Hardening produit final | Phase 5 PASS (ou 4 si 5 skip) |
| 7 | 70_FINAL_PRODUCT_TARGET.md | Cible produit final | Toutes phases PASS |

## Critères de passage

Chaque phase produit un verdict : **PASS / PARTIAL / FAIL**.
Une phase suivante ne s'ouvre qu'après PASS de sa dépendance.

## Gouvernance

- Chaque phase est traçable via son fichier dédié.
- Le closeout final est dans `90_CLOSEOUT.md`.
- Les risques et invariants sont dans `80_RISKS_AND_INVARIANTS.md`.
