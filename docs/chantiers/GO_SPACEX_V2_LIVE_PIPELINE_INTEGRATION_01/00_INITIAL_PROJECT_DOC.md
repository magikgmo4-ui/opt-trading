---
doc_id: GO_SPACEX_V2_LIVE_PIPELINE_INTEGRATION_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_LIVE_PIPELINE_INTEGRATION_01
parent_go: GO_SPACEX_V2_BACKTEST_RUNNER_IMPLEMENTATION_01
status: draft
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_V2_BACKTEST_RUNNER_IMPLEMENTATION_01/00_INITIAL_PROJECT_DOC.md
  - modules/spcx_v2/
  - modules/ipo_tracking/pipeline.py
  - modules/ipo_tracking/reports.py
  - modules/ipo_tracking/telegram_dispatcher.py
  - modules/ipo_tracking/sheets_consumer.py
  - scripts/ipo/spacex_collect_once_v5.sh
  - scripts/ipo/spacex_report_daily_v5.sh
---

# GO_SPACEX_V2_LIVE_PIPELINE_INTEGRATION_01

## [6_FINAL_TARGET]

Brancher le runner SPCX V2 (`modules/spcx_v2/`) au pipeline de collection SpaceX existant (`modules/ipo_tracking/`) pour que chaque cycle `collect-once` produise automatiquement des détections de setup, des logs paper, et des exports Desk/Sheets/Telegram.

---

## [7_CANONICAL_STATE] — Files

```text
modules/spcx_v2/pipeline_adapter.py      # bridge entre enriched snapshot et MarketSnapshot
scripts/ipo/spacex_collect_and_detect.sh # collect-once + spcx_v2 runner
tests/test_spcx_v2_pipeline_integration.py
docs/chantiers/GO_SPACEX_V2_LIVE_PIPELINE_INTEGRATION_01/
├── 00_INITIAL_PROJECT_DOC.md
└── FILE_SCOPE.txt
```

---

## [5_GO_PLAN]

### pipeline_adapter.py

- `from modules.spcx_v2.config import MarketSnapshot`
- `def enriched_to_snapshot(enriched: dict) -> MarketSnapshot`
- Lit le fichier `data/ipo/spacex/enriched/latest.json`
- Convertit les champs enrichis (price, volume, VWAP, spread, halt, structures SMC, news) en `MarketSnapshot`
- Gère les cas où les données sont absentes (price_status="missing")

### spacex_collect_and_detect.sh

- Appelle `spacex_collect_once_v5.sh` d'abord
- Puis appelle `python3 -m modules.spcx_v2.runner --once`
- Puis appelle `python3 -m modules.spcx_v2.runner --summary` pour le log

### Wire reports/telegram/sheets

- Après `runner --once`, le paper_logger a écrit dans `data/ipo/spacex/paper_log/`
- Ajouter un appel `write_spcx_setups_to_report()` dans `reports.py` ou comme étape du pipeline
- Les setups A+ déclenchent une notification Telegram via `shared/telegram_notify.py`
- Les setups A+/A sont ajoutés à l'onglet Sheets via `sheets_consumer.py`

---

## [11_KEY_DECISIONS]

- Aucune modification des modules `ipo_tracking/` existants
- Le pipeline_adapter est dans `modules/spcx_v2/`, pas dans `modules/ipo_tracking/`
- Le script `collect_and_detect.sh` est un wrapper, pas un remplacement
- La chaîne paper-only est conservée
- Telegram: seuls les setups A+ sont notifiés en temps réel
- Sheets: tous les setups A+ et A sont exportés
- Le résumé EOD inclut les stats du paper_logger

---

## [12_INVARIANTS]

1. PAPER ONLY à toutes les étapes
2. NO LIVE PRICE = NO SETUP (Gate 0 bloque)
3. TOUT LOGGÉ (y compris rejets)
4. ZÉRO MODIFICATION des modules existants
5. DÉTERMINISME du replay

---

## [17_RESUME_POINT]

```text
Branchement du runner SPCX V2 au pipeline ipo_tracking.
Wrappers: pipeline_adapter.py (conversion enriched -> MarketSnapshot),
collect_and_detect.sh (collect + runner --once + summary).
Exports: reports, Telegram (A+), Sheets (A+/A), Desk.
```
