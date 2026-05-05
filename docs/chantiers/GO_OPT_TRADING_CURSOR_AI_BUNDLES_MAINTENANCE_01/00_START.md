---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01
machine: cursor-ai
status: active
lifecycle_stage: bundles_maintenance
links:
  - bundles/claude-artifacts/README.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01/50_NEXT_GO_OPTIONS.md
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01.md
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01

## Objet

Option B de la sequence cursor-ai : maintenance Bundles — completer le pack Claude artifacts avec `CHECKLIST_EXECUTION.md` et `bundle_meta/manifest.json`, et mettre a jour l'index `bundles/README.md`.

## Etat valide

- PR #210 : Option A (alert webhook test safe) mergee.
- Pack Claude artifacts existant : README, PROMPT_TEMPLATES, REPRISE_TEMPLATE, NO_COMMIT_RULES.
- Bundles workflow actif (PR #207).

## Livrables

| Fichier | Action |
| --- | --- |
| `bundles/claude-artifacts/CHECKLIST_EXECUTION.md` | CREER |
| `bundles/claude-artifacts/bundle_meta/manifest.json` | CREER |
| `bundles/README.md` | METTRE A JOUR (index) |

## Structure du GO

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_SOURCE_STATE.md` | Etat des sources |
| `20_MAINTENANCE_PLAN.md` | Plan de maintenance |
| `30_MODIFICATIONS.md` | Liste des modifications |
| `40_VERIFICATION.md` | Verification post-maintenance |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Invariants

- Machine : cursor-ai.
- Doc-only.
- Admin-trading ferme.
- Aucun secret.
