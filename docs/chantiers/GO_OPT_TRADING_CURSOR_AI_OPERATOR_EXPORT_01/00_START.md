---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01
machine: cursor-ai
status: active
lifecycle_stage: operator_export
links:
  - bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md
  - bundles/operator-export/README.md
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01.md
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01

## Objet

Option C de la sequence cursor-ai : produire un export operateur propre, autonome, lisible et transportable a partir des bundles et packets deja valides apres Options A et B.

## Etat valide

- Option A (alert webhook test safe) : MERGE — PR #210.
- Option B (bundles maintenance) : MERGE — PR #211.
- Pack Claude artifacts : 6 fichiers, complet.
- Bundles workflow actif.
- Admin-trading ferme.

## Livrables

| Emplacement | Fichier | Contenu |
| --- | --- | --- |
| `bundles/operator-export/` | `README.md` | Survol de l'export |
| `bundles/operator-export/` | `EXPORT_MANIFEST.json` | Inventaire structure de l'export |
| `bundles/operator-export/` | `HANDOFF.md` | Instructions de handoff pour operateur |
| `bundles/operator-export/` | `CHECKLIST_VERIFICATION.md` | Checklist de verification de l'export |

## Chantier

`docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01/`

## Invariants

- Machine : cursor-ai.
- Doc-only / bundle-only.
- Admin-trading ferme.
- Aucun secret, runtime, endpoint externe.

## RISKS

- À qualifier.
