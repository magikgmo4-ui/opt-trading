# 50_LOCALCMS_INTEGRATION

## Status

Draft only. LocalCMS route is deferred.

## Cards

Target cards:

```yaml
cards:
  - score_summary
  - true_value_vs_hype
  - catalyst_context
  - surprise_window
  - risk_flags
  - source_health
```

## Visible fields

```yaml
visible_fields:
  - ticker
  - universe
  - final_grade
  - final_score
  - catalyst_score
  - ecosystem_score
  - true_value_score
  - hype_score
  - surprise_score
  - risk_score
  - confidence_score
  - action_bias
  - flags
```

## Fallback behavior

If output file is absent:

```text
Display "No Stock/SpaceX True Value output available yet."
Do not crash LocalCMS.
```

If confidence is low:

```text
Show LOW_CONFIDENCE_SCORE visibly.
Do not hide the ticker.
```

## Route proposal

Future route:

```text
/localcms/spacex-true-value
```

or under existing SpaceX desk if present:

```text
/spacex/true-value
```
