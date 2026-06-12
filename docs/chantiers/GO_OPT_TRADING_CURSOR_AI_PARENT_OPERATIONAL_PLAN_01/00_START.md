---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01
machine: cursor-ai
status: active
lifecycle_stage: operational_plan
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01.md
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01

## Objet

Ce GO parent `doc-only` consolide l'etat operateur cursor-ai en un plan opératoire unique.

Il fixe :
- les GO actifs propres a cursor-ai ;
- les parents et sous-parents ;
- les produits finaux prevus ;
- le role Bundles ;
- le role Claude artifacts ;
- le role alert_webhook ;
- la gate admin-trading ;
- l'ordre recommande des prochains GO.

## Contrainte

- `cursor-ai` continue seul.
- `admin-trading` n'est pas ouvert sans demande explicite.
- Aucun runtime n'est modifie.
- Aucune alerte reelle n'est declenchee.

## Etat valide

- PR #204 mergee dans `sot/mainline`.
- Map cursor-ai clean en 6 sous-sections.
- Parent cursor-ai TradingView MCP ferme transport/docs.
- `alert_webhook = ACTIVE_CONTINUITY`.
- `Bundles = APPLICATION_DOCUMENTED`, produit non ferme.
- Claude cowork / live artifacts / IDE bundle = matiere integree.
- Admin-trading non ouvert.
- Runtime non modifie.

## Structure du GO

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_CURSOR_AI_CANONICAL_STATE.md` | Etat canonique cursor-ai |
| `20_ACTIVE_GO_LIST.md` | Liste des GO actifs cursor-ai |
| `30_PARENT_AND_PRODUCT_MAP.md` | Table parents / GO / produits |
| `40_BUNDLES_OPERATIONAL_PLAN.md` | Plan Bundles |
| `50_CLAUDE_ARTIFACTS_OPERATOR_PLAN.md` | Plan Claude artifacts |
| `60_ALERT_WEBHOOK_ACTIVE_PLAN.md` | Plan alert_webhook |
| `70_ADMIN_TRADING_GATE.md` | Gate admin-trading |
| `80_NEXT_GO_SEQUENCE.md` | Ordre recommande prochains GO |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Demarrage

Branche creee : `go/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01`

Prochaine etape : produire les 9 fichiers du chantier.

## RISKS

- À qualifier.
