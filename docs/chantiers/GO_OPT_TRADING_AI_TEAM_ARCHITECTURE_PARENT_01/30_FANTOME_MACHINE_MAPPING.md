# Mapping machine fantome

## Role retenu

- `fantome` est la machine candidate pour `AI Team / strict workers`
- elle porte un role d'execution parallele candidate, de simulation ou de workers specialises, si un futur GO le valide
- elle ne remplace pas `cursor-ai`, qui garde l'orchestration multi-agents locale

## Controles read-only executes

- `ssh fantome 'hostname; whoami; pwd; test -d /opt/trading && echo HAS_OPT_TRADING || true; test -d /home/fantome/opt-trading && echo HAS_HOME_OPT_TRADING || true'`
- `ssh fantome 'readlink -f /opt/trading || realpath /opt/trading || ls -ld /opt/trading'`

## Resultats

| Champ | Valeur constatee | Statut |
| --- | --- | --- |
| alias SSH | `fantome` | `PASS` |
| hostname | `fantome` | `PASS` |
| user | `fantome` | `PASS` |
| pwd | `/home/fantome` | `PASS` |
| chemin runtime attendu | `/opt/trading` present | `PASS` |
| chemin reel | `/home/fantome/opt-trading` | `PASS` |
| resolution | `/opt/trading -> /home/fantome/opt-trading` | `PASS` |

## Separation avec cursor-ai

| Machine | Role principal | Hors scope ici |
| --- | --- | --- |
| `cursor-ai` | orchestration multi-agents, IDE, prompts, Git, arbitrage humain | execution AI Team parallele |
| `fantome` | AI Team, `strict workers`, environnement parallele candidat | orchestration Git/prompt principale |

## Separation avec les autres machines

| Machine | Role retenu |
| --- | --- |
| `db-layer` | `OpenClaw` + `LocalCMS` actuels |
| `admin-trading` | runtime trading / bot_vision / deskpro / webhook / collectors |
| `student` | `Local Ollama` differe |

## Limites / gaps

- le probe SSH prouve la disponibilite machine et les chemins, pas une execution AI Team effective
- aucun outillage `strict workers` n'est deploye ni lance sur `fantome` dans ce GO
