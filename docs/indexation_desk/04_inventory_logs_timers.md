# 04 — Inventory Logs / Timers / Services (first pass)

## Source
Derived from:
- `systemctl list-unit-files --type=service`
- `systemctl list-unit-files --type=timer`
- `systemctl --type=service --state=running`
- log directory scan from the raw inventory log

## Services present in unit files
Relevant service units discovered:
- `bot_vision_step2.service`
- `desk_bridge.service`
- `desk_retention.service`
- `perf.service` (masked)
- `trading-heartbeat.service`
- `tv-perf.service`
- `tv-webhook.service`
- `vision_bot.service`

## Timers present in unit files
- `bot_vision_step2_prune.timer`
- `bot_vision_step2_send.timer`
- `desk_bridge.timer`
- `desk_retention.timer`
- `trading-heartbeat.timer`

## Running services at capture time
- `bot_vision_step2.service`
- `ngrok-tv.service`
- `tv-perf.service`
- `tv-webhook.service`
- `vision_bot.service`

## Immediate reading
### Live operational layer already active
Current live activity is concentrated around:
- webhook ingestion
- perf API
- bot vision
- tunnel / webhook connectivity

### Desk Pro core engines not yet surfaced as systemd-operated layer
The repo contains many Desk Pro business modules, but the running systemd layer is not yet a unified “Desk Pro production surface”.

## Common log / journal locations seen
- `./data/journal`
- `./data/logs`
- `./journal`
- `./journal/tmp`
- `./modules/desk_pro/logs`
- `./tmp`

## First-pass interpretation
### What already exists
- logging locations exist
- journal workflow exists
- retention / bridge timers already exist
- runtime services are already in use for some desk-adjacent flows

### What is still missing
- explicit mapping module -> log path
- explicit mapping module -> timer/service ownership
- clean separation of operator logs vs dev/debug logs
- clear exploitability standard for Desk Pro engines

## Priority questions for next pass
1. Which logs are source-of-truth for operators?
2. Which services belong to current production flow vs legacy experiments?
3. Which Desk Pro modules should eventually have timers/services, and which should remain on-demand only?
4. Should MSI consume services from admin-trading or host its own UI-facing units?

## Key conclusion
The exploitability layer exists, but it is centered on webhook/vision/perf rather than the full Desk Pro chain. Before expanding UI and APIs, the system should clarify which modules are on-demand tools, which are operator-facing commands, and which deserve service/timer packaging.

## RISKS

- À qualifier.
