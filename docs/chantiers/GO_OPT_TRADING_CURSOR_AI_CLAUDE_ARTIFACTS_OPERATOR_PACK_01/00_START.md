---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
machine: cursor-ai
status: active
lifecycle_stage: operator_pack
links:
  - bundles/claude-artifacts/README.md
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01.md
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01

## Objet

Transformer les artefacts Claude / IDE Bundle / Claude cowork live artifacts deja integres dans `sot/mainline` en pack operateur cursor-ai stable.

## Etat valide

- PR #205 mergee dans `sot/mainline`.
- Plan operateur parent cursor-ai integre.
- `alert_webhook = ACTIVE_CONTINUITY`.
- `Bundles = APPLICATION_DOCUMENTED`, produit non ferme.
- `admin-trading = gate fermee`.
- Runtime non modifie.
- Claude artifacts / IDE Bundle presents mais non transformes en operator pack.

## Structure du GO

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_SOURCE_BUNDLES_INVENTORY.md` | Inventaire des sources utilisees |
| `20_OPERATOR_USAGE.md` | Guide d'usage operateur |
| `30_PROMPT_TEMPLATES.md` | Templates de prompts |
| `40_BUNDLE_INTEGRATION.md` | Integration avec Bundles |
| `50_NO_COMMIT_RULES.md` | Regles de non-commit |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Pack bundle

Les artefacts reutilisables sont dans `bundles/claude-artifacts/` :
- `README.md`
- `PROMPT_TEMPLATES.md`
- `REPRISE_TEMPLATE.md`
- `NO_COMMIT_RULES.md`

## Invariants

- Machine cible : cursor-ai uniquement.
- Ne pas ouvrir admin-trading.
- Ne pas modifier runtime.
- Ne pas committer secrets, .env, tokens ou outputs sensibles.
- Ne pas marquer alert_webhook comme ferme.
- Ne pas marquer Bundles produit comme ferme.
