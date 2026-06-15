# 30_CANONICAL_SCORING_ENGINE

## Final score engine

```yaml
final_score_engine:
  spacex_context:
    catalyst_score: 0-100
    ecosystem_score: 0-100
    price_action_score: 0-100
    risk_penalty: 0-100

  true_value_layer:
    fundamental_score: 0-100
    valuation_score: 0-100
    flow_score: 0-100
    surprise_score: 0-100
    hype_score: 0-100
    risk_score: 0-100
    confidence_score: 0-100

  final:
    final_score: 0-100
    final_grade: A+|A|B|C|D|RESEARCH_REQUIRED
    action_bias: string
    flags: list
```

## Core formulas

```text
true_value_score =
  0.35 * fundamental_score +
  0.35 * valuation_score +
  0.15 * flow_score +
  0.15 * surprise_score
```

```text
hype_score =
  0.60 * speculation_score +
  0.20 * social_trend_score +
  0.20 * options_pressure_score
```

```text
risk_score =
  0.40 * hype_score +
  0.25 * valuation_overextension_risk +
  0.20 * earnings_event_risk +
  0.15 * data_confidence_penalty
```

## Consolidated final score

For SPCX / SpaceX ecosystem:

```text
final_score =
  0.25 * catalyst_score +
  0.20 * ecosystem_score +
  0.25 * true_value_score +
  0.15 * surprise_score +
  0.15 * (100 - risk_score)
```

For non-SPCX equity universe:

```text
final_score =
  0.45 * true_value_score +
  0.20 * flow_score +
  0.20 * surprise_score +
  0.15 * (100 - risk_score)
```

## Grade assignment

```yaml
A+:
  final_score: ">= 85"
  confidence_score: ">= 70"
  risk_score: "<= 70"

A:
  final_score: ">= 75"
  confidence_score: ">= 65"

B:
  final_score: ">= 60"

C:
  final_score: ">= 45"

D:
  final_score: "< 45"

RESEARCH_REQUIRED:
  confidence_score: "< 60"
```

## Interpretation matrix

| True Value | Hype | Interpretation |
|---:|---:|---|
| High | Low | neglected opportunity |
| High | High | leader; wait for pullback / size down |
| Low | High | dangerous speculation |
| Low | Low | weak / no interest |
| Medium | High | momentum-only candidate |
