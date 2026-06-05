---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_SOURCE_SELECTION_POLICY
doc_type: policy
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/BEST_VALUE_RESOLVER_POLICY.md
---

# 40_SOURCE_SELECTION_POLICY

## Objet

Formaliser la policy de selection de source candidate. Le Data Center ne decide pas le trade — il arbitre les sources. Le source selector est le composant qui applique cette policy.

## 1. Terminologie verrouillee

```text
Data Center arbitre les sources.
Data Center ne decide pas les trades.

Data Center performs source selection, not trading decisioning.
```

| Composant | Role | Decision |
|---|---|---|
| **Source Selector** | Choisit la meilleure source candidate selon policy | Quelle source fournit la donnee |
| **Data Center** | Stocke, normalise, score, arbitre, expose | Quelle donnee est canonique |
| **Consumer** | Utilise la donnee exposee | Quoi faire avec la donnee (trade, affichage, analyse) |
| **Strategy** | Genere des signaux | LONG/SHORT/NEUTRAL |
| **Execution** | Envoie les ordres | Comment executer |

## 2. Modes de selection

### 2.1 Best Candidate (default)

```text
Input:  contract_class, symbol, data_key
Output: canonical_value from best candidate

Policy:
  1. List all candidates for (contract_class, data_key) from by_contract_class index
  2. For each candidate:
     a. Check freshness (stale flag, age < max_age)
     b. Check eligibility (score >= min_threshold, schema valid)
     c. Get source_score from cache or compute
  3. Sort eligible candidates by score desc
  4. Return value from highest-score candidate
  5. Attach resolver_decision with all candidates, scores, selection_reason
```

### 2.2 All Candidates (debug/audit)

```text
Input:  contract_class, symbol, data_key
Output: canonical_value + all candidate values + scores

Policy:
  1. Same as Best Candidate
  2. Return the best value as canonical_value
  3. ALSO return all candidates with their values, scores, eligibility
  4. Consumer can see why one source was chosen over another
```

### 2.3 Consensus (strict)

```text
Input:  contract_class, symbol, data_key
Output: canonical_value if consensus, else STALE

Policy:
  1. List all candidates
  2. Check freshness for all
  3. If < 2 candidates have fresh data → STALE
  4. If deviation between candidates > tolerance → FLAGGED (return best + flag)
  5. If deviation within tolerance → CONSENSUS (return mean/median)
```

### 2.4 Fallback only

```text
Input:  contract_class, symbol, data_key
Output: value from primary, fallback if primary stale

Policy:
  1. Try primary source
  2. If primary fresh → return primary
  3. If primary stale → try fallback
  4. If fallback fresh → return fallback
  5. If both stale → return last known value + stale=true
```

## 3. Selection mode assignment

| Contract class | Mode | Reason |
|---|---|---|
| market_metrics.v1 | best_candidate | 2 sources (bitget + binance), score-based selection |
| pair_market_snapshot.v1 | fallback_only | 1 source primary, fallback TBD |
| vision_analysis.v1 | best_candidate | 1 source for now, extensible |
| vision_context.coinglass.v1 | fallback_only | 1 source (headless → API future) |
| vision_context.screener.v1 | fallback_only | 1 source (headless) |
| vision_context.news_sentiment.v1 | fallback_only | 1 source (headless) |

## 4. Selection decision audit

Chaque selection produit `resolver_decision.v1` (specifie dans `SOURCE_RELIABILITY_SCORING_01`) :

```json
{
  "schema_version": "resolver_decision.v1",
  "decision_id": "uuid",
  "contract_class": "market_metrics.v1",
  "symbol": "BTCUSDT",
  "data_key": "open_interest",
  "decided_at": "2026-06-05T12:00:00Z",
  "selection_mode": "best_candidate",
  "candidates": [
    {"producer_id": "derivatives_collector__bitget", "score": 0.87, "eligible": true},
    {"producer_id": "derivatives_collector__binance", "score": 0.72, "eligible": true}
  ],
  "selected_producer_id": "derivatives_collector__bitget",
  "selection_reason": "bitget score 0.87 > binance score 0.72, both eligible",
  "selection_rule": "highest_score"
}
```

## 5. Edge cases

| Case | Behavior |
|---|---|
| 0 candidates | return STALE, canonical_value=null, stale=true |
| 1 candidate, stale | return STALE, last known value |
| 1 candidate, fresh | return value, mode=only_eligible |
| 2+ candidates, all stale | return STALE, last best value |
| 2+ candidates, all below threshold | return STALE, no eligible source |
| 2+ candidates, tie on score | break by freshness, then reliability |
| Candidate returns error | disqualify, retry with next best |
