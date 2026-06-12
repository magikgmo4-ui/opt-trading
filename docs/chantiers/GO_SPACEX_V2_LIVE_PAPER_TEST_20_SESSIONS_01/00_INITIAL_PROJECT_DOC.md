---
doc_id: GO_SPACEX_V2_LIVE_PAPER_TEST_20_SESSIONS_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_LIVE_PAPER_TEST_20_SESSIONS_01
parent_go: GO_SPACEX_V2_PROXY_IPO_BACKTEST_01
status: draft
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_V2_PROXY_IPO_BACKTEST_01/00_INITIAL_PROJECT_DOC.md
  - modules/spcx_v2/
  - modules/ipo_tracking/pipeline.py
  - scripts/ipo/spacex_collect_and_detect.sh
---

# GO_SPACEX_V2_LIVE_PAPER_TEST_20_SESSIONS_01

## [6_FINAL_TARGET]

Exécuter 20 sessions paper avec SPCX réel, collecter tous les setups, calculer les stats réelles (winrate, expectancy, MFE/MAE), et décider quels setups promouvoir de paper-only à validé.

---

## [7_CANONICAL_STATE] — Files

```text
modules/spcx_v2/session_tracker.py      # session counter + validation decisions
scripts/ipo/spacex_session_run.sh        # single session runner
tests/test_spcx_v2_session_tracker.py
docs/chantiers/GO_SPACEX_V2_LIVE_PAPER_TEST_20_SESSIONS_01/
├── 00_INITIAL_PROJECT_DOC.md
└── FILE_SCOPE.txt
```

---

## [5_GO_PLAN]

### session_tracker.py

- `bump_session() -> int` — incrémente le compteur de sessions, retourne le numéro
- `get_session_count() -> int` — lit le compteur courant
- `is_test_complete() -> bool` — session >= 20 ?
- `validate_setup(setup_type: str) -> dict` — évalue si un setup mérite d'être validé
- Critères de validation :
  - Au moins 5 occurrences
  - Winrate >= 45%
  - Expectancy_R > 0
  - Profit factor > 1.1
  - Max drawdown_R < 5
- `graduation_report() -> dict` — rapport de décision : quels setups passent, quels setups sont rejetés

### spacex_session_run.sh

- Appelle `collect_and_detect.sh`
- Appelle `bump_session()`
- Si session == 5/10/15/20, génère un rapport intermédiaire
- Si session == 20, génère le `graduation_report()` final

### Graduation criteria per setup

| Setup | Min trades | Min WR | Min Exp. R | Min PF |
|-------|-----------|--------|-----------|--------|
| IPO_ORB_5M | 5 | 45% | >0 | 1.1 |
| IPO_ORB_15M | 5 | 45% | >0 | 1.1 |
| VWAP_HOLD_LONG | 3 | 40% | >0 | 1.0 |
| VWAP_RECLAIM | 3 | 40% | >0 | 1.0 |
| Others | 2 | 35% | >0 | 1.0 |

---

## [11_KEY_DECISIONS]

- Les sessions sont exécutées en production, pas simulées
- Chaque session = 1 cycle collect + detect
- Rapport intermédiaire toutes les 5 sessions
- Rapport de graduation à la session 20
- Les setups qui ne passent pas restent en paper-only
- Les setups qui passent sont marqués "validated" dans la config
- Décision finale manuelle (humaine) — le rapport est une recommandation

---

## [12_INVARIANTS]

1. PAPER ONLY — aucune exécution d'ordre pendant les 20 sessions
2. TOUT EST LOGGÉ — chaque session, chaque candidat
3. DÉCISION HUMAINE FINALE — le rapport recommande, ne décide pas seul
4. ZÉRO SECRET
5. REPRODUCTIBLE — le compteur de session est stocké dans un fichier

---

## [17_RESUME_POINT]

```text
20 sessions paper avec SPCX réel via collect_and_detect.sh.
Tracker de session avec graduation_report().
Critères de validation par setup (min trades, WR, expectancy, PF).
Rapports intermédiaires toutes les 5 sessions.
Décision finale humaine basée sur les stats réelles.
```
