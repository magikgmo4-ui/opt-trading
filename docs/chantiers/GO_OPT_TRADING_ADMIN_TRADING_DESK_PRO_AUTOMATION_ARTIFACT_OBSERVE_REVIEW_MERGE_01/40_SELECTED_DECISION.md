---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01_40_SELECTED_DECISION
doc_type: chantier/decision
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01
status: active
scope: doc-only
decided_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01/30_REVIEW_MERGE_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01/90_CLOSEOUT.md
---

# 40_SELECTED_DECISION

## Decision

**Traiter la branche active complete `ARTIFACT_STABILITY_WINDOW_01` avant tout realignement `admin-trading` et avant toute reprise `tmux-ide`.**

Branche a ouvrir en PR :

```text
go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_STABILITY_WINDOW_01
```

## Statut de `OBSERVE_01`

`OBSERVE_01` n'est pas abandonnee. Elle est incluse dans `STABILITY_WINDOW_01`.

```text
OUTPUT_01 -> OBSERVE_01 -> STABILITY_WINDOW_01
```

La demande initiale "traiter observe" reste satisfaite par le traitement du head complet, car cela merge aussi le commit `eadc6f5`.

## Actions non retenues

| Action | Decision | Raison |
| --- | --- | --- |
| PR depuis `OUTPUT_01` | non retenue | laisserait observation + stabilite hors PR |
| PR depuis `OBSERVE_01` | non retenue | laisserait `STABILITY_WINDOW_01` hors PR |
| switch immediat de `admin-trading` vers `sot/mainline` | non retenu | le travail desk-pro n'est pas merge |
| branche de sauvegarde | non necessaire | les commits sont deja sur `origin` |

## Gate suivante

La prochaine action GitHub doit etre une PR fonctionnelle desk-pro, pas une PR `tmux-ide`.

Apres merge de cette PR, ouvrir un GO d'execution dedie au realignement de `admin-trading:/opt/trading` sur `sot/mainline`.

## Point de reprise

```text
sot/mainline @ a86ca134
admin-trading:/opt/trading @ 2908ff32
branche active: go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_STABILITY_WINDOW_01
PR existante: aucune
decision: ouvrir PR depuis STABILITY_WINDOW_01 vers sot/mainline
tmux-ide: reporte
```

## RISKS

- À qualifier.
