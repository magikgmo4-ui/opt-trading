---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01_30_STATUS_PATCH
doc_type: chantier/status_patch
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01
status: active
scope: doc-only
---

# 30_STATUS_PATCH

## Surfaces a regulariser

Le closeout produit doit mettre a jour uniquement les surfaces propres au pack Claude Artifacts :

| Surface | Changement attendu |
| --- | --- |
| `bundles/claude-artifacts/README.md` | statut `product_closed`, lifecycle `product_closed`, invariant pack ferme |
| `bundles/claude-artifacts/bundle_meta/manifest.json` | status `product_closed`, version patch si necessaire |
| `docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_PRODUCT_CLOSEOUT_01.md` | entree courte du GO |
| `90_CLOSEOUT.md` | verdict PASS |

## Surfaces a ne pas modifier

| Surface | Raison |
| --- | --- |
| `docs/index/GO_INDEX.md` | index global hors scope |
| `docs/index/ACTIVE_STREAMS.md` | index global hors scope |
| `docs/index/NEXT_GO_CANDIDATES.md` | index global hors scope |
| `docs/index/REPRISE.md` | index global hors scope |
| `docs/index/BRANCH_STATE.md` | branche/PR pas encore mergee |
| `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` | pas de changement de rattachement machine |

## Note de coherence

Le statut `PRODUCT_CLOSED` s'applique au pack `claude-artifacts` seulement. Il ne ferme pas la famille `Bundles` globale ni les autres applications `cursor-ai`.
