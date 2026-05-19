# desk_capture_inputs — Step D (feed Desk inputs from TradingView captures)

- Reads `/opt/trading/desk/snapshots/latest.json`
- Extracts compact inputs from each quadrant image (OpenAI Vision)
- Writes:
  - `/opt/trading/desk/inputs/tv_inputs_latest.json`
  - `/opt/trading/desk/inputs/tv_inputs_history.jsonl`
- Optionally merges extracted `tv_inputs` back into `desk/snapshots/latest.json`.

Config:
Copy env:
`cp modules/desk_capture_inputs/config/desk_capture_inputs.env.example modules/desk_capture_inputs/config/desk_capture_inputs.env`

Run:
- `modules/desk_capture_inputs/scripts/sanity_check.sh`
- `modules/desk_capture_inputs/scripts/cmd.sh extract_once`
- `modules/desk_capture_inputs/scripts/cmd.sh print_latest`

## Statut de stack
- satellite d'extraction d'inputs pour la stack Desk Pro
- adjacent a la stack, sans etre un entrypoint operateur principal
