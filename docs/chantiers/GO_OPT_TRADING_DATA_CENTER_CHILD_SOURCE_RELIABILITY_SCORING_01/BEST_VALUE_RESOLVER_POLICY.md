---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01_BEST_VALUE_RESOLVER_POLICY
doc_type: policy
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
links:
  - schemas/source_score.v1.schema.json
  - schemas/source_evidence.v1.schema.json
  - schemas/canonical_value.v1.schema.json
  - schemas/resolver_decision.v1.schema.json
---

# BEST_VALUE_RESOLVER_POLICY

## Objet

Definir la policy de selection de la meilleure valeur pour un contract multi-source. Cette policy est appliquee par le Data Center, pas par DeskPro.

## 1. Principe

```text
candidate sources
→ evaluation (source_score.v1 + source_evidence.v1)
→ selection (resolver_decision.v1)
→ publication (canonical_value.v1)
→ data/data_center/views/<contract_class>/
→ DeskPro / Strategy / Perf / Telegram / Sheets / Dashboards
```

Les consumers lisent la view canonique. Ils ne savent pas quelle source a gagne. La decision du resolver est tracee et auditable.

## 2. Algorithme de resolution

### Etape 1 — Identification

```text
Input:  GET /resolve?contract_class=market_metrics.v1&symbol=BTCUSDT&data_key=open_interest
Output: canonical_value.v1
```

1. Identifier le `contract_class` depuis la requete.
2. Lister les producers enregistres pour ce contract_class dans `producers.json`.
3. Verifier que chaque producer a une donnee disponible (last_write non null, fichier existant).

### Etape 2 — Scoring

Pour chaque producer candidat :

1. Calculer `source_score.v1` selon les 8 dimensions ponderees.
2. Produire `source_evidence.v1` avec les justifications.
3. Verifier l'eligibilite :
   - `final_score >= min_score_threshold` (defaut: 0.3)
   - `permission.value > 0` (source accessible)
   - `schema_validation.value > 0` (donnee conforme au schema)

### Etape 3 — Selection

1. Filtrer les candidats eligibles.
2. Si aucun candidat eligible → `selection_rule = "stale_fallback"`, retourner la derniere valeur canonique avec `stale = true`.
3. Si un seul candidat eligible → `selection_rule = "only_eligible"`, le selectionner.
4. Si plusieurs candidats eligibles → `selection_rule = "highest_score"`, selectionner celui avec le `final_score` le plus eleve.
5. En cas d'egalite de score → departager par `freshness` (le plus recent gagne).
6. En cas d'egalite persistante → departager par `source_reliability` (uptime historique).

### Etape 4 — Decision

Produire `resolver_decision.v1` avec :
- La liste complete des candidats (scores, eligibility, disqualification)
- Le producer selectionne et son score
- La raison de selection
- La regle appliquee

### Etape 5 — Publication

Produire `canonical_value.v1` avec :
- La valeur du producer gagnant
- La reference au resolver_decision
- Le score du gagnant
- Les alternatives (autres sources) pour audit
- Le flag `stale` si fallback

### Etape 6 — Mise a jour de la view

Ecrire `canonical_value.v1` dans la view correspondante :

```text
data/data_center/views/<contract_class>/by_symbol/<symbol>.json
data/data_center/views/<contract_class>/latest.json  (aggregation multi-symbol)
```

## 3. Cas concret : market_metrics.v1

### Contexte

```text
Contract:     market_metrics.v1
Producers:    derivatives_collector__bitget
              derivatives_collector__binance
Symbol:       BTCUSDT
Data keys:    open_interest, funding_rate, volume_futures,
              long_short_ratio, liquidations_long, liquidations_short
```

### Scenario nominal

```text
bitget:
  open_interest = 28_450_000_000
  score = 0.87
  eligible = true

binance:
  open_interest = 28_320_000_000
  score = 0.72
  eligible = true

→ selection_rule = "highest_score"
→ selected = bitget (0.87 > 0.72)
→ canonical_value = 28_450_000_000
```

### Scenario avec source invalide

```text
bitget:
  open_interest = 28_450_000_000
  score = 0.87
  eligible = true

binance:
  open_interest = null  (donnee manquante)
  score = 0.12  (< 0.3 threshold)
  eligible = false
  disqualification = "score_below_threshold + missing_value"

→ selection_rule = "only_eligible"
→ selected = bitget
→ canonical_value = 28_450_000_000
```

### Scenario sans donnee fraiche

```text
bitget:
  last_write = null (jamais execute)

binance:
  last_write = null (jamais execute)

→ 0 candidats eligibles
→ selection_rule = "stale_fallback"
→ canonical_value = derniere valeur connue
→ stale = true
```

## 4. Seuils de decision

| Parametre | Valeur par defaut | Description |
|---|---|---|
| `min_score_threshold` | 0.3 | Score minimum pour qu'une source soit eligible |
| `max_age_seconds` | 3600 | Age maximum d'une donnee pour etre consideree fraiche (1h) |
| `stale_max_age_seconds` | 86400 | Age maximum pour le fallback stale (24h) |
| `consistency_tolerance_pct` | 5.0 | Ecart maximum entre sources pour cross_source_consistency = 1.0 |
| `freshness_decay_rate` | 0.05 | Perte de score freshness par seconde au-dela de max_age/2 |

## 5. Regles de scoring dimensionnelles

### 5.1 source_reliability (poids 0.20)

```text
value = 1.0 - (consecutive_failures / 10)  (min 0.1)
Base: 0.8 si la source a deja ecrit au moins une fois
Base: 0.5 si last_write = null (source jamais testee)
```

### 5.2 freshness (poids 0.20)

```text
age_seconds = now - produced_at
if age_seconds <= max_age_seconds / 2:
    value = 1.0
else:
    value = max(0.1, 1.0 - (age_seconds / max_age_seconds))
```

### 5.3 schema_validation (poids 0.15)

```text
value = 1.0 si schema valide sans erreur
value = 0.8 si schema valide avec warnings
value = 0.0 si schema invalide
```

### 5.4 completeness (poids 0.15)

```text
value = metrics_present / metrics_expected
```

### 5.5 cross_source_consistency (poids 0.10)

```text
Pour chaque peer source :
    deviation = |this_value - peer_value| / max(|this_value|, |peer_value|, 1)
    if deviation <= consistency_tolerance_pct / 100:
        peer_score += 1
value = peer_score / (nombre de peers + 1)
Si pas de peer → value = 0.5 (neutre)
```

### 5.6 historical_accuracy (poids 0.10)

```text
Si historique disponible :
    value = 1.0 - mean_relative_error
Sinon :
    value = 0.5 (neutre, pas de donnees historiques)
```

### 5.7 latency (poids 0.05)

```text
total_ms = collection_duration_ms + pipeline_duration_ms
value = max(0.1, 1.0 - (total_ms / 60000))  (1 min = 0.0)
```

### 5.8 permission (poids 0.05)

```text
value = 1.0 si api_key_valid ET rate_limit_ok ET entitlement = full
value = 0.5 si entitlement = limited
value = 0.0 si api_key expired / revoked
```

## 6. Interdits

- Pas de resolver dans DeskPro.
- Pas de scoring source dans DeskPro.
- Pas de lecture directe de producer path par DeskPro.
- Pas de best value sans `resolver_decision.v1` publie.
- Pas de selection de source sans `source_score.v1` + `source_evidence.v1`.
- Pas de valeur canonique publiee sans reference au `resolver_decision`.
- Pas de comparaison inter-contracts (on ne compare que des sources d'un meme contract_class).

## 7. Stockage

```text
data/data_center/scores/<producer_id>/<contract_class>/<symbol>/<data_key>/source_score.v1.json
data/data_center/scores/<producer_id>/<contract_class>/<symbol>/<data_key>/source_evidence.v1.json
data/data_center/resolver/<contract_class>/<symbol>/resolver_decision.v1.json
data/data_center/views/<contract_class>/by_symbol/<symbol>.json  (canonical_value)
data/data_center/views/<contract_class>/latest.json               (aggregation)
```
