---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01_40_SELECTED_DECISION
doc_type: chantier/decision
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01
status: active
scope: doc-only
decided_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/30_ARBITRATION_OPTIONS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/90_CLOSEOUT.md
---

# 40_SELECTED_DECISION

## Decision retenue

**Reporter la suite `tmux-ide`.**

Avant toute reprise sur `admin-trading:/opt/trading`, ouvrir puis merger une PR base `sot/mainline` avec head :

```text
go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01
```

## Pourquoi `OBSERVE_01` et pas `OUTPUT_01`

`OBSERVE_01` est le head actuellement actif sur `admin-trading` et il contient deja :

- le commit fonctionnel `1a52bb0`
- le closeout d'observation `eadc6f5`

Autrement dit :

- ouvrir une PR depuis `OBSERVE_01` couvre tout le travail utile connu
- aucune branche de sauvegarde additionnelle n'est requise
- le travail restera traque dans une seule PR

## Si l'operateur veut une revue plus etroite

Alternative acceptable :

1. PR `OUTPUT_01` vers `sot/mainline`
2. puis PR `OBSERVE_01` si le closeout d'observation doit aussi etre merge

Cette alternative est plus decoupee, mais elle n'est pas la voie la plus simple.

## Ce que ce GO autorise

- constater que rien n'est seulement local sur `admin-trading`
- constater qu'aucune PR n'existe encore pour la chaine desk-pro
- recommander le traitement Git a faire avant `tmux-ide`

## Ce que ce GO n'execute pas

- aucun `git switch` sur `admin-trading`
- aucun `git pull`
- aucune PR desk-pro
- aucune installation `tmux-ide`
- aucune creation de `ide.yml`

## Suite operatoire recommandee

1. Ouvrir la PR desk-pro depuis `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01` vers `sot/mainline`.
2. La merger apres revue.
3. Ouvrir un GO d'execution pour remettre `admin-trading:/opt/trading` sur `sot/mainline` a jour.
4. Seulement ensuite reprendre la suite `tmux-ide`.

## Point de reprise exact

```text
admin-trading:/opt/trading
- branche active: go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01
- HEAD: eadc6f5
- base canonique courante: origin/sot/mainline @ c28b9bd2
- derive: mainline ahead 13, branch ahead 2
- PR desk-pro: aucune
- decision: PR/merge desk-pro d'abord, tmux-ide ensuite
```
