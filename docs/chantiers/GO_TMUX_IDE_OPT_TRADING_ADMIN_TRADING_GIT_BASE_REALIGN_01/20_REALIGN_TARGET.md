---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01_20_REALIGN_TARGET
doc_type: chantier/target
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
status: active
scope: doc-only
---

# 20_REALIGN_TARGET

## Cible canonique a atteindre

Pour ouvrir une vraie qualification `tmux-ide`, `admin-trading` doit etre remis sur:

- un repo `/opt/trading` propre
- une base `origin/sot/mainline` verifiee
- une branche de travail explicite reliee au GO actif

## Etat cible minimal

| Critere | Cible |
| --- | --- |
| remote | `origin` vers `magikgmo4-ui/opt-trading` |
| base | `origin/sot/mainline` a jour |
| branche locale | branche explicite pour le GO actif ou lot de validation |
| worktree | propre |
| divergence upstream | absente ou volontaire et documentee |

## Ce que ce GO ne decide pas

- nom exact de la branche machine-side finale
- installation de `tmux-ide`
- contenu de `ide.yml`

Ces points viennent apres le realignement Git.

## RISKS

- À qualifier.
