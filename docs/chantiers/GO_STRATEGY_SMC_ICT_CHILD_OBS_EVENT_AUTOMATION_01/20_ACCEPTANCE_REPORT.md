---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_OBS_EVENT_AUTOMATION_01_ACCEPTANCE
doc_type: acceptance_report
go_id: GO_STRATEGY_SMC_ICT_CHILD_OBS_EVENT_AUTOMATION_01
verdict: PASS_OBS_EVENT_AUTOMATION
created_at: 2026-05-30
---

# 20_ACCEPTANCE_REPORT

## Verdict

```
PASS_OBS_EVENT_AUTOMATION
```

## Validations

```
tests/test_smc_ict_obs_processor.py   17 passed in 0.07s
sanity_check.sh                       PASS
git diff --check                      clean
```

## Surface livrée

```bash
# Poster manuellement un ObsEvent
cmd-smc_ict_obs_processor post \
  --direction LONG_WATCH \
  --choch true --mss true \
  --sweep true --sweep-type BSL_sweep \
  --fvg true --ob true \
  --premium-discount DISCOUNT \
  --invalidation "close_below_swing_low_90000" \
  --base-url http://127.0.0.1:8010

# Depuis un summary.json bot_vision_step2
cmd-smc_ict_obs_processor from-summary \
  /opt/_work/desk_pro/vision/latest/summary.json \
  --direction LONG_WATCH \
  --choch true \
  --invalidation "close_below_swing" \
  --dry-run
```

## État post-GO

```
G02 (OBS_EVENT_AUTOMATION) : CLOSED
Posting ObsEvents : possible (manuel + semi-auto depuis summary.json)
score_confidence  : implémenté (60_SCORING_INITIAL.md)
Prochain : accumuler ≥30 ObsEvents avant 2026-06-13 → PAPER_CLOSEOUT_01
```
