# desk_state — Step E (fichier canonique unique)

## But
Produire un state canonique: `/opt/trading/desk/state/latest.json`

Fusionne (si présents):
- `/opt/trading/desk/snapshots/latest.json`
- `/opt/trading/desk/inputs/tv_inputs_latest.json` (optionnel)
- `/opt/trading/desk/inputs/coinglass_latest.json` (optionnel)

## Sorties
- `/opt/trading/desk/state/latest.json`
- `/opt/trading/desk/state/history.jsonl`

## Install
Unzip à la racine du repo `/opt/trading`, puis:
- `bash INSTALL.sh`
- `modules/desk_state/scripts/sanity_check.sh`
- `modules/desk_state/scripts/cmd.sh build_once`

## Config
`cp modules/desk_state/config/desk_state.env.example modules/desk_state/config/desk_state.env`
