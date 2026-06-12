---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/20_ACTIVE_GO_LIST.md
  - docs/index/BRANCH_STATE.md
  - docs/index/GO_INDEX.md
---

# 10_SOURCE_STATE

## Canon machine retenu

| Famille | Etat | Decision locale |
| --- | --- | --- |
| TradingView MCP Observer | `CLOSED / merged` | Ne pas rouvrir |
| `alert_webhook` | `ACTIVE_CONTINUITY` | Continuer a le traiter comme actif |
| Bundles | `APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED` | Ne pas fermer le produit |
| Live artifacts / Claude cowork | `MERGED` | Servent de base au pack |
| DOC_OPS historical | `supprime / historique` | Ne pas rouvrir |
| DOC_OPS open work control | `BLOCKED` | Ne pas toucher |
| References audit Git | `reference` | Lecture seule |

## GO plan retenu par le canon `cursor-ai`

| Priorite | GO | Statut canon |
| ---: | --- | --- |
| 1 | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_APPLICATION_ACTIVE_01` | `ACTIVE_CONTINUITY` |
| 2 | `GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01` | `APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED` |
| 3 | `GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01` | `CANDIDATE` |
| 4 | `GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01` | `FUTURE` |
| 5 | `GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01` | `FUTURE` |

## Etat prouve sur `sot/mainline` au `2026-05-08`

| Element prouve | Etat observe | Impact sur ce passage |
| --- | --- | --- |
| `bundles/claude-artifacts/` | Present avec 6 artefacts (`README`, prompts, reprise, no-commit, checklist, manifest) | Utiliser comme base, ne pas recreer le bundle |
| `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01/` | Dossier deja present avec structure legacy | Regulariser sans casser les liens existants |
| `GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01` | Dossier present sur `sot/mainline` | Confirme que Bundles est deja documente comme workflow actif |
| `GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01` | Dossier present sur `sot/mainline` | Confirme que le pack a deja une validation d'usage reel |
| `GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01` | Dossier present sur `sot/mainline` | Confirme qu'un handoff operateur existe deja |
| `GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01` | Dossier present sur `sot/mainline` | Confirme qu'un export operateur existe deja |

## Sources de lecture seule

- `docs/index/BRANCH_STATE.md` : reference branches uniquement.
- `docs/index/GO_INDEX.md` : reference globale, non suffisante pour rouvrir ou fermer un GO `cursor-ai`.
- `docs/index/GO_CLOSED_INDEX.md` : reference des closeouts, sans action locale dans ce passage.

## Interpretation retenue

Le canon machine du `2026-05-05` positionne ce GO comme meilleur prochain chantier `cursor-ai`. L'etat prouve du repo au `2026-05-08` montre qu'un premier passage sur ce GO et plusieurs prolongements documentaires sont deja merges dans `sot/mainline`.

Ce passage adopte donc une regle simple :

- ne pas refaire d'arbitrage global ;
- ne pas rouvrir de surface interdite ;
- regulariser le dossier `GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01` pour qu'il expose une structure canonique claire et exploitable par `cursor-ai`.

## RISKS

- À qualifier.
