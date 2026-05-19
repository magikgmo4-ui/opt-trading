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
- PR #206 mergee dans `sot/mainline` pour le pack operateur initial.
- Au `2026-05-08`, `sot/mainline` contient deja les prolongements documentaires relies au pack (Bundles actif, real usage test, operator reprise/export).
- `alert_webhook = ACTIVE_CONTINUITY`.
- `Bundles = APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED`.
- `admin-trading = gate fermee`.
- Runtime non modifie.
- Claude artifacts / IDE Bundle presents ; premier pack deja cree, dossier canonique regularise ici.

## Structure canonique au `2026-05-08`

| Fichier | Contenu |
| --- | --- |
| `00_GO_OPEN.md` | Ouverture canonique du chantier et contraintes |
| `10_SOURCE_STATE.md` | Etat source machine + etat prouve sur `sot/mainline` |
| `20_OPERATOR_PACK_SPEC.md` | Spec du pack operateur et perimetre |
| `30_ARTIFACTS_INDEX.md` | Index des artefacts, dependances et traces legacy |
| `40_USAGE_WORKFLOW.md` | Workflow d'usage operateur |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Traces legacy conservees

Les fichiers suivants restent en place pour ne pas casser les liens deja presents dans le repo :

- `00_START.md`
- `10_SOURCE_BUNDLES_INVENTORY.md`
- `20_OPERATOR_USAGE.md`
- `30_PROMPT_TEMPLATES.md`
- `40_BUNDLE_INTEGRATION.md`
- `50_NO_COMMIT_RULES.md`

## Pack bundle

Les artefacts reutilisables sont dans `bundles/claude-artifacts/` :
- `README.md`
- `PROMPT_TEMPLATES.md`
- `REPRISE_TEMPLATE.md`
- `NO_COMMIT_RULES.md`
- `CHECKLIST_EXECUTION.md`
- `bundle_meta/manifest.json`

## Invariants

- Machine cible : cursor-ai uniquement.
- Ne pas ouvrir admin-trading.
- Ne pas modifier runtime.
- Ne pas committer secrets, .env, tokens ou outputs sensibles.
- Ne pas marquer alert_webhook comme ferme.
- Ne pas marquer Bundles produit comme ferme.
