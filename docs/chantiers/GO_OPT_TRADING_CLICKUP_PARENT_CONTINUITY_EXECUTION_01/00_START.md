---
doc_id: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01
go_id: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01
machine: fantome
status: active
lifecycle_stage: execution
links:
  - docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/INDEX.md
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/10_EXECUTION_SUMMARY.md
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/90_CLOSEOUT.md
---

# 00_START — GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01

## Objet

Executer le bundle ClickUp V1 et creer le cockpit operateur initial opt-trading.

## Contexte

- Plan apps valide (PR #224): ClickUp → Repo KG → Airtable → Botpress
- Bundle implementation V1 present dans `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/`
- Execution via ClickUp API v2

## Structure

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_EXECUTION_SUMMARY.md` | Resume complet de l'execution |
| `execute_clickup.py` | Script d'execution ClickUp API |
| `execution_results.json` | Resultats bruts API |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Contraintes

- Aucun secret commit (token dans /tmp/clickup_token, hors repo)
- ClickUp = cockpit de pilotage uniquement, pas source canonique
- Repo, commits, PR restent la preuve

## RISKS

- À qualifier.
