---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01_40_REALIGN_PLAN
doc_type: chantier/plan
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
status: active
scope: doc-only
---

# 40_REALIGN_PLAN

## Plan operatoire recommande

1. Reconnecter `admin-trading` en SSH read-only pour relire l'etat Git.
2. Capturer les refs locales et upstream exactes.
3. Valider l'absence de travail local a proteger.
4. Choisir la base canonique de reprise:
   - `origin/sot/mainline`
   - branche de travail GO explicite ensuite
5. Executer le realignement Git sur machine cible dans un lot machine-first separe.
6. Revenir ensuite sur `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` pour qualifier `tmux-ide`.

## Frontiere explicite

Ce GO ne fait qu'ouvrir et borner le travail de realignement.
Il ne modifie pas `admin-trading` dans cette PR.
