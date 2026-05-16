# Matrice machine et connectivite

## Matrice principale

| Machine | Alias | Hostname constate | User constate | Chemin repo attendu | Chemin repo reel constate | Statut | Prochain chantier lie |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `db-layer` | `db-layer` | `db-layer` | `ghost` | `/opt/trading` | `/opt/trading` | `PASS` | cycle `db-layer` deja clarifie ; pas de nouveau GO machine prioritaire avant la suite transverse / orchestration |
| `admin-trading` | `admin-trading` | `admin-trading` | `ghost` | `/opt/trading` | `/opt/trading` | `PASS` | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` reste ouvert mais differe |
| `student` | `student` | `student` | `student` | `/opt/trading` | `/opt/trading` | `PASS` | `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` reste le meilleur candidat differe cote student |
| `fantome` | `fantome` | `fantome` | `fantome` | `/opt/trading` | `/home/fantome/opt-trading` via `/opt/trading` | `PASS_NOTE` | `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` reste principal ; `strict workers` reste a absorption differree |
| `cursor-ai` | `cursor-ai` | `DESKTOP-1KDQTBH` | `desktop-1kdqtbh\\ghost` | `C:\\Users\\ghost\\opt-trading` | `C:\\Users\\ghost\\opt-trading` | `PASS_LOCAL` | `GO_OPT_TRADING_MULTI_AGENTS_CURSOR_AI_PARENT_ALIGNMENT_01` recommande |

## Notes de lecture

- `db-layer`, `admin-trading`, `student` et `fantome` repondent tous en lecture seule depuis le poste courant
- pour `fantome`, `/opt/trading` existe mais se resolvait en reel vers `/home/fantome/opt-trading`
- pour `cursor-ai`, la verification utile de ce lot est locale : hostname Windows, user courant et chemin repo courant

## Verification specifique des raccourcis `reseau_ssh`

| Machine | `menu-reseau_ssh` | `cmd-reseau_ssh` | `sanity-reseau_ssh` | Statut |
| --- | --- | --- | --- | --- |
| `db-layer` | `modules/reseau_ssh/scripts/menu.sh` | `modules/reseau_ssh/scripts/cmd.sh` | `modules/reseau_ssh/scripts/sanity_check.sh` | `PASS` |
| `admin-trading` | `modules/reseau_ssh/scripts/menu.sh` | `modules/reseau_ssh/scripts/cmd.sh` | `modules/reseau_ssh/scripts/sanity_check.sh` | `PASS` |
| `student` | `modules/reseau_ssh/scripts/menu.sh` | `modules/reseau_ssh/scripts/cmd.sh` | `modules/reseau_ssh/scripts/sanity_check.sh` | `PASS` |
| `fantome` | `modules/reseau_ssh/scripts/menu.sh` sous `/home/fantome/opt-trading` | `modules/reseau_ssh/scripts/cmd.sh` sous `/home/fantome/opt-trading` | `modules/reseau_ssh/scripts/sanity_check.sh` sous `/home/fantome/opt-trading` | `PASS_NOTE` |
| `cursor-ai` | non verifie dans ce lot | non verifie dans ce lot | non verifie dans ce lot | `LOCAL_DEFER` |

## Gaps constates

- aucun gap de connectivite bloquant sur les quatre alias Linux prioritaires
- une divergence non bloquante de realpath repo existe sur `fantome`
- aucune preuve utile n'impose une probe SSH de `cursor-ai` dans ce lot
