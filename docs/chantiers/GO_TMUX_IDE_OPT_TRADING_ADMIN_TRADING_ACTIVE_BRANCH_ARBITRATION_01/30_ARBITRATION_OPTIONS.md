---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01_30_ARBITRATION_OPTIONS
doc_type: chantier/options
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01
status: active
scope: doc-only
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/20_BRANCH_ANALYSIS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/40_SELECTED_DECISION.md
---

# 30_ARBITRATION_OPTIONS

## Option A - garder la branche active telle quelle et reprendre tmux-ide tout de suite

Statut : **REJETEE**

Raisons :

- `admin-trading:/opt/trading` ne serait toujours pas sur une base canonique `sot/mainline`
- le chantier desk-pro resterait non merge et sans PR
- la suite `tmux-ide` continuerait au-dessus d'une branche fonctionnelle et non closee

## Option B - basculer immediatement vers `sot/mainline` parce que rien n'est seulement local

Statut : **ADMISSIBLE MAIS NON RETENUE**

Points positifs :

- les commits `1a52bb0` et `eadc6f5` sont deja sur `origin`
- il n'y a pas besoin de sauvegarde supplementaire pour eviter une perte de commit

Points negatifs :

- aucune PR n'existe encore pour materialiser la revue et la fusion du travail desk-pro
- le basculement maintenant rend tres facile l'oubli d'un travail utile non merge
- la suite `tmux-ide` se remettrait en mouvement avant fermeture du sujet desk-pro

## Option C - creer une branche de sauvegarde

Statut : **NON NECESSAIRE**

Raison :

- la preuve de preservation existe deja sur `origin/go/...ARTIFACT_OUTPUT_01` et `origin/go/...ARTIFACT_OBSERVE_01`
- aucune donnee non poussee n'a ete detectee

## Option D - ouvrir une PR pour la branche active, merger, puis seulement ensuite realigner `admin-trading` sur `sot/mainline`

Statut : **RECOMMANDEE**

Raisons :

- le travail desk-pro est utile et deja pousse
- la branche active `OBSERVE_01` est un superset propre de `OUTPUT_01`
- la fermeture du sujet desk-pro devient explicite et tracable
- une fois la PR mergee, le retour de `admin-trading:/opt/trading` sur `sot/mainline` ne perd rien et redevient coherent pour la suite `tmux-ide`

## Synthese

| Option | Perte de commit evitee | Discipline de revue | Reprise tmux-ide saine | Decision |
| --- | --- | --- | --- | --- |
| A | oui | non | non | rejetee |
| B | oui | non | partielle | non retenue |
| C | oui | sans objet | sans effet | inutile |
| D | oui | oui | oui | retenue |

## RISKS

- À qualifier.
