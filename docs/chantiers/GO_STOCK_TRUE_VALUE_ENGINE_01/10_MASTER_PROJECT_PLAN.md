# GO_STOCK_TRUE_VALUE_ENGINE_01 — Master Project Plan

Status: MASTER_PROJECT_PLAN
Mode: documentation-first
Created: 2026-06-13

---

## Direction

Créer un moteur de lecture fondamentale + spéculative pour les actions suivies par le setup opt-trading.

Le moteur doit répondre à une question centrale :

> Le prix actuel est-il soutenu par la valeur réelle, par les flux, par la spéculation, ou par une surprise anticipable ?

---

## Roadmap

### Phase 1 — Documentation canonique

- créer la fiche initiale;
- définir les axes de scoring;
- fixer les poids initiaux;
- définir les contrats de sortie;
- indexer le chantier.

### Phase 2 — Schéma canonique

- produire `schema.yaml`;
- produire `score_weights.yaml`;
- produire `watchlist_config.yaml`;
- produire un exemple JSON complet par ticker.

### Phase 3 — Collecteurs

Sources candidates :

- Yahoo Finance;
- SEC EDGAR;
- FMP;
- Alpha Vantage;
- Finnhub;
- Nasdaq Earnings Calendar;
- TradingView;
- ETF flow providers;
- options data provider.

### Phase 4 — Scoring Engine

Créer un module capable de calculer :

- fundamental_score;
- valuation_score;
- flow_score;
- speculation_score;
- surprise_score;
- true_value_score;
- hype_score;
- final_grade.

### Phase 5 — Reporting

Sorties :

- rapport quotidien;
- rapport hebdomadaire;
- dashboard LocalCMS;
- signal Telegram optionnel;
- intégration watchlist bundle.

---

## Major Axes

1. Fondamentaux.
2. Valorisation.
3. Flux / liquidité.
4. Spéculation / surachat.
5. Surprise Engine.
6. Scoring final.
7. Reporting et gouvernance.

---

## Non-objectifs initiaux

- Pas d'ordre auto.
- Pas de recommandation achat/vente automatique.
- Pas de dépendance à une seule source.
- Pas de scoring opaque non documenté.

---

## Validation attendue

Le chantier est prêt pour un child GO de schéma lorsque les documents suivants existent :

- `00_INITIAL_PROJECT_DOC.md`;
- `10_MASTER_PROJECT_PLAN.md`;
- `20_CANONICAL_SCORING_MODEL.md`;
- `30_DATA_SOURCES_AND_COLLECTORS.md`;
- `40_OUTPUT_CONTRACTS.md`;
- `70_RESUME_POINT.md`;
- inbox index.
