# 03 — Inventory Global Wrappers (first pass)

## Source
Derived from `/usr/local/bin` scan for:
- `menu-*`
- `cmd-*`
- `sanity-*`

## Wrappers clearly present
Examples currently exposed globally:
- `menu-audit`, `cmd-audit`, `sanity-audit`
- `menu-auth`, `cmd-auth`, `sanity-auth`
- `menu-bot_vision`, `cmd-bot_vision`, `sanity-bot_vision`
- `menu-deepseek*`, `cmd-deepseek*`, `sanity-deepseek*`
- `menu-desk_analyze`, `cmd-desk_analyze`, `sanity-desk_analyze`
- `menu-desk_capture_inputs`, `cmd-desk_capture_inputs`, `sanity-desk_capture_inputs`
- `menu-desk_common`, `cmd-desk_common`, `sanity-desk_common`
- `menu-desk_pro`, `cmd-desk_pro`, `sanity-desk_pro`
- `menu-perf`, `cmd-perf`, `sanity-perf`
- `menu-router`, `cmd-router`, `sanity-router`
- `menu-vision_bot`, `cmd-vision_bot`, `sanity-vision_bot`
- `menu-webhook`, `cmd-webhook`, `sanity-webhook`

## Core Desk Pro wrappers missing despite module scripts existing
These modules have internal `scripts/menu.sh`, `scripts/cmd.sh`, `scripts/sanity_check.sh` in the repo, but no obvious corresponding global wrappers were seen in `/usr/local/bin` during this scan:
- `decision_engine`
- `derivatives_analyzer`
- `derivatives_collector`
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`
- `execution_engine`
- `journal_engine`
- `liquidation_analyzer`
- `market_scanner`
- `opportunity_ranker`
- `perf_engine`
- `portfolio_engine`
- `position_engine`
- `probability_engine`
- `risk_engine`

## Wrappers present but structure needs confirmation
The following wrappers exist globally and should be checked against actual module layout / intent:
- `cmd-bot_vision_step2`, `menu-bot_vision_step2`, `sanity-bot_vision_step2`
- `cmd-deepseek_hub`, `menu-deepseek_hub`, `sanity-deepseek_hub`
- `cmd-journal_de_bord`, `menu-journal_de_bord`, `sanity-journal_de_bord`
- `cmd-shared_sshfs_permanent`

## Naming inconsistencies observed
- `menu-desk-pro` and `menu-desk_pro` both exist
- `sanity-desk-pro` and `sanity-desk_pro` both exist
- `menu-desk-pro-student` / `sanity-desk-pro-student` also exist
- `cmd-ops_hub` and `cmd-ops_menu_hub` coexist
- mixed dash vs underscore naming appears across the wrapper layer

## First-pass conclusion
The wrapper layer is incomplete and inconsistent relative to the business modules already present. This is the highest-value packaging target before further UI expansion or API integration.

## Recommended wrapper standard for next phase
For each operator-approved module:
- `menu-<module>`
- `cmd-<module>`
- `sanity-<module>`

Prefer one canonical naming convention and avoid duplicate dash/underscore aliases unless explicitly required for backward compatibility.
