---
doc_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01_INBOX
doc_type: index/inbox_entry
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
status: active
scope: doc-only
---

# GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01

Ouverture doc-only du check de topologie cible avant implementation reelle `tmux-ide`.

Surfaces principales:
- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/`
- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/`
- `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/`

Decision posee:
- `cursor-ai` = poste operateur / IDE / Git / PR
- `db-layer` = runtime OpenClaw / gateway tmux deja PASS
- `admin-trading` = premiere cible a verifier pour `tmux-ide`

Reserve:
- verifier la machine cible avant execution
- ne pas casser `openclaw-gateway`

Validation reelle `2026-05-11`:
- SSH `cursor-ai -> admin-trading`: PASS
- repo `/opt/trading`: PASS
- prerequis `tmux` / `node` / `npm`: PASS
- `tmux-ide`: absent
- `ide.yml`: absent
- base Git machine cible pour ce GO: a remettre en canon avant implementation
