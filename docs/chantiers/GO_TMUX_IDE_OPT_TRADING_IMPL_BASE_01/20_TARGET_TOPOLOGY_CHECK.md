---
doc_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01_20_TARGET_TOPOLOGY_CHECK
doc_type: chantier/check
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
status: active
scope: doc-only
---

# 20_TARGET_TOPOLOGY_CHECK

## Topologie candidate A

`cursor-ai -> SSH -> admin-trading -> repo local opt-trading -> tmux-ide`

### Avantages

- conforme a l'hypothese distante du cadrage initial `tmux-ide`
- separe le poste operateur Windows du runtime Linux cible
- n'entre pas en collision directe avec `db-layer`
- reutilise une machine deja citee comme cible `tmux-ide`

### Risques

- machine cible encore a verifier en reel
- emplacement repo local a prouver
- prerequis `tmux`, `node`, `npm`, `tmux-ide` a qualifier

## Topologie candidate B

`cursor-ai -> SSH -> db-layer -> repo local opt-trading -> tmux-ide`

### Avantages

- machine Linux deja prouvee
- acces tmux deja demontre

### Risques majeurs

- collision potentielle avec la session runtime `openclaw-gateway`
- confusion entre outillage IDE et runtime OpenClaw
- hors reserve explicite posee par les surfaces globales recentes

## Topologie candidate C

`cursor-ai local Windows -> tmux-ide local`

### Avantages

- controle local operateur

### Risques majeurs

- non conforme a l'hypothese distante Linux/SSH du cadrage initial
- aucune preuve locale sur prerequis ou compatibilite utile
- risque de detourner le GO vers un autre mode de fonctionnement

## Evaluation

| Critere | A: admin-trading distant | B: db-layer distant | C: cursor-ai local |
| --- | --- | --- | --- |
| conforme au cadrage initial | oui | oui partiellement | non |
| preserve OpenClaw db-layer | oui | non | oui |
| machine cible deja citee dans surfaces tmux-ide | oui | non | non |
| separation operateur / runtime | oui | non | oui |
| besoin de requalification machine | oui | oui | oui |

## Verdict du check

Topologie recommandee pour l'ouverture d'implementation:

`cursor-ai -> SSH -> admin-trading`

Topologies explicitement non retenues par defaut:

- `db-layer` comme cible `tmux-ide` de base
- `cursor-ai` comme cible locale `tmux-ide` de base

## RISKS

- À qualifier.
