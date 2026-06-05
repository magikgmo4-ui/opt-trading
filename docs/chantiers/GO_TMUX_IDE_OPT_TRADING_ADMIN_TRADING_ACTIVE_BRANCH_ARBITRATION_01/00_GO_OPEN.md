---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01
status: active
scope: doc-only
opened_at: 2026-05-12
base: sot/mainline
branch: go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01
parent_go: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/90_CLOSEOUT.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/20_BRANCH_ANALYSIS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/30_ARBITRATION_OPTIONS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/40_SELECTED_DECISION.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01.md
---

# 00_GO_OPEN

## Identifiant

`GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01`

## Objectif

Arbitrer l'etat Git actif de `admin-trading:/opt/trading` avant toute reprise de la suite `tmux-ide`, sans reset, sans runtime change, sans toucher `modules/`, `db-layer` ou `OpenClaw`.

## Contexte etabli

| Element | Etat | Source |
| --- | --- | --- |
| `sot/mainline` local | clean et aligne | user `13_ESTABLISHED`, 2026-05-12 |
| PR `#311` | merged | GitHub, `2026-05-12T04:19:50Z` |
| `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01` | BLOCKED documente | `90_CLOSEOUT.md` |
| `tmux-ide` sur `admin-trading` | absent / `npx` EBADPLATFORM | GO qualify, `2026-05-12` |
| branche active sur `admin-trading:/opt/trading` | `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01` | probe live, `2026-05-12` |
| branche parente observee | `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01` | historique Git live |

## Questions a trancher

1. La branche active contient-elle encore un travail seulement local ?
2. Faut-il la pousser, ouvrir une PR, creer une sauvegarde, ou la laisser telle quelle ?
3. A quel moment `admin-trading:/opt/trading` peut-il revenir sur `sot/mainline` sans rien perdre ?
4. La suite `tmux-ide` doit-elle etre reportee tant que la branche desk-pro n'est pas traitee ?

## Regles

- Ne pas reset.
- Ne pas force push.
- Ne pas supprimer de branche.
- Ne pas installer `tmux-ide`.
- Ne pas creer `ide.yml`.
- Ne pas toucher runtime.
- Ne pas toucher `modules/`.
- Ne pas toucher `db-layer`.
- Ne pas toucher `OpenClaw`.
- Toute sortie de ce GO reste doc-only.

## Structure

| Fichier | Role |
| --- | --- |
| `10_SOURCE_STATE.md` | Etat local + probes SSH capturees le `2026-05-12` |
| `20_BRANCH_ANALYSIS.md` | Topologie des branches, commits, PR, derive contre `sot/mainline` |
| `30_ARBITRATION_OPTIONS.md` | Options comparees et admissibilite |
| `40_SELECTED_DECISION.md` | Decision retenue et suite operatoire |
| `90_CLOSEOUT.md` | Verdict de l'arbitrage |

## Critere de PASS

Le GO est `PASS` si les elements suivants sont prouvees et documentes :

- branche active exacte sur `admin-trading`
- relation exacte avec `origin/...OBSERVE_01`, `...OUTPUT_01` et `origin/sot/mainline`
- absence de travail seulement local
- decision explicite sur PR / sauvegarde / retour a `sot/mainline`
- gate explicite pour la suite `tmux-ide`

## RISKS

- À qualifier.
