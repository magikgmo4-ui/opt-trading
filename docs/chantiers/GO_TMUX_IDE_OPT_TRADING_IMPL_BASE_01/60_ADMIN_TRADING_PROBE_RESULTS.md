---
doc_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01_60_ADMIN_TRADING_PROBE_RESULTS
doc_type: chantier/probe_results
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
status: active
scope: doc-only
---

# 60_ADMIN_TRADING_PROBE_RESULTS

## Verdict par gate

| Gate | Resultat | Observation |
| --- | --- | --- |
| SSH `cursor-ai -> admin-trading` | PASS | acces SSH direct confirme |
| Identite machine cible | PASS | `admin-trading`, user `ghost` |
| Presence repo `opt-trading` | PASS | `/opt/trading` present |
| Remote Git cible | PASS | `origin` pointe vers le repo GitHub canonique |
| Repo propre | PASS | aucun fichier modifie localement |
| Branche canonique de depart | FAIL | branche courante non alignee sur `sot/mainline` ni sur le GO courant |
| Upstream coherent | FAIL | upstream differente du nom de branche locale |
| `tmux` present | PASS | `tmux 3.3a` |
| `node` / `npm` presents | PASS | `node v18.20.4`, `npm 9.2.0` |
| `tmux-ide` present | FAIL | commande absente |
| `ide.yml` present | FAIL | aucun fichier detecte |
| Impact `db-layer` | PASS | aucun acces, aucune modification, aucun couplage runtime |

## Sens operatoire

`admin-trading` est bien la premiere cible validee pour la suite, mais uniquement comme machine
a preparer. Elle n'est pas encore une cible prete pour `doctor` / `validate`.

## Risque principal actuel

Passer trop vite a l'installation ou au reglage `tmux-ide` sans d'abord remettre la machine
sur une base Git de travail explicite pour ce GO.
