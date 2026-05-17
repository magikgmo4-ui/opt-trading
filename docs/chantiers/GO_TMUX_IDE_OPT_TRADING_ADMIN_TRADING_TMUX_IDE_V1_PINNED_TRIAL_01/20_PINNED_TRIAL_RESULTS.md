# 20_PINNED_TRIAL_RESULTS

## 1_MASTER_TARGET

Documenter le resultat du trial pinne `tmux-ide@1.3.1` sur `admin-trading`.

## 7_CANONICAL_STATE

Commandes autorisees executees :

```text
npx -y tmux-ide@1.3.1 --version
npx -y tmux-ide@1.3.1 --help
```

## 8_RESULTS

| Commande | Resultat | Exit |
| --- | --- | --- |
| `npx -y tmux-ide@1.3.1 --version` | `tmux-ide v1.3.1` | 0 |
| `npx -y tmux-ide@1.3.1 --help` | usage affiche | 0 |

## 9_HELP_SUMMARY

Le help de `tmux-ide@1.3.1` expose notamment :

- `tmux-ide` : launch IDE from `ide.yml` ;
- `tmux-ide <path>` : launch from a specific directory ;
- `tmux-ide init [--template]` : scaffold a new `ide.yml` ;
- `tmux-ide doctor` : check system requirements ;
- `tmux-ide validate [--json]` : validate `ide.yml` ;
- `tmux-ide detect [--json]` ;
- `tmux-ide detect --write` ;
- `tmux-ide status [--json]` ;
- `tmux-ide inspect [--json]` ;
- `tmux-ide config [--json]`.

## 10_INTERPRETATION

`tmux-ide@1.3.1` est executable sur `admin-trading` via `npx -y` pour les commandes non destructives testees.

Ce resultat ne prouve pas encore :

- que `doctor` passe ;
- que `validate` passe ;
- qu'un `ide.yml` peut etre cree sans cadrage ;
- qu'une session tmux-ide doit etre lancee ;
- qu'une installation globale est acceptable.

## 12_INVARIANTS

- Aucun `npm install -g`.
- Aucun `ide.yml`.
- Aucun `detect --write`.
- Aucun `init`.
- Aucun lancement de session.
- Aucun changement durable connu hors comportement normal de `npx`.

## 17_RESUME_POINT

Le trial pinne passe pour `--version` et `--help`; la suite doit rester gatee avant `ide.yml`.
