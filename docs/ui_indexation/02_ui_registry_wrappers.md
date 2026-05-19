# UI Registry — Wrappers / Entrées

## Wrappers UI déjà présents (extraits pertinents)

### Hub / entrypoints
- `menu-ops_menu_hub`
- `cmd-ops_menu_hub`
- `sanity-ops_menu_hub`
- `menu-desk_pro`
- `menu-desk-pro`
- `cmd-desk_pro`

### Operator / desk
- `cmd-desk_pro_runner`
- `cmd-desk_capture_inputs`
- `cmd-desk_analyze`
- `cmd-desk_pro_dashboard`
- `cmd-desk_state`
- `cmd-desk_snapshot_ingest`
- `cmd-desk_retention`

### Analysis / probability / trades
- `cmd-derivatives_analyzer`
- `cmd-decision_engine`
- `cmd-probability_engine`
- `cmd-risk_engine`
- `cmd-market_scanner`
- `cmd-liquidation_analyzer`
- `cmd-portfolio_engine`
- `cmd-position_engine`

### Monitoring / vision / perf
- `menu-perf`
- `cmd-perf`
- `cmd-perf_engine`
- `menu-vision_bot`
- `cmd-bot_vision`
- `cmd-bot_vision_step2`

## Lecture initiale
- Les entrées CLI sont déjà nombreuses et utilisables.
- Le travail futur côté UI n’est pas de créer des wrappers, mais de créer une **registry visuelle et des panneaux lisibles** au-dessus de ces wrappers.
- `ops_menu_hub` doit rester la couche CLI/hub; les futures UI MSI doivent être des surfaces plus visuelles et plus contextuelles.
