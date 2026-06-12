---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01
machine: cursor-ai
status: active
lifecycle_stage: workflow_active
links:
  - bundles/README.md
  - bundles/CURSOR_AI_BUNDLES_REPRISE.md
  - bundles/ACTIVE_WORKFLOW.md
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01.md
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01

## Objet

Passer Bundles de `APPLICATION_DOCUMENTED` a **workflow actif cursor-ai**, sans fermer Bundles produit et sans ouvrir admin-trading.

## Etat valide

- PR #205 : parent operational plan cursor-ai integre.
- PR #206 : pack Claude artifacts integre.
- `bundles/README.md` existe.
- `bundles/CURSOR_AI_BUNDLES_REPRISE.md` existe.
- `bundles/claude-artifacts/` existe.
- `Bundles = APPLICATION_DOCUMENTED`.
- `Bundles produit non ferme`.
- `alert_webhook = ACTIVE_CONTINUITY`.
- `admin-trading gate fermee`.
- `Runtime non modifie`.

## Structure du GO

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_SOURCE_STATE.md` | Etat des sources avant activation |
| `20_ACTIVE_WORKFLOW.md` | Definition de Bundles comme workflow actif |
| `30_BUNDLE_TYPES.md` | Types de bundles utilisables |
| `40_OPERATOR_FLOW.md` | Flux operateur Bundles |
| `50_BOUNDARIES_AND_RULES.md` | Limites no-runtime / no-secret |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Fichiers workflow actif

- `bundles/ACTIVE_WORKFLOW.md`
- `bundles/BUNDLE_TYPES.md`
- `bundles/OPERATOR_FLOW.md`
- `bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md`

## Invariants

- Machine cible : cursor-ai.
- Ne pas ouvrir admin-trading.
- Ne pas modifier runtime.
- Ne pas marquer Bundles produit comme ferme.
- Ne pas marquer alert_webhook comme ferme.
- Ne pas committer secrets, .env, tokens ou outputs sensibles.

## RISKS

- À qualifier.
